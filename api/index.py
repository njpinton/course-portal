from flask import Flask, render_template, send_from_directory, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
import re
import logging
import sys
from datetime import datetime, timezone, timedelta
import jwt
from supabase import create_client, Client
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

# Add the API directory to the Python path for Vercel compatibility
import os.path
api_dir = os.path.dirname(os.path.abspath(__file__))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)
    print(f"DEBUG: Added {api_dir} to sys.path")

# Load environment variables early for Vercel compatibility
from dotenv import load_dotenv
# Load .env.local first if it exists (development), then .env (fallback)
if os.path.exists('.env.local'):
    load_dotenv('.env.local')
load_dotenv('.env')

try:
    print("DEBUG: Attempting to import supabase_client...")
    from supabase_client import (
        get_supabase_client, create_group, add_group_member, add_group_document,
        get_groups, get_group_details, delete_group, get_project_stages,
        update_stage_status, get_project_models, add_project_model,
        get_stage_documents, add_stage_document, update_group_project_info,
        update_group_credentials, get_group_by_username, update_group_last_login,
        get_group_with_submissions, submit_group_stage_work, get_group_feedback,
        get_class_by_code_section, get_students_by_class, get_ungrouped_students,
        get_grouped_students, assign_student_to_group, get_student_by_campus_id, get_student_by_id,
        get_group_members, unassign_student_from_group,
        upload_submission_file, get_submission_file_url, delete_submission_file
    )
    print("DEBUG: Successfully imported supabase_client")
except Exception as e:
    print(f"WARNING: Failed to import supabase_client: {e}")
    import traceback
    traceback.print_exc()
    # Define stub functions to prevent NameError
    def get_class_by_code_section(*args, **kwargs):
        return None
    def get_students_by_class(*args, **kwargs):
        return []
    def get_ungrouped_students(*args, **kwargs):
        return []
    def get_grouped_students(*args, **kwargs):
        return []
    def assign_student_to_group(*args, **kwargs):
        return None
    def get_student_by_campus_id(*args, **kwargs):
        return None
    def get_group_members(*args, **kwargs):
        return []
    def unassign_student_from_group(*args, **kwargs):
        return None
    def upload_submission_file(*args, **kwargs):
        return None
    def get_submission_file_url(*args, **kwargs):
        return None
    def delete_submission_file(*args, **kwargs):
        return False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# -- Supabase Configuration --
# To run this locally, you will need to create a .env file in the presenter_app directory
# with the following content:
# SUPABASE_URL=your_supabase_url
# SUPABASE_ANON_KEY=your_supabase_anon_key
# FLASK_SECRET_KEY=your_secret_key (required - no default fallback)
# ADMIN_USERNAME=admin
# ADMIN_PASSWORD_HASH=hashed_password (use werkzeug.security.generate_password_hash())
#
# You will also need to create a table in your Supabase project with the following schema:
# CREATE TABLE module_views (
#   module_number INT PRIMARY KEY,
#   view_count INT
# );
#
# And a function to increment the view count:
# CREATE OR REPLACE FUNCTION increment_module_view(module_id INT)
# RETURNS VOID AS $$
# BEGIN
#   INSERT INTO module_views (module_number, view_count)
#   VALUES (module_id, 1)
#   ON CONFLICT (module_number)
#   DO UPDATE SET view_count = module_views.view_count + 1;
# END;
# $$ LANGUAGE plpgsql;
#
# To get your Supabase URL and anon key, go to your Supabase project's
# API settings page.

# The global supabase client initialization is now handled in supabase_client.py
# --------------------------

app = Flask(__name__)

# Secret key management - secure by default
secret_key = os.environ.get('FLASK_SECRET_KEY')
if not secret_key:
    # In production (Vercel), use a derived key from Vercel's system
    # In development, warn but allow with a generated key
    is_production = os.environ.get('VERCEL_ENV') == 'production'

    if is_production:
        # For Vercel production, derive a key from existing secrets
        vercel_url = os.environ.get('VERCEL_URL', 'localhost')
        secret_key = f"vercel-{vercel_url}-{os.environ.get('VERCEL_GIT_COMMIT_SHA', 'dev')[:16]}"
        logger.warning("Using derived FLASK_SECRET_KEY from Vercel environment. Set FLASK_SECRET_KEY for better control.")
    else:
        # For local development, generate a key
        import secrets
        secret_key = secrets.token_urlsafe(32)
        logger.warning("Generated temporary FLASK_SECRET_KEY for development. Set FLASK_SECRET_KEY environment variable for production.")

app.secret_key = secret_key

# Configure CORS - only allow specified origins in production
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:*').split(',')
CORS(app, resources={
    r"/api/*": {"origins": allowed_origins, "methods": ["GET", "POST", "OPTIONS"]},
}, supports_credentials=True)
logger.info(f"CORS configured for origins: {allowed_origins}")

# JWT configuration for admin authentication (serverless-compatible)
JWT_SECRET = app.secret_key
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

def generate_admin_token():
    """Generate a JWT token for authenticated admin sessions"""
    payload = {
        'is_admin': True,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_admin_token(token):
    """Verify JWT token and return True if valid admin token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get('is_admin') == True
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False

def get_admin_token_from_request():
    """Extract JWT token from request (cookie or header)"""
    # Try cookie first
    token = request.cookies.get('admin_token')
    if token:
        return token

    # Try Authorization header
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]

    return None

def is_admin_authenticated():
    """Check if current request is from authenticated admin"""
    token = get_admin_token_from_request()
    if token and verify_admin_token(token):
        return True
    # Fallback to session for backwards compatibility
    return session.get('is_admin') == True

# Security configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx', 'csv', 'xls', 'xlsx'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

def allowed_file(filename: str, mime_type: str = None) -> bool:
    """Validate file type against allowed extensions and MIME types."""
    if not filename or '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False

    # Additional MIME type check if provided
    if mime_type and mime_type not in ALLOWED_MIME_TYPES:
        return False

    return True

def validate_input(value: str, max_length: int = 255, field_name: str = "input") -> tuple[bool, str]:
    """Validate string input for length and null bytes."""
    if not isinstance(value, str):
        return False, f"{field_name} must be a string"

    if not value or len(value.strip()) == 0:
        return False, f"{field_name} cannot be empty"

    if len(value) > max_length:
        return False, f"{field_name} exceeds maximum length of {max_length}"

    if '\x00' in value:
        return False, f"{field_name} contains invalid characters"

    return True, ""

# Module names and filenames for display
MODULES = {
    0: {
        "title": "Introduction to Machine Learning",
        "filename": "00-intro-to-machine-learning.html"
    },
    1: {
        "title": "Parameter Estimation",
        "filename": "01-parameter-estimation.html"
    },
    2: {
        "title": "Linear Regression",
        "filename": "02-linear-regression.html"
    },
    3: {
        "title": "Regularization",
        "filename": "03-regularization.html"
    },
    4: {
        "title": "Exploratory Data Analysis",
        "filename": "04-exploratory-data-analysis.html"
    },
    5: {
        "title": "Model Selection",
        "filename": "05-model-selection.html"
    },
    6: {
        "title": "Cross Validation",
        "filename": "06-cross-validation.html"
    },
    7: {
        "title": "PCA",
        "filename": "07-pca.html"
    },
    8: {
        "title": "Logistic Regression",
        "filename": "08-logistic-regression.html"
    },
    9: {
        "title": "Classification",
        "filename": "09-classification.html"
    },
    10: {
        "title": "Kernel Methods",
        "filename": "10-kernel-methods.html"
    },
    11: {
        "title": "Clustering",
        "filename": "11-clustering.html"
    },
    12: {
        "title": "Neural Networks",
        "filename": "12-neural-networks.html"
    },
    13: {
        "title": "Advanced Neural Networks",
        "filename": "13-advanced-neural-networks.html"
    },
}

def get_available_modules():
    """Dynamically discover available module templates"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    available = {}

    for module_num, module_info in MODULES.items():
        filename = module_info['filename']
        filepath = os.path.join(templates_dir, filename)

        if os.path.exists(filepath):
            available[module_num] = module_info

    return available

@app.route('/')
def index():
    available_modules = get_available_modules()

    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CMSC 173: Machine Learning</title>
        <style>
            body {
                font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #1B5E4F 0%, #2D4F47 50%, #7A1E3F 100%);
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 50px 40px;
                overflow: hidden;
            }
            h1 {
                color: #1B5E4F;
                text-align: center;
                font-size: 2.8em;
                margin-bottom: 10px;
                font-weight: 700;
            }
            .subtitle {
                text-align: center;
                color: #7A1E3F;
                margin-bottom: 40px;
                font-size: 1.2em;
                font-weight: 600;
                letter-spacing: 1px;
            }
            .modules-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
                margin: 40px 0;
            }
            .module-card {
                background: linear-gradient(135deg, #1B5E4F 0%, #7A1E3F 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                text-decoration: none;
                transition: all 0.3s ease;
                box-shadow: 0 6px 20px rgba(27, 94, 79, 0.2);
                border-top: 4px solid #D4AF37;
                position: relative;
                overflow: hidden;
            }
            .module-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="rgba(212,175,55,0.1)" stroke-width="1"/></svg>');
                opacity: 0.5;
            }
            .module-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 12px 35px rgba(27, 94, 79, 0.3);
            }
            .module-num {
                font-size: 0.95em;
                opacity: 0.9;
                margin-bottom: 8px;
                color: #D4AF37;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                position: relative;
                z-index: 1;
            }
            .module-title {
                font-size: 1.4em;
                font-weight: 600;
                position: relative;
                z-index: 1;
            }
            .status {
                text-align: center;
                color: #888;
                margin-top: 40px;
                padding-top: 30px;
                border-top: 2px solid #1B5E4F;
                font-size: 1em;
            }
            .status strong {
                color: #1B5E4F;
                font-size: 1.3em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>CMSC 173: Machine Learning</h1>
            <p class="subtitle">Interactive HTML Presentations</p>
            <div style="text-align: center; margin-bottom: 30px;">
                <a href="/group_portal" style="
                    background-color: #D4AF37;
                    color: white;
                    padding: 12px 25px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 1.1em;
                    transition: background-color 0.3s ease;
                ">Group Project Portal</a>
            </div>

            <div class="modules-grid">
    """

    for module_num in sorted(available_modules.keys()):
        module = available_modules[module_num]
        html += f'''
                <a href="/module/{module_num}" class="module-card">
                    <div class="module-num">Module {module_num}</div>
                    <div class="module-title">{module['title']}</div>
                </a>
        '''

    html += f"""
            </div>

            <div class="status">
                <p><strong>{len(available_modules)}</strong> of 14 modules available</p>
            </div>
        </div>
    </body>
    </html>
    """

    return html

@app.route('/module/<int:module_number>')
def show_module(module_number):
    available_modules = get_available_modules()

    if module_number not in available_modules:
        return f"""
        <html>
        <head>
            <title>Module Not Found</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 40px; background: #f0f0f0; }}
                .error {{ background: white; padding: 20px; border-radius: 8px; }}
                h1 {{ color: #d32f2f; }}
                a {{ color: #667eea; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>Module {module_number} Not Found</h1>
                <p>Available modules: {sorted(available_modules.keys())}</p>
                <p><a href="/">← Back to homepage</a></p>
                </div>
            </body>
            </html>
            """, 404

    # -- Supabase Integration --
    view_count = 0
    supabase_client = get_supabase_client()
    if supabase_client:
        try:
            # Increment view count
            supabase_client.rpc('increment_module_view', {'module_id': module_number}).execute()

            # Get view count
            response = supabase_client.table('module_views').select('view_count').eq('module_number', module_number).execute()
            if response.data:
                view_count = response.data[0]['view_count']
            logger.info(f"Module {module_number} view count: {view_count}")
        except Exception as e:
            logger.error(f"Error interacting with Supabase for module {module_number}: {e}", exc_info=True)
            view_count = 0  # Default to 0 instead of "Error" string
    # --------------------------

    module = available_modules[module_number]
    return render_template(module['filename'], view_count=view_count)

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve images from the images directory"""
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    return send_from_directory(images_dir, filename)

@app.route('/api/groups', methods=['POST'])
def create_group_api():
    supabase_client = get_supabase_client()
    if not supabase_client:
        logger.error("Supabase client not configured")
        return jsonify({"error": "Supabase not configured"}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        group_name = data.get('group_name', '').strip()
        project_title = data.get('project_title', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        class_id = data.get('class_id', '').strip() # Get class_id from request
        # Accept both 'member_ids' (new) and 'members' (backward compat)
        member_ids = data.get('member_ids', data.get('members', []))

        # Validate group_name
        is_valid, error_msg = validate_input(group_name, 100, "group_name")
        if not is_valid:
            logger.warning(f"Invalid group_name: {error_msg}")
            return jsonify({"error": error_msg}), 400

        # Validate project_title if provided
        if project_title:
            is_valid, error_msg = validate_input(project_title, 255, "project_title")
            if not is_valid:
                logger.warning(f"Invalid project_title: {error_msg}")
                return jsonify({"error": error_msg}), 400

        # Validate username
        if not username:
            return jsonify({"error": "Username is required"}), 400
        is_valid, error_msg = validate_input(username, 100, "username")
        if not is_valid:
            logger.warning(f"Invalid username: {error_msg}")
            return jsonify({"error": error_msg}), 400

        # Validate password
        if not password or len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        
        # Validate class_id (optional)
        if class_id:
            is_valid, error_msg = validate_input(class_id, 50, "class_id") # Assuming class_id is a short string like 'CMCS173A'
            if not is_valid:
                logger.warning(f"Invalid class_id: {error_msg}")
                return jsonify({"error": error_msg}), 400

        # Validate members list
        if not isinstance(member_ids, list):
            return jsonify({"error": "members must be a list"}), 400

        if len(member_ids) > 50:  # Reasonable limit
            return jsonify({"error": "Too many members (max 50)"}), 400

        # Create the group
        new_group = create_group(group_name, project_title, class_id) # Pass class_id here
        if new_group:
            group_id = new_group['id']
            logger.info(f"Created group {group_id} with name '{group_name}'")

            # Add members by student ID (update their group_id in the database)
            for student_id in member_ids:
                try:
                    # Assign student to group - this updates the student's group_id in the database
                    if assign_student_to_group(student_id, group_id):
                        logger.info(f"Assigned student {student_id} to group {group_id}")
                    else:
                        logger.warning(f"Failed to assign student {student_id} to group {group_id}")
                except Exception as e:
                    logger.warning(f"Error assigning student {student_id} to group: {e}")

            # Set group credentials (username and hashed password)
            password_hash = generate_password_hash(password)
            if update_group_credentials(group_id, username, password_hash):
                logger.info(f"Set credentials for group {group_id}")
                return jsonify(new_group), 201
            else:
                return jsonify({"error": "Failed to set group credentials"}), 500
        return jsonify({"error": "Failed to create group"}), 500
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error creating group: {e}", exc_info=True)

        # Check for duplicate username error
        if "duplicate key" in error_msg and "username" in error_msg:
            return jsonify({"error": "Username already exists. Please choose a different username."}), 400
        elif "23505" in error_msg:  # PostgreSQL unique violation code
            return jsonify({"error": "Username already taken. Please choose a different username."}), 400

        return jsonify({"error": "Failed to create group. Please try again."}), 500

@app.route('/api/groups', methods=['GET'])
def get_groups_api():
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Supabase not configured"}), 500
    try:
        groups = get_groups()
        return jsonify(groups), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<group_id>', methods=['GET'])
def get_group_details_api(group_id):
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Supabase not configured"}), 500
    try:
        group_details = get_group_with_submissions(group_id)
        if group_details:
            return jsonify(group_details), 200
        return jsonify({"error": "Group not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<group_id>', methods=['DELETE'])
def delete_group_api(group_id):
    # Require admin authentication
    if not is_admin_authenticated():
        logger.warning(f"Unauthorized group deletion attempt for group {group_id}")
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        logger.error("Supabase client not configured for group deletion")
        return jsonify({"error": "Supabase not configured"}), 500

    try:
        # Validate group_id format
        is_valid, error_msg = validate_input(group_id, 255, "group_id")
        if not is_valid:
            logger.warning(f"Invalid group_id for deletion: {error_msg}")
            return jsonify({"error": error_msg}), 400

        success = delete_group(group_id)
        if success:
            logger.info(f"Group {group_id} deleted successfully via API")
            return jsonify({"message": "Group deleted successfully"}), 200
        else:
            logger.warning(f"Failed to delete group {group_id}")
            return jsonify({"error": "Failed to delete group"}), 500
    except Exception as e:
        logger.error(f"Error deleting group {group_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<group_id>/documents', methods=['POST'])
def upload_document_api(group_id):
    supabase_client = get_supabase_client()
    if not supabase_client:
        logger.error("Supabase client not configured for document upload")
        return jsonify({"error": "Supabase not configured"}), 500

    try:
        # Validate group_id format
        is_valid, error_msg = validate_input(group_id, 255, "group_id")
        if not is_valid:
            logger.warning(f"Invalid group_id: {error_msg}")
            return jsonify({"error": error_msg}), 400

        if 'file' not in request.files:
            logger.warning("File upload attempt with no file part")
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Validate file size
        if request.content_length and request.content_length > MAX_FILE_SIZE:
            logger.warning(f"File size exceeds maximum: {request.content_length} > {MAX_FILE_SIZE}")
            return jsonify({"error": f"File size exceeds maximum of {MAX_FILE_SIZE // (1024*1024)} MB"}), 413

        # Validate file type
        if not allowed_file(file.filename, file.content_type):
            logger.warning(f"File type not allowed: {file.filename} ({file.content_type})")
            return jsonify({"error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

        document_title = request.form.get('document_title', '').strip() or file.filename

        # Validate document title
        is_valid, error_msg = validate_input(document_title, 255, "document_title")
        if not is_valid:
            logger.warning(f"Invalid document_title: {error_msg}")
            return jsonify({"error": error_msg}), 400

        # Store files locally in uploads directory
        # TODO: Consider migrating to cloud storage (Supabase Storage, S3)
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        # Use secure filename and add timestamp to prevent collisions
        import time
        secure_name = secure_filename(file.filename)
        filename = f"{int(time.time())}_{secure_name}"
        file_path = os.path.join(upload_folder, filename)

        # Ensure file_path is within upload_folder (path traversal prevention)
        real_path = os.path.realpath(file_path)
        real_upload_folder = os.path.realpath(upload_folder)
        if not real_path.startswith(real_upload_folder):
            logger.error(f"Path traversal attempt detected: {file_path}")
            return jsonify({"error": "Invalid file path"}), 400

        file.save(file_path)
        logger.info(f"File saved: {filename} for group {group_id}")

        try:
            new_document = add_group_document(group_id, document_title, file_path)
            if new_document:
                logger.info(f"Document metadata added for group {group_id}")
                return jsonify(new_document), 201
            return jsonify({"error": "Failed to add document metadata"}), 500
        except Exception as e:
            logger.error(f"Error adding document metadata: {e}", exc_info=True)
            # Clean up file if metadata insertion fails
            try:
                os.remove(file_path)
            except:
                pass
            return jsonify({"error": "Failed to process document"}), 500
    except Exception as e:
        logger.error(f"Error in file upload: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# --- Project Stages & Tracking Endpoints ---

@app.route('/api/groups/<group_id>/stages', methods=['GET'])
def get_stages_api(group_id):
    """Fetch all project stages for a group"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Supabase not configured"}), 500
    try:
        stages = get_project_stages(group_id)
        logger.info(f"Fetched {len(stages)} stages for group {group_id}")
        return jsonify(stages), 200
    except Exception as e:
        logger.error(f"Error fetching stages for group {group_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/stages/<stage_id>', methods=['PUT'])
def update_stage_api(stage_id):
    """Update project stage status, grade, and feedback"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Supabase not configured"}), 500
    try:
        data = request.get_json()
        status = data.get('status')
        grade = data.get('grade')
        feedback = data.get('feedback')

        if not status:
            return jsonify({"error": "Status is required"}), 400

        success = update_stage_status(stage_id, status, grade, feedback)
        if success:
            logger.info(f"Stage {stage_id} updated successfully")
            return jsonify({"message": "Stage updated successfully"}), 200
        return jsonify({"error": "Failed to update stage"}), 500
    except Exception as e:
        logger.error(f"Error updating stage {stage_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<group_id>/models', methods=['GET'])
def get_models_api(group_id):
    """Fetch all trained models for a group"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Supabase not configured"}), 500
    try:
        models = get_project_models(group_id)
        logger.info(f"Fetched {len(models)} models for group {group_id}")
        return jsonify(models), 200
    except Exception as e:
        logger.error(f"Error fetching models for group {group_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<group_id>/models', methods=['POST'])
def add_model_api(group_id):
    """Add a trained model result to the database"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Supabase not configured"}), 500
    try:
        data = request.get_json()
        model_name = data.get('model_name')
        model_type = data.get('model_type')
        metrics = {k: v for k, v in data.items() if k not in ['model_name', 'model_type']}

        if not model_name or not model_type:
            return jsonify({"error": "model_name and model_type are required"}), 400

        new_model = add_project_model(group_id, model_name, model_type, metrics)
        if new_model:
            logger.info(f"Model '{model_name}' added for group {group_id}")
            return jsonify(new_model), 201
        return jsonify({"error": "Failed to add model"}), 500
    except Exception as e:
        logger.error(f"Error adding model for group {group_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<group_id>/stage-documents', methods=['GET'])
def get_stage_docs_api(group_id):
    """Fetch documents for a specific stage or all stages"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Supabase not configured"}), 500
    try:
        stage_id = request.args.get('stage_id')
        documents = get_stage_documents(group_id, stage_id)
        logger.info(f"Fetched {len(documents)} stage documents for group {group_id}")
        return jsonify(documents), 200
    except Exception as e:
        logger.error(f"Error fetching stage documents for group {group_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/group_portal')
def group_portal():
    return render_template('group_portal_enhanced.html', is_admin=False)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            # Validate input
            if not username or not password:
                logger.warning("Login attempt with empty credentials")
                return render_template('admin_login.html', error='Username and password are required')

            admin_username = os.environ.get('ADMIN_USERNAME', '')
            admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH', '')

            if not admin_username or not admin_password_hash:
                logger.error("Admin credentials not properly configured")
                return render_template('admin_login.html', error='Server misconfiguration')

            # Verify password - try hash check first, then direct plaintext for debugging
            hash_check = check_password_hash(admin_password_hash, password)
            plaintext_check = password == os.environ.get('ADMIN_PASSWORD', '')

            if username == admin_username and (hash_check or plaintext_check):
                # Generate JWT token for serverless-compatible authentication
                token = generate_admin_token()

                # Create response with redirect
                response = redirect(url_for('admin_dashboard'))

                # Set JWT token in secure HTTP-only cookie
                response.set_cookie(
                    'admin_token',
                    token,
                    max_age=JWT_EXPIRATION_HOURS * 3600,
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                # Also set session for backwards compatibility
                session['logged_in'] = True
                session['is_admin'] = True

                logger.info(f"Admin login successful for user {username}")
                return response
            else:
                # Use generic message to prevent user enumeration
                logger.warning(f"Failed login attempt for user {username}")
                return render_template('admin_login.html', error='Invalid credentials')
        except Exception as e:
            logger.error(f"Error in admin login: {e}", exc_info=True)
            return render_template('admin_login.html', error='An error occurred during login')
    return render_template('admin_login.html')

@app.route('/admin_logout')
def admin_logout():
    """Logout admin user and clear session"""
    session.clear()
    logger.info("Admin user logged out")
    return redirect(url_for('group_portal'))

# --- ADMIN DASHBOARD & SUBMISSIONS ---

@app.route('/admin_dashboard')
def admin_dashboard():
    """Admin dashboard with statistics and overview"""
    if not is_admin_authenticated():
        logger.warning("Unauthorized access to admin dashboard")
        return redirect(url_for('admin_login'))

    return render_template('admin_dashboard.html')

@app.route('/admin_roster')
def admin_roster():
    """Admin student roster page."""
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    return render_template('admin_student_roster.html')

@app.route('/admin_submissions')
def admin_submissions():
    """Admin view to see all submissions by all groups"""
    if not is_admin_authenticated():
        logger.warning("Unauthorized access to admin submissions")
        return redirect(url_for('admin_login'))

    return render_template('admin_submissions.html')

@app.route('/api/admin/statistics', methods=['GET'])
def get_admin_statistics():
    """Get dashboard statistics for admin"""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Count total groups
        groups_response = supabase_client.table('groups').select('id', count='exact').execute()
        total_groups = groups_response.count

        # Count total submissions
        submissions_response = supabase_client.table('group_submissions').select('id', count='exact').execute()
        total_submissions = submissions_response.count

        # Count submissions by stage
        submissions_by_stage = {}
        for stage_num in range(1, 7):
            stage_response = supabase_client.table('group_submissions').select('id', count='exact').eq('stage_number', stage_num).execute()
            submissions_by_stage[f'stage_{stage_num}'] = stage_response.count

        # Calculate submission rate per stage
        submission_rates = {}
        for stage_num in range(1, 7):
            rate = (submissions_by_stage[f'stage_{stage_num}'] / total_groups * 100) if total_groups > 0 else 0
            submission_rates[f'stage_{stage_num}'] = round(rate, 1)

        # Get recent submissions (last 10)
        recent_submissions_query = supabase_client.table('group_submissions').select('*, groups(group_name, project_title)').order('submitted_at', desc=True).limit(10)
        recent_submissions = recent_submissions_query.execute()

        statistics = {
            'total_groups': total_groups,
            'total_submissions': total_submissions,
            'submissions_by_stage': submissions_by_stage,
            'submission_rates': submission_rates,
            'recent_submissions': recent_submissions.data,
            'average_submissions_per_group': round(total_submissions / total_groups, 1) if total_groups > 0 else 0
        }

        logger.info("Admin statistics fetched successfully")
        return jsonify(statistics), 200

    except Exception as e:
        logger.error(f"Error fetching admin statistics: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/submissions', methods=['GET'])
def get_all_submissions_admin():
    """Get all submissions with optional filters"""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Get query parameters for filtering
        group_id = request.args.get('group_id')
        stage_number = request.args.get('stage_number')

        # Build query
        query = supabase_client.table('group_submissions').select('*, groups(id, group_name, project_title)')

        # Apply filters
        if group_id:
            query = query.eq('group_id', group_id)
        if stage_number:
            query = query.eq('stage_number', int(stage_number))

        # Order by submission date (newest first)
        query = query.order('submitted_at', desc=True)

        response = query.execute()

        # Flatten the response data for the frontend
        flattened_submissions = []
        for submission in response.data:
            group_data = submission.get('groups', {})
            flattened_submission = {
                'id': submission.get('id'),
                'group_id': submission.get('group_id'),
                'group_name': group_data.get('group_name') if group_data else 'N/A',
                'project_title': group_data.get('project_title') if group_data else 'N/A',
                'stage': submission.get('stage_number'),
                'stage_number': submission.get('stage_number'),
                'file_name': submission.get('file_path', '').split('/')[-1] if submission.get('file_path') else 'N/A',
                'submitted_at': submission.get('submitted_at'),
                'file_size': submission.get('file_size'),
            }
            flattened_submissions.append(flattened_submission)

        logger.info(f"Fetched {len(flattened_submissions)} submissions for admin")
        return jsonify(flattened_submissions), 200

    except Exception as e:
        logger.error(f"Error fetching submissions: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/submissions/<submission_id>', methods=['GET'])
def get_submission_details_admin(submission_id):
    """Get detailed information about a specific submission"""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Validate submission_id
        is_valid, error_msg = validate_input(submission_id, 255, "submission_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Fetch submission with group details
        response = supabase_client.table('group_submissions').select(
            '*, groups(id, group_name, project_title, members:group_members(member_name))'
        ).eq('id', submission_id).execute()

        if not response.data or len(response.data) == 0:
            return jsonify({"error": "Submission not found"}), 404

        # Flatten the response data for the frontend
        submission_data = response.data[0]
        group_data = submission_data.get('groups', {})

        # Extract and structure the data
        flattened_data = {
            'id': submission_data.get('id'),
            'group_id': submission_data.get('group_id'),
            'group_name': group_data.get('group_name') if group_data else 'N/A',
            'project_title': group_data.get('project_title') if group_data else 'N/A',
            'members': [m.get('member_name', '') for m in (group_data.get('members', []) if group_data else [])],
            'stage': submission_data.get('stage_number'),
            'description': submission_data.get('content'),
            'file_name': submission_data.get('file_path', '').split('/')[-1] if submission_data.get('file_path') else 'N/A',
            'file_size': submission_data.get('file_size'),
            'submitted_at': submission_data.get('submitted_at'),
            'updated_at': submission_data.get('updated_at'),
        }

        logger.info(f"Fetched details for submission {submission_id}")
        return jsonify(flattened_data), 200

    except Exception as e:
        logger.error(f"Error fetching submission details: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/download/<submission_id>', methods=['GET'])
def download_submission_file(submission_id):
    """Download a submitted file"""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Validate submission_id
        is_valid, error_msg = validate_input(submission_id, 255, "submission_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Get submission
        response = supabase_client.table('group_submissions').select('file_path, file_name').eq('id', submission_id).execute()

        if not response.data or len(response.data) == 0 or not response.data[0].get('file_path'):
            return jsonify({"error": "File not found"}), 404

        file_path = response.data[0]['file_path']
        file_name = response.data[0]['file_name']

        # Verify file exists and is in uploads directory
        if not os.path.exists(file_path):
            logger.error(f"File not found on disk: {file_path}")
            return jsonify({"error": "File not found on server"}), 404

        # Security check: ensure file is within uploads directory
        real_path = os.path.realpath(file_path)
        real_upload_folder = os.path.realpath(UPLOAD_FOLDER)
        if not real_path.startswith(real_upload_folder):
            logger.error(f"Path traversal attempt detected: {file_path}")
            return jsonify({"error": "Invalid file path"}), 400

        # Serve file
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        logger.info(f"Serving file {file_name} for submission {submission_id}")
        return send_from_directory(directory, filename, as_attachment=True, download_name=file_name)

    except Exception as e:
        logger.error(f"Error downloading file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/view/<submission_id>', methods=['GET'])
def view_submission_file(submission_id):
    """View a submitted file in browser (for PDFs)"""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Validate submission_id
        is_valid, error_msg = validate_input(submission_id, 255, "submission_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Get submission
        response = supabase_client.table('group_submissions').select('file_path, file_name').eq('id', submission_id).execute()

        if not response.data or len(response.data) == 0 or not response.data[0].get('file_path'):
            return jsonify({"error": "File not found"}), 404

        file_path = response.data[0]['file_path']

        # Security check
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found on server"}), 404

        real_path = os.path.realpath(file_path)
        real_upload_folder = os.path.realpath(UPLOAD_FOLDER)
        if not real_path.startswith(real_upload_folder):
            logger.error(f"Path traversal attempt detected: {file_path}")
            return jsonify({"error": "Invalid file path"}), 400

        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        logger.info(f"Viewing file for submission {submission_id}")
        return send_from_directory(directory, filename, as_attachment=False)

    except Exception as e:
        logger.error(f"Error viewing file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/groups/submission-status', methods=['GET'])
def get_groups_submission_status():
    """Get all groups with their submission status for each stage"""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Get all groups
        groups_response = supabase_client.table('groups').select('id, group_name, project_title').execute()

        if not groups_response.data:
            return jsonify([]), 200

        groups_data = []

        # For each group, get submission status for each stage
        for group in groups_response.data:
            group_id = group['id']
            group_name = group.get('group_name', 'N/A')
            project_title = group.get('project_title', 'N/A')

            # Get submissions for this group
            submissions_response = supabase_client.table('group_submissions').select('stage_number').eq('group_id', group_id).execute()

            # Create a set of stages that have submissions
            submitted_stages = set()
            if submissions_response.data:
                for submission in submissions_response.data:
                    stage_num = submission.get('stage_number')
                    if stage_num:
                        submitted_stages.add(stage_num)

            # Build the group status object
            group_status = {
                'id': group_id,
                'group_name': group_name,
                'project_title': project_title,
                'stages': {
                    'stage_1': 1 in submitted_stages,
                    'stage_2': 2 in submitted_stages,
                    'stage_3': 3 in submitted_stages,
                    'stage_4': 4 in submitted_stages,
                    'stage_5': 5 in submitted_stages,
                    'stage_6': 6 in submitted_stages,
                }
            }
            groups_data.append(group_status)

        logger.info(f"Fetched submission status for {len(groups_data)} groups")
        return jsonify(groups_data), 200

    except Exception as e:
        logger.error(f"Error fetching groups submission status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# --- GROUP AUTHENTICATION & PORTAL ---

@app.route('/group_login', methods=['GET', 'POST'])
def group_login():
    """Group login page"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not username or not password:
                return render_template('group_login.html', error='Username and password are required')

            # Get group by username
            group = get_group_by_username(username)
            if not group:
                logger.warning(f"Login attempt with non-existent username: {username}")
                return render_template('group_login.html', error='Invalid username or password')

            # Verify password
            if not check_password_hash(group.get('password_hash', ''), password):
                logger.warning(f"Failed login attempt for group username {username}")
                return render_template('group_login.html', error='Invalid username or password')

            # Set session
            session['group_id'] = group['id']
            session['group_name'] = group['group_name']
            session['is_group_logged_in'] = True

            # Update last login
            update_group_last_login(group['id'])

            logger.info(f"Group login successful for {username}")
            return redirect(url_for('group_submission_portal'))

        except Exception as e:
            logger.error(f"Error in group login: {e}", exc_info=True)
            return render_template('group_login.html', error='An error occurred')

    return render_template('group_login.html')

@app.route('/group_submission_portal')
def group_submission_portal():
    """Group project portal (submission interface)"""
    if not session.get('is_group_logged_in'):
        logger.warning("Unauthorized access to group submission portal")
        return redirect(url_for('group_login'))

    group_id = session.get('group_id')
    try:
        group = get_group_with_submissions(group_id)
        if not group:
            return render_template('group_submission_portal.html', error='Group not found')

        return render_template('group_submission_portal.html', group=group, group_name=session.get('group_name'))
    except Exception as e:
        logger.error(f"Error loading group submission portal: {e}", exc_info=True)
        return render_template('group_submission_portal.html', error='An error occurred')

@app.route('/admin/group/<group_id>')
def admin_view_group(group_id):
    """Admin view of a specific group's submissions and portal (admin only)"""
    if not is_admin_authenticated():
        logger.warning("Unauthorized access to admin group view")
        return redirect(url_for('group_login'))

    try:
        group = get_group_with_submissions(group_id)
        if not group:
            return render_template('group_submission_portal.html', error='Group not found')

        # Render the same submission portal template but for admin viewing
        return render_template('group_submission_portal.html', group=group, group_name=group.get('group_name'), is_admin_view=True)
    except Exception as e:
        logger.error(f"Error loading admin group view: {e}", exc_info=True)
        return render_template('group_submission_portal.html', error='An error occurred')

@app.route('/group_logout')
def group_logout():
    """Logout group"""
    session.clear()
    logger.info("Group logged out")
    return redirect(url_for('group_login'))

# --- SUBMISSION ENDPOINTS ---

@app.route('/api/student/submit', methods=['POST'])
def submit_work_api():
    """Submit work for a project stage"""
    if not session.get('is_student'):
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        student_id = session.get('student_id')
        data = request.get_json()
        group_id = data.get('group_id')
        stage_id = data.get('stage_id')
        content = data.get('content')

        if not all([group_id, stage_id]):
            return jsonify({"error": "group_id and stage_id are required"}), 400

        # Verify student is in the group
        student = get_student_by_id(student_id)
        if not student or student.get('group_id') != group_id:
            logger.warning(f"Student {student_id} attempted to submit for unauthorized group {group_id}")
            return jsonify({"error": "Unauthorized"}), 403

        # Submit work
        submission = submit_stage_work(group_id, stage_id, student_id, content)
        if submission:
            logger.info(f"Work submitted by student {student_id} for stage {stage_id}")
            return jsonify(submission), 201
        else:
            return jsonify({"error": "Failed to submit work"}), 500

    except Exception as e:
        logger.error(f"Error submitting work: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/student/submissions', methods=['GET'])
def get_student_submissions():
    """Get all submissions for student's group"""
    if not session.get('is_student'):
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        student_id = session.get('student_id')
        student = get_student_by_id(student_id)
        if not student or not student.get('group_id'):
            return jsonify({"error": "Not assigned to a group"}), 404

        submissions = get_group_submissions(student['group_id'])
        logger.info(f"Retrieved {len(submissions)} submissions for student {student_id}")
        return jsonify(submissions), 200

    except Exception as e:
        logger.error(f"Error getting submissions: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/student/submit-file/<stage_id>', methods=['POST'])
def submit_file_api(stage_id):
    """Submit a file for a project stage"""
    if not session.get('is_student'):
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        student_id = session.get('student_id')
        student = get_student_by_id(student_id)
        if not student or not student.get('group_id'):
            return jsonify({"error": "Not assigned to a group"}), 403

        group_id = student['group_id']

        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename, file.content_type):
            logger.warning(f"Invalid file type submitted: {file.content_type}")
            return jsonify({"error": "File type not allowed"}), 400

        # Save file
        filename = secure_filename(f"{group_id}_{stage_id}_{int(os.times()[4])}_{file.filename}")
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(upload_path)

        # Submit work with file reference
        submission = submit_stage_work(group_id, stage_id, student_id, file_path=upload_path, file_name=filename)
        if submission:
            logger.info(f"File submitted by student {student_id} for stage {stage_id}")
            return jsonify(submission), 201
        else:
            return jsonify({"error": "Failed to record submission"}), 500

    except Exception as e:
        logger.error(f"Error submitting file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# --- GROUP SUBMISSION ENDPOINTS ---

def get_stage_id_by_number(stage_number: int) -> str:
    """Get stage UUID by stage number"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return None
    try:
        response = supabase_client.table('project_stages').select('id').eq('stage_number', stage_number).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]['id']
        return None
    except Exception as e:
        logger.error(f"Error getting stage ID: {e}")
        return None

@app.route('/api/group/submit', methods=['POST'])
def group_submit_api():
    """Submit work for a group project stage"""
    if not session.get('is_group_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        group_id = session.get('group_id')

        # Handle submission - file is optional, presentation link and summary are required
        stage_number = request.form.get('stage_number', type=int)
        summary_markdown = request.form.get('summary_markdown', '').strip()
        content = request.form.get('content', '')
        presentation_link = request.form.get('presentation_link', '').strip()
        file = request.files.get('file') if request.files else None

        # Validate stage number
        if not stage_number or stage_number < 1 or stage_number > 6:
            return jsonify({"error": "Invalid stage number"}), 400

        # Validate presentation link (required)
        if not presentation_link:
            return jsonify({"error": "Presentation link is required"}), 400

        # Validate summary markdown (required)
        if not summary_markdown:
            return jsonify({"error": "Summary is required"}), 400

        # Process file if provided (optional)
        submission_data = {
            'stage_number': stage_number,
            'summary_markdown': summary_markdown if summary_markdown else '',
            'content': content if content else '',
            'presentation_link': presentation_link
        }

        if file and file.filename != '':
            # Validate file
            if not allowed_file(file.filename, file.content_type):
                logger.warning(f"Invalid file type submitted: {file.content_type}")
                return jsonify({"error": "File type not allowed"}), 400

            if file.content_length and file.content_length > MAX_FILE_SIZE:
                return jsonify({"error": "File too large (max 50MB)"}), 413

            # Process file for storage
            filename = secure_filename(f"group_{group_id}_stage_{stage_number}_{file.filename}")
            file_upload_result = upload_submission_file(
                file,
                group_id,
                stage_number,
                filename
            )

            if not file_upload_result:
                logger.error(f"Failed to process file for group {group_id}")
                return jsonify({"error": "Failed to process file for submission"}), 500

            # Add file information to submission data
            submission_data['file_path'] = file_upload_result.get('file_path')
            submission_data['file_name'] = file_upload_result.get('filename')
            submission_data['file_size'] = file_upload_result.get('size')
            submission_data['file_mime_type'] = file.content_type

        # Submit work
        submission = submit_group_stage_work(
            group_id,
            None,  # stage_id - not needed, we use stage_number in submission_data
            submission_data
        )
        if submission:
            logger.info(f"Submission recorded for group {group_id} stage {stage_number}")
            return jsonify(submission), 201
        else:
            logger.error(f"Failed to record submission for group {group_id} stage {stage_number}")
            return jsonify({"error": "Failed to record submission"}), 500

    except Exception as e:
        logger.error(f"Error submitting group work: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# --- STUDENT MANAGEMENT API ---

@app.route('/api/students/class/<class_id>', methods=['GET'])
def get_students_by_class_api(class_id):
    """Get all students in a class."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        students = get_students_by_class(class_id)
        return jsonify(students), 200
    except Exception as e:
        logger.error(f"Error getting students: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/ungrouped/all', methods=['GET'])
def get_all_ungrouped_students_api():
    """Get all ungrouped students across all classes."""
    try:
        supabase_client = get_supabase_client()
        if not supabase_client:
            return jsonify({"error": "Database not configured"}), 500

        # Get all ungrouped students
        response = supabase_client.table('students').select('*').is_('group_id', 'null').order('last_name').execute()
        students = response.data

        # Return safe student data
        safe_students = []
        for student in students:
            safe_students.append({
                'id': student['id'],
                'first_name': student.get('first_name', ''),
                'last_name': student.get('last_name', ''),
                'campus_id': student.get('campus_id', ''),
                'program': student.get('program', ''),
                'class_id': student.get('class_id', '')
            })

        return jsonify(safe_students), 200
    except Exception as e:
        logger.error(f"Error getting all ungrouped students: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/ungrouped/<class_id>', methods=['GET'])
def get_ungrouped_students_api(class_id):
    """Get ungrouped students in a class."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        students = get_ungrouped_students(class_id)
        return jsonify(students), 200
    except Exception as e:
        logger.error(f"Error getting ungrouped students: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/grouped/<class_id>', methods=['GET'])
def get_grouped_students_api(class_id):
    """Get grouped students in a class."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        students = get_grouped_students(class_id)
        return jsonify(students), 200
    except Exception as e:
        logger.error(f"Error getting grouped students: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/campus/<campus_id>', methods=['GET'])
def get_student_api(campus_id):
    """Get student by campus ID."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        student = get_student_by_campus_id(campus_id)
        if student:
            return jsonify(student), 200
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        logger.error(f"Error getting student: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/<student_id>/assign-group/<group_id>', methods=['POST'])
def assign_student_to_group_api(student_id, group_id):
    """Assign a student to a group."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        success = assign_student_to_group(student_id, group_id)
        if success:
            logger.info(f"Assigned student {student_id} to group {group_id}")
            return jsonify({"success": True}), 200
        return jsonify({"error": "Failed to assign student"}), 500
    except Exception as e:
        logger.error(f"Error assigning student: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/<student_id>/unassign-group', methods=['POST'])
def unassign_student_api(student_id):
    """Remove a student from their group."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        success = unassign_student_from_group(student_id)
        if success:
            logger.info(f"Unassigned student {student_id} from group")
            return jsonify({"success": True}), 200
        return jsonify({"error": "Failed to unassign student"}), 500
    except Exception as e:
        logger.error(f"Error unassigning student: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/group/members/ungrouped', methods=['GET'])
def get_ungrouped_group_members_api():
    """Get ungrouped students from the group's class for group members to add."""
    if not session.get('is_group_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    group_id = session.get('group_id')
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Get group details to find its class_id
        group_details = get_group_details(group_id) # This now fetches class_id
        if not group_details or not group_details.get('class_id'):
            return jsonify({"error": "Could not determine group's class"}), 400

        class_id = group_details['class_id']
        ungrouped_students = get_ungrouped_students(class_id)
        
        # Filter out sensitive data from student objects before sending to frontend
        safe_students = []
        for student in ungrouped_students:
            safe_students.append({
                'id': student['id'],
                'first_name': student.get('first_name', ''),
                'last_name': student.get('last_name', ''),
                'campus_id': student.get('campus_id', '')
            })
        return jsonify(safe_students), 200
    except Exception as e:
        logger.error(f"Error getting ungrouped students for group {group_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/group/members/available', methods=['GET'])
def get_available_students_for_group_api():
    """Get ungrouped students excluding those already in the group."""
    if not session.get('is_group_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    group_id = session.get('group_id')
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Get all ungrouped students
        all_ungrouped = supabase_client.table('students').select('*').is_('group_id', 'null').order('last_name').execute()
        ungrouped_students = all_ungrouped.data if all_ungrouped.data else []

        # Get current group members
        group_members = supabase_client.table('group_members').select('student_id').eq('group_id', group_id).execute()
        member_ids = {m['student_id'] for m in (group_members.data if group_members.data else [])}

        # Filter out students already in this group
        available_students = [
            {
                'id': student['id'],
                'first_name': student.get('first_name', ''),
                'last_name': student.get('last_name', ''),
                'campus_id': student.get('campus_id', ''),
                'program': student.get('program', ''),
                'class_id': student.get('class_id', '')
            }
            for student in ungrouped_students
            if student['id'] not in member_ids
        ]

        logger.info(f"Group {group_id}: Found {len(ungrouped_students)} ungrouped, {len(member_ids)} group members, returning {len(available_students)} available")
        return jsonify(available_students), 200
    except Exception as e:
        logger.error(f"Error getting available students for group: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/group/members/add', methods=['POST'])
def add_group_member_api():
    """Add a student to the current group (for group members)."""
    if not session.get('is_group_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    group_id = session.get('group_id')
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        data = request.get_json()
        student_id = data.get('student_id')

        # Validate student_id
        is_valid, error_msg = validate_input(student_id, 255, "student_id")
        if not is_valid:
            logger.warning(f"Invalid student_id for adding to group: {error_msg}")
            return jsonify({"error": error_msg}), 400

        success = assign_student_to_group(group_id, student_id)
        if success:
            logger.info(f"Student {student_id} successfully added to group {group_id}")
            return jsonify({"success": True, "message": "Student added successfully"}), 200
        else:
            # Check why the assignment failed - most likely student already in a group
            logger.warning(f"assign_student_to_group returned False for student {student_id} and group {group_id}")
            try:
                # Use regular query (no .single()) to get list of students
                student_response = supabase_client.table('students').select('group_id, first_name, last_name').eq('id', student_id).execute()
                logger.info(f"Student response: {student_response.data}")
                if student_response.data and len(student_response.data) > 0:
                    student_data = student_response.data[0]
                    if student_data.get('group_id') is not None:
                        error_msg = f"Student {student_data.get('first_name', '')} {student_data.get('last_name', '')} is already in another group"
                        logger.warning(f"Failed to add student {student_id} to group {group_id}: {error_msg}")
                        return jsonify({"error": error_msg}), 400
                    else:
                        logger.warning(f"Student {student_id} exists but assignment failed for unknown reason")
                else:
                    logger.warning(f"Student {student_id} not found in database")
                    return jsonify({"error": "Student not found"}), 404
            except Exception as e:
                logger.error(f"Error checking student status: {e}", exc_info=True)

            logger.warning(f"Failed to add student {student_id} to group {group_id} - unknown reason")
            return jsonify({"error": "Failed to add student to group"}), 500
    except Exception as e:
        logger.error(f"Error adding student to group {group_id}: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<group_id>/members', methods=['GET'])
def get_group_members_api(group_id):
    """Get all members of a group."""
    try:
        members = get_group_members(group_id)
        return jsonify(members), 200
    except Exception as e:
        logger.error(f"Error getting group members: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<group_id>/comments', methods=['GET'])
def get_group_comments(group_id):
    """Get admin comments for a group."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Validate group_id
        is_valid, error_msg = validate_input(group_id, 255, "group_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Fetch comments from group_comments table
        response = supabase_client.table('group_comments').select('*').eq('group_id', group_id).order('created_at', desc=True).execute()

        logger.info(f"Fetched {len(response.data)} comments for group {group_id}")
        return jsonify(response.data), 200

    except Exception as e:
        logger.error(f"Error fetching group comments: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<group_id>/comments', methods=['POST'])
def add_group_comment(group_id):
    """Add a comment to a group (admin only)."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Validate group_id
        is_valid, error_msg = validate_input(group_id, 255, "group_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        data = request.get_json()
        comment_text = data.get('comment_text', '').strip()

        if not comment_text:
            return jsonify({"error": "Comment text is required"}), 400

        # Validate comment text
        is_valid, error_msg = validate_input(comment_text, 5000, "comment_text")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Insert comment
        comment_data = {
            'group_id': group_id,
            'admin_name': session.get('admin_username', 'Admin'),
            'comment_text': comment_text,
            'created_at': datetime.now(timezone.utc).isoformat(),
        }

        response = supabase_client.table('group_comments').insert([comment_data]).execute()

        logger.info(f"Added comment to group {group_id}")
        return jsonify(response.data[0] if response.data else comment_data), 201

    except Exception as e:
        logger.error(f"Error adding group comment: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/classes/cmsc173a', methods=['GET'])
def get_cmsc173a_class_api():
    """Get CMSC173 Section A class info and students."""
    try:
        print("DEBUG: Starting CMSC173A query")
        from supabase_client import get_supabase_client
        client = get_supabase_client()
        print(f"DEBUG: Supabase client available: {client is not None}")

        cmsc_class = get_class_by_code_section('CMSC173', 'A')
        print(f"DEBUG: get_class_by_code_section returned: {cmsc_class}")

        if not cmsc_class:
            # Debug: Check if Supabase client is available
            debug_info = {
                "error": "Class not found",
                "supabase_client_available": client is not None
            }
            logger.warning(f"Class not found. Supabase client available: {client is not None}")
            return jsonify(debug_info), 404

        all_students = get_students_by_class(cmsc_class['id'])
        ungrouped = get_ungrouped_students(cmsc_class['id'])
        grouped = get_grouped_students(cmsc_class['id'])

        return jsonify({
            "class": cmsc_class,
            "total_students": len(all_students),
            "ungrouped_count": len(ungrouped),
            "grouped_count": len(grouped),
            "ungrouped_students": ungrouped,
            "grouped_students": grouped
        }), 200
    except Exception as e:
        logger.error(f"Error getting CMSC173A class: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/classes/cmsc173d', methods=['GET'])
def get_cmsc173d_class_api():
    """Get CMSC173 Section D class info and students."""
    try:
        cmsc_class = get_class_by_code_section('CMSC173', 'D')
        if not cmsc_class:
            return jsonify({"error": "Class not found"}), 404

        all_students = get_students_by_class(cmsc_class['id'])
        ungrouped = get_ungrouped_students(cmsc_class['id'])
        grouped = get_grouped_students(cmsc_class['id'])

        return jsonify({
            "class": cmsc_class,
            "total_students": len(all_students),
            "ungrouped_count": len(ungrouped),
            "grouped_count": len(grouped),
            "ungrouped_students": ungrouped,
            "grouped_students": grouped
        }), 200
    except Exception as e:
        logger.error(f"Error getting CMSC173D class: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/classes/cmsc173e', methods=['GET'])
def get_cmsc173e_class_api():
    """Get CMSC173 Section E class info and students."""
    try:
        cmsc_class = get_class_by_code_section('CMSC173', 'E')
        if not cmsc_class:
            return jsonify({"error": "Class not found"}), 404

        all_students = get_students_by_class(cmsc_class['id'])
        ungrouped = get_ungrouped_students(cmsc_class['id'])
        grouped = get_grouped_students(cmsc_class['id'])

        return jsonify({
            "class": cmsc_class,
            "total_students": len(all_students),
            "ungrouped_count": len(ungrouped),
            "grouped_count": len(grouped),
            "ungrouped_students": ungrouped,
            "grouped_students": grouped
        }), 200
    except Exception as e:
        logger.error(f"Error getting CMSC173E class: {e}")
        return jsonify({"error": str(e)}), 500

# --- ADMIN SUBMISSION SCORING ENDPOINTS ---

@app.route('/api/admin/submissions/<submission_id>/score', methods=['POST'])
def save_submission_score(submission_id):
    """Save a score for a submission."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json or request.form.to_dict()
        score = float(data.get('score', 0))
        max_score = float(data.get('max_score', 100))
        feedback = data.get('feedback', '')
        admin_notes = data.get('admin_notes', '')

        result = supabase_client.save_submission_score(
            submission_id=submission_id,
            score=score,
            max_score=max_score,
            feedback=feedback,
            admin_notes=admin_notes
        )

        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Failed to save score"}), 500
    except ValueError:
        return jsonify({"error": "Invalid score value"}), 400
    except Exception as e:
        logger.error(f"Error saving submission score: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/submissions/<submission_id>/score', methods=['GET'])
def get_submission_score(submission_id):
    """Get the score for a submission."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        score = supabase_client.get_submission_score(submission_id)
        if score:
            return jsonify(score), 200
        else:
            return jsonify({"message": "No score found"}), 404
    except Exception as e:
        logger.error(f"Error getting submission score: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/groups/submissions-grid', methods=['GET'])
def get_groups_submissions_grid():
    """Get all groups with their submission statuses organized for dashboard grid view."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        groups = supabase_client.get_all_groups_with_submissions()
        return jsonify(groups), 200
    except Exception as e:
        logger.error(f"Error getting groups submissions grid: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/groups/<group_id>/submissions-dashboard', methods=['GET'])
def get_group_submissions_dashboard(group_id):
    """Get a group's submissions organized by stage for dashboard display."""
    if not is_admin_authenticated():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        group_data = supabase_client.get_group_submissions_for_dashboard(group_id)
        if group_data:
            return jsonify(group_data), 200
        else:
            return jsonify({"error": "Group not found"}), 404
    except Exception as e:
        logger.error(f"Error getting group submissions dashboard: {e}")
        return jsonify({"error": str(e)}), 500

# --- SUBMISSION FILE DOWNLOADS ---

@app.route('/api/submissions/<submission_id>/download/summary', methods=['GET'])
def download_submission_summary(submission_id):
    """Download the summary document (file_name) from a submission"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Validate submission_id
        is_valid, error_msg = validate_input(submission_id, 255, "submission_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Get submission with file info
        response = supabase_client.table('group_submissions').select('id, file_path, file_name, group_id').eq('id', submission_id).execute()

        if not response.data or len(response.data) == 0:
            logger.warning(f"Submission not found: {submission_id}")
            return jsonify({"error": "Submission not found"}), 404

        submission = response.data[0]
        file_path = submission.get('file_path')
        file_name = submission.get('file_name')

        if not file_path:
            logger.warning(f"No file found in submission: {submission_id}")
            return jsonify({"error": "No file available for download"}), 404

        # Verify file exists on disk
        if not os.path.exists(file_path):
            logger.error(f"File not found on disk: {file_path}")
            return jsonify({"error": "File not found on server"}), 404

        # Security check: ensure file is within uploads directory
        real_path = os.path.realpath(file_path)
        real_upload_folder = os.path.realpath(UPLOAD_FOLDER)
        if not real_path.startswith(real_upload_folder):
            logger.error(f"Path traversal attempt detected: {file_path}")
            return jsonify({"error": "Invalid file path"}), 400

        # Serve file
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        logger.info(f"Downloading summary file {file_name} for submission {submission_id}")
        return send_from_directory(directory, filename, as_attachment=True, download_name=file_name or filename)

    except Exception as e:
        logger.error(f"Error downloading summary file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/submissions/<submission_id>/download/presentation', methods=['GET'])
def download_submission_presentation(submission_id):
    """Download the presentation file from a submission"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Validate submission_id
        is_valid, error_msg = validate_input(submission_id, 255, "submission_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Get submission with presentation file info
        # Use * to select all columns and handle missing columns gracefully
        response = supabase_client.table('group_submissions').select('id, group_id').eq('id', submission_id).execute()

        if not response.data or len(response.data) == 0:
            logger.warning(f"Submission not found: {submission_id}")
            return jsonify({"error": "Submission not found"}), 404

        submission = response.data[0]

        # Try to get presentation file info from the full submission record
        # Check if presentation_path or presentation_file columns exist
        response_full = supabase_client.table('group_submissions').select('*').eq('id', submission_id).execute()
        if response_full.data:
            submission = response_full.data[0]
            file_path = submission.get('presentation_path')
            file_name = submission.get('presentation_file')
        else:
            file_path = None
            file_name = None

        # If presentation_path doesn't exist, try to construct it from presentation_file
        if not file_path and file_name:
            # Try to find the file in uploads with the given filename
            possible_path = os.path.join(UPLOAD_FOLDER, secure_filename(file_name))
            if os.path.exists(possible_path):
                file_path = possible_path
            else:
                logger.warning(f"Presentation file path not found for submission: {submission_id}")
                return jsonify({"error": "Presentation file not available"}), 404

        if not file_path:
            logger.warning(f"No presentation file found in submission: {submission_id}")
            return jsonify({"error": "Presentation file not available for download"}), 404

        # Verify file exists on disk
        if not os.path.exists(file_path):
            logger.error(f"Presentation file not found on disk: {file_path}")
            return jsonify({"error": "File not found on server"}), 404

        # Security check: ensure file is within uploads directory
        real_path = os.path.realpath(file_path)
        real_upload_folder = os.path.realpath(UPLOAD_FOLDER)
        if not real_path.startswith(real_upload_folder):
            logger.error(f"Path traversal attempt detected: {file_path}")
            return jsonify({"error": "Invalid file path"}), 400

        # Serve file
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        logger.info(f"Downloading presentation file {file_name} for submission {submission_id}")
        return send_from_directory(directory, filename, as_attachment=True, download_name=file_name or filename)

    except Exception as e:
        logger.error(f"Error downloading presentation file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8788)