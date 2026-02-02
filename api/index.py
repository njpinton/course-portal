from flask import Flask, render_template, send_from_directory, send_file, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os
import json
import csv
import logging
import sys
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

# Add the API directory and parent directory to the Python path for Vercel compatibility
import os.path
api_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(api_dir)  # Parent directory (project root)

if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Load environment variables early for Vercel compatibility
from dotenv import load_dotenv
if os.path.exists('.env.local'):
    load_dotenv('.env.local')
load_dotenv('.env')

# Import from organized modules
from .config import (
    MAX_FILE_SIZE, ALLOWED_EXTENSIONS, UPLOAD_FOLDER, MODULES,
    JWT_EXPIRATION_HOURS, COURSES, PROJECTS, MODULE_CATEGORIES, COURSE_PROJECTS
)
from .utils.validation import allowed_file, validate_input
from .utils.auth import (
    generate_admin_token, admin_required, admin_page_required
)

# Configure logging early for import debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    logger.debug("Attempting to import supabase_client...")
    from api.utils.supabase_client import (
        get_supabase_client, create_group, add_group_member, add_group_document,
        get_groups, get_group_details, delete_group, get_project_stages,
        update_stage_status, get_project_models, add_project_model,
        get_stage_documents, add_stage_document, update_group_project_info,
        update_group_credentials, get_group_by_username, update_group_last_login,
        get_group_with_submissions, submit_group_stage_work, get_group_feedback,
        get_class_by_code_section, get_class_by_id, get_students_by_class, get_ungrouped_students,
        get_grouped_students, assign_student_to_group, get_student_by_campus_id, get_student_by_id,
        get_group_members, unassign_student_from_group,
        upload_submission_file, get_submission_file_url, delete_submission_file,
        submit_stage_work, get_group_submissions,
        # Course Resources
        get_course_resources, get_resource_by_id, create_resource,
        update_resource, delete_resource, reorder_resources, get_resource_counts_by_course,
        # Class Records
        get_all_classes, get_class_records, update_student_exam_status, bulk_update_exam_status,
        # Assessments
        get_assessments_by_class, create_assessment, update_assessment, delete_assessment,
        get_grades_by_assessment, get_student_grades_for_class, upsert_student_grade,
        bulk_upsert_grades, get_assessment_stats
    )
    logger.debug("Successfully imported supabase_client")
except Exception as e:
    logger.warning(f"Failed to import supabase_client: {e}", exc_info=True)
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
    def submit_stage_work(*args, **kwargs):
        return None
    def get_group_submissions(*args, **kwargs):
        return []
    def get_course_resources(*args, **kwargs):
        return []
    def get_resource_by_id(*args, **kwargs):
        return None
    def create_resource(*args, **kwargs):
        return None
    def update_resource(*args, **kwargs):
        return None
    def delete_resource(*args, **kwargs):
        return False
    def reorder_resources(*args, **kwargs):
        return False
    def get_resource_counts_by_course(*args, **kwargs):
        return {}

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

app = Flask(__name__, static_folder='../static', static_url_path='/static')

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================

# Secret key management - REQUIRED in production
is_production = os.environ.get('VERCEL_ENV') == 'production'
secret_key = os.environ.get('FLASK_SECRET_KEY')

if not secret_key:
    if is_production:
        # FAIL FAST: Production MUST have a proper secret key
        logger.critical("FLASK_SECRET_KEY environment variable is required in production!")
        raise RuntimeError("FLASK_SECRET_KEY environment variable must be set in production. "
                          "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
    else:
        # For local development only, generate a temporary key
        import secrets
        secret_key = secrets.token_urlsafe(32)
        logger.warning("Generated temporary FLASK_SECRET_KEY for development. "
                      "Set FLASK_SECRET_KEY environment variable for production.")

app.secret_key = secret_key

# Secure session cookie configuration
app.config.update(
    SESSION_COOKIE_SECURE=is_production,  # HTTPS only in production
    SESSION_COOKIE_HTTPONLY=True,         # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE='Lax',        # CSRF protection
    PERMANENT_SESSION_LIFETIME=86400,     # 24 hours
    WTF_CSRF_ENABLED=True,                # Enable CSRF protection
    WTF_CSRF_TIME_LIMIT=3600,             # CSRF token valid for 1 hour
)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Exempt API endpoints from CSRF (they use JWT/session auth instead)
# CSRF is primarily for form submissions from browsers
# Routes defined directly on app (not in blueprints)
csrf.exempt('create_group_api')
csrf.exempt('get_groups_api')
csrf.exempt('get_group_details_api')
csrf.exempt('delete_group_api')
csrf.exempt('group_login')
csrf.exempt('group_submit_api')  # Group submission endpoint
csrf.exempt('update_submission_api')  # Edit submission endpoint
csrf.exempt('upload_document_api')
csrf.exempt('update_student_exam_api')  # Class records exam status
csrf.exempt('bulk_update_exam_api')  # Class records bulk update

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Security headers via Flask-Talisman
# Configure CSP to allow inline styles/scripts for the presentation templates
csp = {
    'default-src': "'self'",
    'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
    'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
    'font-src': ["'self'", "https://fonts.gstatic.com", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
    'img-src': ["'self'", "data:", "https:", "blob:"],
    'connect-src': ["'self'", "https://*.supabase.co", "wss://*.supabase.co"],
    'frame-src': ["'self'", "https://www.youtube.com", "https://youtube.com"],
    'media-src': ["'self'", "https:"],
}

# Only enable Talisman in production (it forces HTTPS which breaks local dev)
if is_production:
    Talisman(
        app,
        force_https=True,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,  # 1 year
        content_security_policy=csp,
        # Note: nonce requirement removed to allow 'unsafe-inline' for inline scripts
        # If nonce is present, CSP ignores 'unsafe-inline' per spec
        referrer_policy='strict-origin-when-cross-origin',
        feature_policy={
            'geolocation': "'none'",
            'midi': "'none'",
            'camera': "'none'",
            'microphone': "'none'",
        }
    )
    logger.info("Flask-Talisman security headers enabled for production")
else:
    # In development, just add basic security headers without HTTPS enforcement
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    # Provide dummy csp_nonce() for development (Talisman provides it in production)
    @app.context_processor
    def inject_csp_nonce():
        def csp_nonce():
            return ''  # Empty nonce in dev - CSP not enforced
        return dict(csp_nonce=csp_nonce)

# Configure CORS - only allow specified origins in production
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:*').split(',')
CORS(app, resources={
    r"/api/*": {"origins": allowed_origins, "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]},
}, supports_credentials=True)
logger.info(f"CORS configured for origins: {allowed_origins}")

# =============================================================================
# END SECURITY CONFIGURATION
# =============================================================================

# Auth functions, validation, and config imported from organized modules above
# See: api/utils/auth.py, api/utils/validation.py, api/config.py

def get_available_modules(course_id=None):
    """Dynamically discover available module templates for a course.

    Args:
        course_id: The course identifier (e.g., 'cmsc173'). If None, returns empty dict.

    Returns:
        Dict of available modules keyed by module number.
    """
    if not course_id:
        return {}

    course = COURSES.get(course_id)
    if not course:
        return {}

    templates_dir = os.path.join(os.path.dirname(__file__), 'templates', 'courses', course_id)
    available = {}

    for module_num, module_info in course.get('modules', {}).items():
        filename = module_info['filename']
        filepath = os.path.join(templates_dir, filename)

        if os.path.exists(filepath):
            available[module_num] = module_info

    return available

@app.route('/')
def index():
    """Course Hub - main landing page with all courses"""
    # Calculate stats
    active_courses = sum(1 for c in COURSES.values() if c.get('is_active', False))
    total_modules = sum(len(c.get('modules', {})) for c in COURSES.values() if c.get('is_active', False))
    total_projects = sum(len(c.get('projects', [])) for c in COURSES.values() if c.get('is_active', False))

    return render_template('course_hub.html',
        courses=COURSES,
        active_courses=active_courses,
        total_modules=total_modules,
        total_projects=total_projects,
        active_page='hub'
    )


@app.route('/course/<course_id>')
def course_detail(course_id):
    """Course detail page with modules and projects"""
    if course_id not in COURSES:
        return render_template('error.html', error='Course not found', courses=COURSES), 404

    course = COURSES[course_id]

    # Get projects for this course
    course_projects = [PROJECTS[pid] for pid in course.get('projects', []) if pid in PROJECTS]

    # For CMSC 178IP, load exam notebook data for inline viewing
    exam_notebook = None
    answer_key_notebook = None
    if course_id == 'cmsc178ip':
        notebook_path = os.path.join(
            app.root_path, '..', 'static', 'data', 'courses',
            'cmsc178ip', 'finals_exam', 'student_template',
            'CMSC178IP_Finals_Unified.ipynb'
        )
        if os.path.exists(notebook_path):
            with open(notebook_path, 'r') as f:
                exam_notebook = json.load(f)

        # Load answer key for admins
        if session.get('is_admin'):
            answer_key_path = os.path.join(
                app.root_path, '..', 'static', 'data', 'courses',
                'cmsc178ip', 'finals_exam', 'admin',
                'CMSC178IP_Finals_ANSWER_KEY.ipynb'
            )
            if os.path.exists(answer_key_path):
                with open(answer_key_path, 'r') as f:
                    answer_key_notebook = json.load(f)

    return render_template('course_detail.html',
        course=course,
        course_id=course_id,
        projects=course_projects,
        categories=MODULE_CATEGORIES,
        courses=COURSES,
        active_course=course_id,
        is_admin=session.get('is_admin', False),
        exam_notebook=exam_notebook,
        answer_key_notebook=answer_key_notebook
    )

@app.route('/course/<course_id>/module/<module_id>')
def show_module(course_id, module_id):
    """Display a specific module for a course."""
    # Convert module_id to int if it's a number, otherwise keep as string
    try:
        module_number = int(module_id)
    except ValueError:
        module_number = module_id  # Keep as string (e.g., "intro")

    # Validate course exists
    course = COURSES.get(course_id)
    if not course:
        return render_template('error.html',
            error_title="Course Not Found",
            error_message=f"Course '{course_id}' does not exist.",
            back_url="/",
            back_text="Back to Course Hub",
            courses=COURSES
        ), 404

    available_modules = get_available_modules(course_id)

    if module_number not in available_modules:
        return render_template('error.html',
            error_title="Module Not Found",
            error_message=f"Module {module_number} not found in {course['code']}.",
            back_url=f"/course/{course_id}",
            back_text=f"Back to {course['code']}",
            courses=COURSES
        ), 404

    # -- Supabase Integration --
    # Only track view counts for numeric module IDs (skip "intro" etc.)
    view_count = 0
    supabase_client = get_supabase_client()
    if supabase_client and isinstance(module_number, int):
        try:
            # Increment view count (include course_id for future multi-course analytics)
            supabase_client.rpc('increment_module_view', {'module_id': module_number}).execute()

            # Get view count
            response = supabase_client.table('module_views').select('view_count').eq('module_number', module_number).execute()
            if response.data:
                view_count = response.data[0]['view_count']
            logger.info(f"Course {course_id} Module {module_number} view count: {view_count}")
        except Exception as e:
            logger.error(f"Error interacting with Supabase for {course_id}/module {module_number}: {e}", exc_info=True)
            view_count = 0
    # --------------------------

    module = available_modules[module_number]
    # Use course-scoped template path
    template_path = f"courses/{course_id}/{module['filename']}"
    return render_template(template_path, view_count=view_count, course=course, course_id=course_id, courses=COURSES)

@app.route('/course/<course_id>/syllabus')
def show_syllabus(course_id):
    """Display the syllabus for a course."""
    course = COURSES.get(course_id)
    if not course:
        return render_template('error.html',
            error_title="Course Not Found",
            error_message=f"Course '{course_id}' does not exist.",
            back_url="/",
            back_text="Back to Course Hub",
            courses=COURSES
        ), 404

    template_path = f"courses/{course_id}/syllabus.html"
    return render_template(template_path, course=course, course_id=course_id, courses=COURSES)

@app.route('/course/<course_id>/exam/download')
def download_exam(course_id):
    """Download the finals exam notebook for a course."""
    # Currently only cmsc178ip has a finals exam
    if course_id != 'cmsc178ip':
        return render_template('error.html',
            error_title="Exam Not Available",
            error_message=f"No finals exam is available for this course.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    # Path to the exam notebook
    exam_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'static', 'data', 'courses', 'cmsc178ip', 'finals_exam',
        'student_template', 'CMSC178IP_Finals_Unified.ipynb'
    )

    if not os.path.exists(exam_path):
        logger.error(f"Exam file not found: {exam_path}")
        return render_template('error.html',
            error_title="File Not Found",
            error_message="The exam file could not be found. Please contact the instructor.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    return send_file(
        exam_path,
        as_attachment=True,
        download_name='CMSC178IP_Finals_Exam.ipynb',
        mimetype='application/x-ipynb+json'
    )

@app.route('/course/<course_id>/exam/answer-key')
def download_answer_key(course_id):
    """Download the answer key (admin only - requires session)."""
    # Check if user is admin
    if not session.get('is_admin'):
        return render_template('error.html',
            error_title="Access Denied",
            error_message="You must be logged in as admin to access the answer key.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 403

    if course_id != 'cmsc178ip':
        return render_template('error.html',
            error_title="Not Available",
            error_message="No answer key available for this course.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    answer_key_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'static', 'data', 'courses', 'cmsc178ip', 'finals_exam',
        'admin', 'CMSC178IP_Finals_ANSWER_KEY.ipynb'
    )

    if not os.path.exists(answer_key_path):
        return render_template('error.html',
            error_title="File Not Found",
            error_message="Answer key file not found.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    return send_file(
        answer_key_path,
        as_attachment=True,
        download_name='CMSC178IP_Finals_ANSWER_KEY.ipynb',
        mimetype='application/x-ipynb+json'
    )

@app.route('/course/<course_id>/exam/view')
def view_exam_notebook(course_id):
    """View the exam notebook in the browser."""
    if course_id != 'cmsc178ip':
        return render_template('error.html',
            error_title="Not Available",
            error_message="No exam available for this course.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    # Determine which notebook to show
    is_admin = session.get('is_admin', False)
    show_answer_key = request.args.get('key') == '1' and is_admin

    if show_answer_key:
        notebook_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static', 'data', 'courses', 'cmsc178ip', 'finals_exam',
            'admin', 'CMSC178IP_Finals_ANSWER_KEY.ipynb'
        )
        title = "Finals Exam - ANSWER KEY"
    else:
        notebook_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static', 'data', 'courses', 'cmsc178ip', 'finals_exam',
            'student_template', 'CMSC178IP_Finals_Unified.ipynb'
        )
        title = "Finals Exam"

    if not os.path.exists(notebook_path):
        return render_template('error.html',
            error_title="File Not Found",
            error_message="Notebook file not found.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    # Read notebook JSON
    import json
    with open(notebook_path, 'r') as f:
        notebook_data = json.load(f)

    course = COURSES.get(course_id)
    return render_template('notebook_viewer.html',
        notebook=notebook_data,
        title=title,
        course=course,
        course_id=course_id,
        is_admin=is_admin,
        show_answer_key=show_answer_key,
        courses=COURSES
    )

@app.route('/course/<course_id>/lab/<int:week_num>/download')
def download_lab(course_id, week_num):
    """Download lab notebook."""
    if course_id != 'cmsc178da':
        return render_template('error.html',
            error_title="Labs Not Available",
            error_message="Labs are only available for CMSC 178DA.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    if not (1 <= week_num <= 11):
        return render_template('error.html',
            error_title="Invalid Week",
            error_message=f"Labs are available for weeks 1-11 only.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    lab_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'static', 'data', 'courses', 'cmsc178da', 'labs',
        f'week-{week_num:02d}-lab.ipynb'
    )

    if not os.path.exists(lab_path):
        logger.error(f"Lab file not found: {lab_path}")
        return render_template('error.html',
            error_title="Lab Not Found",
            error_message=f"Lab for week {week_num} is not yet available.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    return send_file(
        lab_path,
        as_attachment=True,
        download_name=f'CMSC178DA_Week{week_num:02d}_Lab.ipynb',
        mimetype='application/x-ipynb+json'
    )

@app.route('/course/<course_id>/lab/<int:week_num>/solution')
def download_lab_solution(course_id, week_num):
    """Download lab solution (publicly accessible for practice)."""
    if course_id != 'cmsc178da':
        return render_template('error.html',
            error_title="Not Available",
            error_message="Lab solutions are only available for CMSC 178DA.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    if not (1 <= week_num <= 11):
        return render_template('error.html',
            error_title="Invalid Week",
            error_message=f"Solutions are available for weeks 1-11 only.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    solution_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'static', 'data', 'courses', 'cmsc178da', 'labs',
        f'week-{week_num:02d}-solution.ipynb'
    )

    if not os.path.exists(solution_path):
        logger.error(f"Solution file not found: {solution_path}")
        return render_template('error.html',
            error_title="Solution Not Found",
            error_message=f"Solution for week {week_num} is not yet available.",
            back_url=f"/course/{course_id}",
            back_text="Back to Course",
            courses=COURSES
        ), 404

    return send_file(
        solution_path,
        as_attachment=True,
        download_name=f'CMSC178DA_Week{week_num:02d}_Solution.ipynb',
        mimetype='application/x-ipynb+json'
    )

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve images from the images directory"""
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    return send_from_directory(images_dir, filename)

@app.route('/api/groups', methods=['POST'])
@csrf.exempt
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
                    if assign_student_to_group(group_id, student_id):
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
        return jsonify({"error": "An internal error occurred"}), 500

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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/groups/<group_id>', methods=['DELETE'])
@admin_required
def delete_group_api(group_id):
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
        return jsonify({"error": "An internal error occurred"}), 500

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

        # Upload to Supabase Storage (Vercel-compatible - no local filesystem)
        import time
        secure_name = secure_filename(file.filename)
        storage_filename = f"groups/{group_id}/{int(time.time())}_{secure_name}"

        # Upload file directly to Supabase Storage
        uploaded_name = upload_submission_file(file, storage_filename, file.content_type)
        if not uploaded_name:
            logger.error(f"Failed to upload file to Supabase Storage")
            return jsonify({"error": "Failed to upload file"}), 500

        logger.info(f"File uploaded to Supabase Storage: {uploaded_name} for group {group_id}")

        try:
            # Get the public URL for the uploaded file
            file_url = get_submission_file_url(uploaded_name)
            new_document = add_group_document(group_id, document_title, file_url or uploaded_name)
            if new_document:
                logger.info(f"Document metadata added for group {group_id}")
                return jsonify(new_document), 201
            return jsonify({"error": "Failed to add document metadata"}), 500
        except Exception as e:
            logger.error(f"Error adding document metadata: {e}", exc_info=True)
            # Clean up file from Supabase Storage if metadata insertion fails
            try:
                delete_submission_file(uploaded_name)
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/stages/<stage_id>', methods=['PUT'])
def update_stage_api(stage_id):
    """Update project stage status, grade, and feedback"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Supabase not configured"}), 500
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON in request body"}), 400

        status = data.get('status')
        grade = data.get('grade')
        feedback = data.get('feedback')

        if not status:
            return jsonify({"error": "Status is required"}), 400

        success = update_stage_status(stage_id, status, grade, feedback)
        if success:
            logger.info(f"Stage {stage_id} updated successfully")
            return jsonify({"message": "Stage updated successfully"}), 200
        # Failure likely due to missing schema columns
        return jsonify({
            "error": "Failed to update stage. project_stages table may be missing required columns (status, grade, feedback)",
            "status": "incomplete_schema"
        }), 503
    except Exception as e:
        error_msg = str(e)
        if "status" in error_msg and "does not exist" in error_msg:
            return jsonify({
                "error": "project_stages table is missing required columns. Please add 'status', 'grade', and 'feedback' columns to project_stages table in Supabase.",
                "status": "incomplete_schema"
            }), 503
        elif "project_stages" in error_msg:
            return jsonify({
                "error": "Error with project_stages table schema",
                "status": "incomplete_schema"
            }), 503
        logger.error(f"Error updating stage {stage_id}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500

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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/groups/<group_id>/models', methods=['POST'])
def add_model_api(group_id):
    """Add a trained model result to the database"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Supabase not configured"}), 500
    try:
        # Handle missing Content-Type header
        if request.content_type is None or 'application/json' not in request.content_type:
            return jsonify({"error": "Request must have Content-Type: application/json header"}), 400

        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON in request body"}), 400

        model_name = data.get('model_name')
        model_type = data.get('model_type')
        metrics = {k: v for k, v in data.items() if k not in ['model_name', 'model_type']}

        if not model_name or not model_type:
            return jsonify({"error": "model_name and model_type are required"}), 400

        new_model = add_project_model(group_id, model_name, model_type, metrics)
        if new_model:
            logger.info(f"Model '{model_name}' added for group {group_id}")
            return jsonify(new_model), 201
        # Check if failure was due to missing table
        return jsonify({"error": "Failed to add model. project_models table may need to be created in Supabase.", "status": "incomplete_schema"}), 503
    except Exception as e:
        error_msg = str(e)
        if "project_models" in error_msg:
            return jsonify({"error": "project_models table does not exist", "status": "incomplete_schema"}), 503
        logger.error(f"Error adding model for group {group_id}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500

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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/group_portal')
def group_portal():
    return render_template('group_portal_enhanced.html', is_admin=False, courses=COURSES)

@app.route('/admin_login', methods=['GET', 'POST'])
@limiter.limit("5 per minute", methods=["POST"])  # Rate limit login attempts
def admin_login():
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            # Validate input
            if not username or not password:
                logger.warning("Login attempt with empty credentials")
                return render_template('admin_login.html', error='Username and password are required', courses=COURSES)

            admin_username = os.environ.get('ADMIN_USERNAME', '')
            admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH', '')

            if not admin_username or not admin_password_hash:
                logger.error("Admin credentials not properly configured")
                return render_template('admin_login.html', error='Server misconfiguration', courses=COURSES)

            # Verify password using secure hash comparison only
            if username == admin_username and check_password_hash(admin_password_hash, password):
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
                return render_template('admin_login.html', error='Invalid credentials', courses=COURSES)
        except Exception as e:
            logger.error(f"Error in admin login: {e}", exc_info=True)
            return render_template('admin_login.html', error='An error occurred during login', courses=COURSES)
    return render_template('admin_login.html', courses=COURSES)

@app.route('/admin_logout')
def admin_logout():
    """Logout admin user and clear session"""
    session.clear()
    logger.info("Admin user logged out")
    return redirect(url_for('group_portal'))

# --- ADMIN DASHBOARD & SUBMISSIONS ---

@app.route('/admin')
@admin_page_required
def admin():
    """Redirect /admin to /admin_dashboard"""
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard')
@admin_page_required
def admin_dashboard():
    """Admin dashboard with statistics and overview"""
    return render_template('admin_dashboard.html', active_page='admin_dashboard', courses=COURSES)

@app.route('/admin_roster')
@admin_page_required
def admin_roster():
    """Admin student roster page."""
    return render_template('admin_student_roster.html', active_page='admin_roster', courses=COURSES)


@app.route('/admin_class_records')
@admin_page_required
def admin_class_records():
    """Admin class records page - track exam submissions and scores."""
    return render_template('admin_class_records.html', active_page='admin_class_records')

@app.route('/admin_submissions')
@admin_page_required
def admin_submissions():
    """Admin view to see all submissions by all groups"""
    return render_template('admin_submissions.html', active_page='admin_submissions', courses=COURSES)

# ─── CMSC 173 Midterm Exam Routes ────────────────────────────────────────────

CMSC173_DATA_DIR = os.path.join(parent_dir, 'data', 'CMSC173 Midterm Attachments')

@app.route('/admin_cmsc173_midterm')
@admin_page_required
def admin_cmsc173_midterm():
    """CMSC 173 Midterm Exam class record page."""
    return render_template('admin_cmsc173_midterm.html',
                           active_page='admin_cmsc173_midterm',
                           courses=COURSES)


@app.route('/api/admin/cmsc173-midterm/data')
@admin_required
def cmsc173_midterm_data():
    """Return merged grading data as JSON from the two CSV files."""
    summary_path = os.path.join(CMSC173_DATA_DIR, '_grading_summary.csv')
    detail_path = os.path.join(CMSC173_DATA_DIR, '_detailed_grading_table.csv')

    if not os.path.exists(summary_path):
        return jsonify({"error": "Grading summary not found"}), 404

    summary = {}
    with open(summary_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            summary[row['ID']] = row

    details = {}
    if os.path.exists(detail_path):
        with open(detail_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                details[row['ID']] = row

    students = []
    for student_id, s in summary.items():
        d = details.get(student_id, {})
        students.append({
            'name': s.get('Student Name', ''),
            'id': s.get('ID', ''),
            'submitted': s.get('Submitted', ''),
            'exp_k': s.get('Exp_k', ''), 'stu_k': s.get('Stu_k', ''),
            'k_match': s.get('k?', ''),
            'exp_cat': s.get('Exp_Cat', ''), 'stu_cat': s.get('Stu_Cat', ''),
            'exp_clf': s.get('Exp_Clf', ''), 'stu_clf': s.get('Stu_Clf', ''),
            'exp_r2': s.get('Exp_R2', ''), 'stu_r2': s.get('Stu_R2', ''),
            'exp_sil': s.get('Exp_Sil', ''), 'stu_sil': s.get('Stu_Sil', ''),
            'q1': s.get('Q1', ''), 'q2': s.get('Q2', ''),
            'q3': s.get('Q3', ''), 'q4': s.get('Q4', ''),
            'q5': s.get('Q5', ''),
            'total': s.get('Total', ''),
            'bonus': s.get('Bonus', ''),
            'final': s.get('Final', ''),
            'grade': s.get('Grade', ''),
            'q1_reasoning': d.get('Q1 Reasoning', ''),
            'q2_reasoning': d.get('Q2 Reasoning', ''),
            'q3_reasoning': d.get('Q3 Reasoning', ''),
            'q4_reasoning': d.get('Q4 Reasoning', ''),
            'q5_reasoning': d.get('Q5 Reasoning', ''),
            'methodology_checks': d.get('Methodology Checks', ''),
            'llm_model': d.get('LLM Model', ''),
            'llm_experience': d.get('LLM Experience', ''),
        })

    return jsonify(students)


@app.route('/api/admin/cmsc173-midterm/student-files/<student_name>')
@admin_required
def cmsc173_midterm_student_files(student_name):
    """List available files for a student."""
    if not os.path.exists(CMSC173_DATA_DIR):
        return jsonify({"error": "Data directory not found"}), 404

    matching = [d for d in os.listdir(CMSC173_DATA_DIR)
                if d.startswith(student_name + ' (')
                and os.path.isdir(os.path.join(CMSC173_DATA_DIR, d))
                and '@up.edu.ph' in d]

    if not matching:
        return jsonify({"files": {"exam": [], "submission": []}}), 200

    folder = matching[0]
    files = {'exam': [], 'submission': []}

    for subdir in ['exam', 'submission']:
        path = os.path.join(CMSC173_DATA_DIR, folder, subdir)
        if os.path.exists(path):
            for fname in sorted(os.listdir(path)):
                if fname.startswith('.'):
                    continue
                ext = fname.rsplit('.', 1)[-1].lower() if '.' in fname else 'unknown'
                files[subdir].append({
                    'name': fname,
                    'path': f"{folder}/{subdir}/{fname}",
                    'type': ext
                })

    return jsonify({"folder": folder, "files": files})


@app.route('/api/admin/cmsc173-midterm/files/<path:filepath>')
@admin_required
def cmsc173_midterm_file(filepath):
    """Serve student files from the CMSC173 midterm data directory."""
    requested = os.path.realpath(os.path.join(CMSC173_DATA_DIR, filepath))
    allowed = os.path.realpath(CMSC173_DATA_DIR)
    if not requested.startswith(allowed + os.sep):
        return jsonify({"error": "Invalid file path"}), 400

    if not os.path.exists(requested):
        return jsonify({"error": "File not found"}), 404

    directory = os.path.dirname(requested)
    filename = os.path.basename(requested)

    if filename.endswith('.pdf'):
        return send_from_directory(directory, filename, as_attachment=False)
    elif filename.endswith('.ipynb'):
        return send_from_directory(directory, filename, as_attachment=False,
                                   mimetype='application/json')
    elif filename.endswith('.html'):
        return send_from_directory(directory, filename, as_attachment=False)
    else:
        return send_from_directory(directory, filename, as_attachment=True)


@app.route('/admin_cmsc173_midterm/notebook/<path:filepath>')
@admin_page_required
def cmsc173_midterm_notebook(filepath):
    """View a student's notebook in the notebook viewer."""
    notebook_path = os.path.realpath(os.path.join(CMSC173_DATA_DIR, filepath))
    allowed = os.path.realpath(CMSC173_DATA_DIR)
    if not notebook_path.startswith(allowed + os.sep) or not os.path.exists(notebook_path):
        return "Notebook not found", 404

    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_data = json.load(f)

    student_name = filepath.split('/')[0].split(' (')[0]
    return render_template('notebook_viewer.html',
        notebook=notebook_data,
        title=f"Midterm Notebook - {student_name}",
        course=None,
        course_id='cmsc173',
        is_admin=True,
        show_answer_key=False,
        courses=COURSES,
        active_page='admin_cmsc173_midterm'
    )


@app.route('/api/admin/statistics', methods=['GET'])
@admin_required
def get_admin_statistics():
    """Get dashboard statistics for admin"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Count total groups (only active ones)
        groups_response = supabase_client.table('groups').select('id', count='exact').eq('is_active', True).execute()
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/admin/submissions', methods=['GET'])
@admin_required
def get_all_submissions_admin():
    """Get all submissions with optional filters"""
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/admin/submissions/<submission_id>', methods=['GET'])
@admin_required
def get_submission_details_admin(submission_id):
    """Get detailed information about a specific submission"""
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/admin/download/<submission_id>', methods=['GET'])
@admin_required
def download_submission_file(submission_id):
    """Download a submitted file"""
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

        # Check if file_path is a URL (Supabase Storage)
        if file_path.startswith('http://') or file_path.startswith('https://'):
            logger.info(f"Redirecting to Supabase Storage URL for submission {submission_id}")
            return redirect(file_path)

        # Legacy: local file path
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/admin/view/<submission_id>', methods=['GET'])
@admin_required
def view_submission_file(submission_id):
    """View a submitted file in browser (for PDFs)"""
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

        # Check if file_path is a URL (Supabase Storage)
        if file_path.startswith('http://') or file_path.startswith('https://'):
            logger.info(f"Redirecting to Supabase Storage URL for viewing submission {submission_id}")
            return redirect(file_path)

        # Legacy: local file path
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/admin/groups/submission-status', methods=['GET'])
@admin_required
def get_groups_submission_status():
    """Get all groups with their submission status for each stage"""
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Get all active groups
        groups_response = supabase_client.table('groups').select('id, group_name, project_title').eq('is_active', True).execute()

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
        return jsonify({"error": "An internal error occurred"}), 500

# --- GROUP AUTHENTICATION & PORTAL ---

@app.route('/group_login', methods=['GET', 'POST'])
@csrf.exempt
@limiter.limit("10 per minute", methods=["POST"])  # Rate limit login attempts
def group_login():
    """Group login page"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not username or not password:
                return render_template('group_login.html', error='Username and password are required', courses=COURSES)

            # Get group by username
            group = get_group_by_username(username)
            if not group:
                logger.warning(f"Login attempt with non-existent username: {username}")
                return render_template('group_login.html', error='Invalid username or password', courses=COURSES)

            # Verify password
            if not check_password_hash(group.get('password_hash', ''), password):
                logger.warning(f"Failed login attempt for group username {username}")
                return render_template('group_login.html', error='Invalid username or password', courses=COURSES)

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
            return render_template('group_login.html', error='An error occurred', courses=COURSES)

    return render_template('group_login.html', courses=COURSES)

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
            return render_template('group_submission_portal.html', error='Group not found', group=None, courses=COURSES)

        # Derive project from group's class
        project_id = 'ml-research-project'  # Default fallback
        course_id = 'cmsc173'  # Default fallback

        class_id = group.get('class_id')
        if class_id:
            class_data = get_class_by_id(class_id)
            if class_data:
                course_code = class_data.get('course_code', '')
                project_id = COURSE_PROJECTS.get(course_code, 'ml-research-project')
                project_config = PROJECTS.get(project_id, {})
                course_id = project_config.get('course', 'cmsc173')

        project = PROJECTS.get(project_id, PROJECTS.get('ml-research-project', {}))
        course = COURSES.get(course_id, COURSES.get('cmsc173', {}))

        return render_template('group_submission_portal.html',
            group=group,
            group_name=session.get('group_name'),
            project=project,
            course=course,
            courses=COURSES
        )
    except Exception as e:
        logger.error(f"Error loading group submission portal: {e}", exc_info=True)
        return render_template('group_submission_portal.html', error='An error occurred', group=None, courses=COURSES)

@app.route('/admin/group/<group_id>')
@admin_page_required
def admin_view_group(group_id):
    """Admin view of a specific group's submissions and portal (admin only)"""
    try:
        supabase_client = get_supabase_client()
        group = get_group_with_submissions(group_id)
        if not group:
            return render_template('group_submission_portal.html', error='Group not found', courses=COURSES)

        # Derive project from group's class
        project_id = 'ml-research-project'  # Default fallback
        course_id = 'cmsc173'  # Default fallback

        class_id = group.get('class_id')
        if class_id:
            class_data = get_class_by_id(class_id)
            if class_data:
                course_code = class_data.get('course_code', '')
                project_id = COURSE_PROJECTS.get(course_code, 'ml-research-project')
                project_config = PROJECTS.get(project_id, {})
                course_id = project_config.get('course', 'cmsc173')

        project = PROJECTS.get(project_id, PROJECTS.get('ml-research-project', {}))
        course = COURSES.get(course_id, COURSES.get('cmsc173', {}))

        # Get all groups for prev/next navigation
        prev_group_id = None
        next_group_id = None
        try:
            all_groups = supabase_client.table('groups').select('id, group_name').order('group_name').execute()
            if all_groups.data:
                group_ids = [g['id'] for g in all_groups.data]
                if group_id in group_ids:
                    current_index = group_ids.index(group_id)
                    if current_index > 0:
                        prev_group_id = group_ids[current_index - 1]
                    if current_index < len(group_ids) - 1:
                        next_group_id = group_ids[current_index + 1]
        except Exception as nav_error:
            logger.warning(f"Could not fetch group navigation: {nav_error}")

        # Fetch existing scores for this group's submissions
        scores = {}
        try:
            if group.get('submissions'):
                submission_ids = [s['id'] for s in group['submissions'] if s]
                if submission_ids:
                    scores_result = supabase_client.table('submission_scores').select('*').in_('submission_id', submission_ids).execute()
                    if scores_result.data:
                        for score in scores_result.data:
                            # Find which stage this score belongs to
                            for i, sub in enumerate(group['submissions']):
                                if sub and sub['id'] == score['submission_id']:
                                    scores[i] = score
                                    break
            group['scores'] = scores
        except Exception as score_error:
            logger.warning(f"Could not fetch scores: {score_error}")
            group['scores'] = {}

        # Render the same submission portal template but for admin viewing
        return render_template('group_submission_portal.html',
                             group=group,
                             group_name=group.get('group_name'),
                             project=project,
                             course=course,
                             is_admin_view=True,
                             prev_group_id=prev_group_id,
                             next_group_id=next_group_id,
                             courses=COURSES)
    except Exception as e:
        logger.error(f"Error loading admin group view: {e}", exc_info=True)
        return render_template('group_submission_portal.html', error='An error occurred', courses=COURSES)

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
        return jsonify({"error": "An internal error occurred"}), 500

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
        return jsonify({"error": "An internal error occurred"}), 500

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

        # Upload to Supabase Storage (Vercel-compatible)
        import time
        secure_name = secure_filename(file.filename)
        storage_filename = f"submissions/{group_id}/{stage_id}/{int(time.time())}_{secure_name}"

        uploaded_name = upload_submission_file(file, storage_filename, file.content_type)
        if not uploaded_name:
            logger.error("Failed to upload file to Supabase Storage")
            return jsonify({"error": "Failed to upload file"}), 500

        # Get public URL for the file
        file_url = get_submission_file_url(uploaded_name)

        # Submit work with file reference (use URL instead of local path)
        submission = submit_stage_work(group_id, stage_id, student_id, file_path=file_url or uploaded_name, file_name=secure_name)
        if submission:
            logger.info(f"File submitted by student {student_id} for stage {stage_id}")
            return jsonify(submission), 201
        else:
            return jsonify({"error": "Failed to record submission"}), 500

    except Exception as e:
        logger.error(f"Error submitting file: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500

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
@csrf.exempt
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
            import time
            original_filename = secure_filename(file.filename)
            storage_path = f"groups/{group_id}/stage_{stage_number}/{int(time.time())}_{original_filename}"

            # Upload to Supabase Storage
            uploaded_name = upload_submission_file(file, storage_path, file.content_type)

            if not uploaded_name:
                logger.error(f"Failed to upload file for group {group_id}")
                return jsonify({"error": "Failed to upload file"}), 500

            # Get file URL
            file_url = get_submission_file_url(uploaded_name)

            # Add file information to submission data
            submission_data['file_path'] = file_url or uploaded_name
            submission_data['file_name'] = original_filename
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/group/submission/<submission_id>', methods=['PUT'])
def update_submission_api(submission_id):
    """Update a group submission (presentation link, summary, content)"""
    if not session.get('is_group_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        data = request.get_json()
        group_id = session.get('group_id')

        # Get the submission to verify ownership
        submission_response = supabase_client.table('group_submissions').select('*').eq('id', submission_id).execute()
        if not submission_response.data:
            return jsonify({"error": "Submission not found"}), 404

        submission = submission_response.data[0]
        if submission['group_id'] != group_id:
            return jsonify({"error": "Unauthorized - not your submission"}), 403

        # Validate required fields
        presentation_link = data.get('presentation_link', '').strip()
        summary_markdown = data.get('summary_markdown', '').strip()

        if not presentation_link:
            return jsonify({"error": "Presentation link is required"}), 400
        if not summary_markdown:
            return jsonify({"error": "Summary is required"}), 400

        # Update submission
        update_data = {
            'presentation_link': presentation_link,
            'summary_markdown': summary_markdown,
            'submission_content': data.get('submission_content', ''),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }

        response = supabase_client.table('group_submissions').update(update_data).eq('id', submission_id).execute()

        if response.data and len(response.data) > 0:
            logger.info(f"Submission {submission_id} updated for group {group_id}")
            return jsonify({"message": "Submission updated successfully"}), 200
        else:
            logger.error(f"Failed to update submission {submission_id}")
            return jsonify({"error": "Failed to update submission"}), 500

    except Exception as e:
        logger.error(f"Error updating submission: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/group/delete', methods=['PUT'])
def soft_delete_group_api():
    """Soft delete a group (set is_active to false)"""
    # Allow both group login and admin access
    admin_access = is_admin_authenticated()
    is_group = session.get('is_group_logged_in')

    if not admin_access and not is_group:
        return jsonify({"error": "Unauthorized"}), 401

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Get group_id from request for admin, session for group
        data = request.get_json() or {}
        if admin_access and data.get('group_id'):
            group_id = data.get('group_id')
        else:
            group_id = session.get('group_id')

        if not group_id:
            return jsonify({"error": "No group session found"}), 400

        # Soft delete the group by setting is_active to false
        update_data = {
            'is_active': False
        }

        response = supabase_client.table('groups').update(update_data).eq('id', group_id).execute()

        # Check if update was successful (response may be empty but still successful)
        if response:
            logger.info(f"Group {group_id} soft deleted successfully")
            # Clear the session
            session.clear()
            return jsonify({"message": "Group deleted successfully"}), 200
        else:
            logger.error(f"Failed to soft delete group {group_id}")
            return jsonify({"error": "Failed to delete group"}), 500

    except Exception as e:
        logger.error(f"Error deleting group: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500

# --- STUDENT MANAGEMENT API ---

@app.route('/api/students/class/<class_id>', methods=['GET'])
@admin_required
def get_students_by_class_api(class_id):
    """Get all students in a class."""
    try:
        students = get_students_by_class(class_id)
        return jsonify(students), 200
    except Exception as e:
        logger.error(f"Error getting students: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/students/ungrouped/<class_id>', methods=['GET'])
@admin_required
def get_ungrouped_students_api(class_id):
    """Get ungrouped students in a class."""
    try:
        students = get_ungrouped_students(class_id)
        return jsonify(students), 200
    except Exception as e:
        logger.error(f"Error getting ungrouped students: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/students/grouped/<class_id>', methods=['GET'])
@admin_required
def get_grouped_students_api(class_id):
    """Get grouped students in a class."""
    try:
        students = get_grouped_students(class_id)
        return jsonify(students), 200
    except Exception as e:
        logger.error(f"Error getting grouped students: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/students/campus/<campus_id>', methods=['GET'])
@admin_required
def get_student_api(campus_id):
    """Get student by campus ID."""
    try:
        student = get_student_by_campus_id(campus_id)
        if student:
            return jsonify(student), 200
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        logger.error(f"Error getting student: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/students/<student_id>/assign-group/<group_id>', methods=['POST'])
@admin_required
def assign_student_to_group_api(student_id, group_id):
    """Assign a student to a group."""
    try:
        success = assign_student_to_group(student_id, group_id)
        if success:
            logger.info(f"Assigned student {student_id} to group {group_id}")
            return jsonify({"success": True}), 200
        return jsonify({"error": "Failed to assign student"}), 500
    except Exception as e:
        logger.error(f"Error assigning student: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/students/<student_id>/unassign-group', methods=['POST'])
@admin_required
def unassign_student_api(student_id):
    """Remove a student from their group."""
    try:
        success = unassign_student_from_group(student_id)
        if success:
            logger.info(f"Unassigned student {student_id} from group")
            return jsonify({"success": True}), 200
        return jsonify({"error": "Failed to unassign student"}), 500
    except Exception as e:
        logger.error(f"Error unassigning student: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/group/members/available', methods=['GET'])
def get_available_students_for_group_api():
    """Get ungrouped students excluding those already in the group."""
    # Allow both group login and admin access
    is_admin = is_admin_authenticated()
    is_group = session.get('is_group_logged_in')

    if not is_admin and not is_group:
        return jsonify({"error": "Unauthorized"}), 401

    # Get group_id from request param for admin, session for group
    if is_admin and request.args.get('group_id'):
        group_id = request.args.get('group_id')
    else:
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
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/group/members/add', methods=['POST'])
def add_group_member_api():
    """Add a student to the current group (for group members or admin)."""
    # Allow both group login and admin access
    is_admin = is_admin_authenticated()
    is_group = session.get('is_group_logged_in')

    if not is_admin and not is_group:
        return jsonify({"error": "Unauthorized"}), 401

    # Get group_id from request for admin, session for group
    data = request.get_json()
    if is_admin and data.get('group_id'):
        group_id = data.get('group_id')
    else:
        group_id = session.get('group_id')
    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/groups/<group_id>/members', methods=['GET'])
def get_group_members_api(group_id):
    """Get all members of a group."""
    try:
        members = get_group_members(group_id)
        return jsonify(members), 200
    except Exception as e:
        logger.error(f"Error getting group members: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/groups/<group_id>/comments', methods=['GET'])
@admin_required
def get_group_comments(group_id):
    """Get admin comments for a group."""
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/groups/<group_id>/comments', methods=['POST'])
@admin_required
def add_group_comment(group_id):
    """Add a comment to a group (admin only)."""
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
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/classes/<course_code>/<section>', methods=['GET'])
def get_class_api(course_code, section):
    """Get class info and students for any course/section combination.

    Args:
        course_code: Course code (e.g., 'cmsc173', 'CMSC173')
        section: Section letter (e.g., 'a', 'A', 'd', 'D')
    """
    try:
        # Normalize inputs
        course_code_upper = course_code.upper()
        section_upper = section.upper()

        # Validate section (single letter A-Z)
        if len(section_upper) != 1 or not section_upper.isalpha():
            return jsonify({"error": "Invalid section format"}), 400

        cmsc_class = get_class_by_code_section(course_code_upper, section_upper)

        if not cmsc_class:
            logger.warning(f"Class not found: {course_code_upper} Section {section_upper}")
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
        logger.error(f"Error getting class {course_code}/{section}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


# Legacy routes for backward compatibility - redirect to new parameterized route
@app.route('/api/classes/cmsc173a', methods=['GET'])
def get_cmsc173a_class_api():
    """Legacy route - redirects to parameterized endpoint."""
    return get_class_api('CMSC173', 'A')

@app.route('/api/classes/cmsc173d', methods=['GET'])
def get_cmsc173d_class_api():
    """Legacy route - redirects to parameterized endpoint."""
    return get_class_api('CMSC173', 'D')

@app.route('/api/classes/cmsc173e', methods=['GET'])
def get_cmsc173e_class_api():
    """Legacy route - redirects to parameterized endpoint."""
    return get_class_api('CMSC173', 'E')

# --- ADMIN SUBMISSION SCORING ENDPOINTS ---

@app.route('/api/admin/submissions/<submission_id>/score', methods=['POST'])
@admin_required
def save_submission_score(submission_id):
    """Save a score for a submission."""
    supabase = get_supabase_client()
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500

    try:
        data = request.json or request.form.to_dict()
        score = float(data.get('score', 0))
        max_score = float(data.get('max_score', 100))
        feedback = data.get('feedback', '')
        admin_notes = data.get('admin_notes', '')

        result = supabase.table('group_submissions').update({
            'score': score,
            'max_score': max_score,
            'feedback': feedback,
            'admin_notes': admin_notes
        }).eq('id', submission_id).execute()

        # Return updated record
        result = supabase.table('group_submissions').select('*').eq('id', submission_id).execute()
        return jsonify(result.data[0] if result.data else {"error": "Not found"}), 200 if result.data else 404
    except ValueError:
        return jsonify({"error": "Invalid score value"}), 400
    except Exception as e:
        logger.error(f"Error saving submission score: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/admin/submissions/<submission_id>/score', methods=['GET'])
@admin_required
def get_submission_score(submission_id):
    """Get the score for a submission."""
    supabase = get_supabase_client()
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500

    try:
        result = supabase.table('group_submissions').select('score, max_score, feedback, admin_notes').eq('id', submission_id).execute()
        if result.data:
            return jsonify(result.data[0]), 200
        else:
            return jsonify({"message": "No score found"}), 404
    except Exception as e:
        logger.error(f"Error getting submission score: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/admin/groups/submissions-grid', methods=['GET'])
@admin_required
def get_groups_submissions_grid():
    """Get all groups with their submission statuses organized for dashboard grid view."""
    supabase = get_supabase_client()
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Get all groups with their submissions
        groups = supabase.table('groups').select('*, group_submissions(*)').eq('is_active', True).execute()
        return jsonify(groups.data), 200
    except Exception as e:
        logger.error(f"Error getting groups submissions grid: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/admin/groups/<group_id>/submissions-dashboard', methods=['GET'])
@admin_required
def get_group_submissions_dashboard(group_id):
    """Get a group's submissions organized by stage for dashboard display."""
    supabase = get_supabase_client()
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500

    try:
        # Get group with its submissions
        result = supabase.table('groups').select('*, group_submissions(*)').eq('id', group_id).execute()
        if result.data:
            return jsonify(result.data[0]), 200
        else:
            return jsonify({"error": "Group not found"}), 404
    except Exception as e:
        logger.error(f"Error getting group submissions dashboard: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

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

        # Check if file_path is a URL (Supabase Storage)
        if file_path.startswith('http://') or file_path.startswith('https://'):
            logger.info(f"Redirecting to Supabase Storage URL for summary {submission_id}")
            return redirect(file_path)

        # Legacy: local file path - verify exists
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
        return jsonify({"error": "An internal error occurred"}), 500

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
        response = supabase_client.table('group_submissions').select('*').eq('id', submission_id).execute()

        if not response.data or len(response.data) == 0:
            logger.warning(f"Submission not found: {submission_id}")
            return jsonify({"error": "Submission not found"}), 404

        submission = response.data[0]
        file_path = submission.get('presentation_path')
        file_name = submission.get('presentation_file')

        if not file_path:
            logger.warning(f"No presentation file found in submission: {submission_id}")
            return jsonify({"error": "Presentation file not available for download"}), 404

        # Check if file_path is a URL (Supabase Storage)
        if file_path.startswith('http://') or file_path.startswith('https://'):
            logger.info(f"Redirecting to Supabase Storage URL for presentation {submission_id}")
            return redirect(file_path)

        # Legacy: local file path - verify exists
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
        return jsonify({"error": "An internal error occurred"}), 500

# --- COURSE RESOURCES API ---

import re

# YouTube Video ID validation regex
YOUTUBE_VIDEO_ID_REGEX = re.compile(r'^[a-zA-Z0-9_-]{11}$')

# YouTube URL patterns for extracting video ID
YOUTUBE_URL_PATTERNS = [
    re.compile(r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})'),
]


def extract_youtube_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    if not url:
        return None

    # Check if it's already a valid video ID
    if YOUTUBE_VIDEO_ID_REGEX.match(url):
        return url

    # Try to extract from URL
    for pattern in YOUTUBE_URL_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)

    return None


def validate_youtube_video_id(video_id: str) -> bool:
    """Validate YouTube video ID format (XSS prevention)."""
    if not video_id:
        return False
    return bool(YOUTUBE_VIDEO_ID_REGEX.match(video_id))


@app.route('/api/courses/<course_id>/resources', methods=['GET'])
def get_resources_api(course_id):
    """Get all active resources for a course (public endpoint)."""
    try:
        resources = get_course_resources(course_id, include_inactive=False)
        logger.info(f"Fetched {len(resources)} resources for course {course_id}")
        return jsonify(resources), 200
    except Exception as e:
        logger.error(f"Error fetching resources for course {course_id}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/resources', methods=['GET'])
@admin_required
def get_all_resources_admin():
    """Get all resources for a course including inactive (admin only)."""
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400

    try:
        resources = get_course_resources(course_id, include_inactive=True)
        logger.info(f"Admin fetched {len(resources)} resources for course {course_id}")
        return jsonify(resources), 200
    except Exception as e:
        logger.error(f"Error fetching resources: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/resources', methods=['POST'])
@admin_required
def create_resource_api():
    """Create a new course resource (admin only)."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        course_id = data.get('course_id', '').strip()
        title = data.get('title', '').strip()
        resource_type = data.get('resource_type', 'youtube').strip()
        description = data.get('description', '').strip()

        # Validate required fields
        if not course_id:
            return jsonify({"error": "course_id is required"}), 400
        if not title:
            return jsonify({"error": "title is required"}), 400

        # Validate title length
        is_valid, error_msg = validate_input(title, 255, "title")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Validate resource type
        if resource_type not in ('youtube', 'link', 'pdf'):
            return jsonify({"error": "resource_type must be 'youtube', 'link', or 'pdf'"}), 400

        resource_data = {
            'course_id': course_id,
            'title': title,
            'resource_type': resource_type,
            'description': description,
            'is_active': data.get('is_active', True)
        }

        # Handle YouTube resources
        if resource_type == 'youtube':
            youtube_url = data.get('youtube_url', '').strip()
            youtube_video_id = data.get('youtube_video_id', '').strip()

            # Extract video ID from URL if provided
            if youtube_url and not youtube_video_id:
                youtube_video_id = extract_youtube_video_id(youtube_url)

            if not youtube_video_id:
                return jsonify({"error": "youtube_video_id is required for YouTube resources"}), 400

            # Validate video ID format (XSS prevention)
            if not validate_youtube_video_id(youtube_video_id):
                return jsonify({"error": "Invalid YouTube video ID format. Must be 11 characters (a-z, A-Z, 0-9, -, _)"}), 400

            resource_data['youtube_video_id'] = youtube_video_id

        # Handle link/PDF resources
        elif resource_type in ('link', 'pdf'):
            external_url = data.get('external_url', '').strip()
            if not external_url:
                return jsonify({"error": f"external_url is required for {resource_type} resources"}), 400
            resource_data['external_url'] = external_url

        # Create resource
        new_resource = create_resource(resource_data)
        if new_resource:
            logger.info(f"Resource created: {new_resource.get('id')} for course {course_id}")
            return jsonify(new_resource), 201
        else:
            return jsonify({"error": "Failed to create resource"}), 500

    except Exception as e:
        error_msg = str(e)
        # Check for duplicate video constraint
        if "unique_video_per_course" in error_msg or "23505" in error_msg:
            return jsonify({"error": "This video already exists in this course"}), 400
        logger.error(f"Error creating resource: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/resources/<resource_id>', methods=['PUT'])
@admin_required
def update_resource_api(resource_id):
    """Update an existing resource (admin only)."""
    try:
        # Validate resource_id
        is_valid, error_msg = validate_input(resource_id, 255, "resource_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Build update data (only include provided fields)
        update_data = {}

        if 'title' in data:
            title = data['title'].strip()
            is_valid, error_msg = validate_input(title, 255, "title")
            if not is_valid:
                return jsonify({"error": error_msg}), 400
            update_data['title'] = title

        if 'description' in data:
            update_data['description'] = data['description'].strip()

        if 'is_active' in data:
            update_data['is_active'] = bool(data['is_active'])

        if 'youtube_video_id' in data:
            video_id = data['youtube_video_id'].strip()
            if video_id and not validate_youtube_video_id(video_id):
                return jsonify({"error": "Invalid YouTube video ID format"}), 400
            update_data['youtube_video_id'] = video_id if video_id else None

        if 'external_url' in data:
            update_data['external_url'] = data['external_url'].strip()

        if not update_data:
            return jsonify({"error": "No fields to update"}), 400

        # Update resource
        updated = update_resource(resource_id, update_data)
        if updated:
            logger.info(f"Resource {resource_id} updated")
            return jsonify(updated), 200
        else:
            return jsonify({"error": "Resource not found or update failed"}), 404

    except Exception as e:
        logger.error(f"Error updating resource {resource_id}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/resources/<resource_id>', methods=['DELETE'])
@admin_required
def delete_resource_api(resource_id):
    """Delete a resource (admin only)."""
    try:
        # Validate resource_id
        is_valid, error_msg = validate_input(resource_id, 255, "resource_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        success = delete_resource(resource_id)
        if success:
            logger.info(f"Resource {resource_id} deleted")
            return jsonify({"message": "Resource deleted successfully"}), 200
        else:
            return jsonify({"error": "Resource not found or delete failed"}), 404

    except Exception as e:
        logger.error(f"Error deleting resource {resource_id}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/resources/reorder', methods=['PUT'])
@admin_required
def reorder_resources_api():
    """Reorder resources for a course (admin only)."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        course_id = data.get('course_id')
        ordered_ids = data.get('ordered_ids', [])

        if not course_id:
            return jsonify({"error": "course_id is required"}), 400
        if not isinstance(ordered_ids, list):
            return jsonify({"error": "ordered_ids must be a list"}), 400

        success = reorder_resources(course_id, ordered_ids)
        if success:
            logger.info(f"Resources reordered for course {course_id}")
            return jsonify({"message": "Resources reordered successfully"}), 200
        else:
            return jsonify({"error": "Failed to reorder resources"}), 500

    except Exception as e:
        logger.error(f"Error reordering resources: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/resources/counts', methods=['GET'])
def get_resource_counts_api():
    """Get resource counts for all courses (public endpoint for course cards)."""
    try:
        counts = get_resource_counts_by_course()
        return jsonify(counts), 200
    except Exception as e:
        logger.error(f"Error fetching resource counts: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/admin_resources')
@admin_page_required
def admin_resources():
    """Admin resource management page."""
    return render_template('admin_resources.html', active_page='admin_resources', courses=COURSES)


# --- Class Records API Endpoints ---

@app.route('/api/admin/classes', methods=['GET'])
@admin_required
def get_classes_api():
    """Get all classes for the class records filter."""
    try:
        classes = get_all_classes()
        return jsonify(classes), 200
    except Exception as e:
        logger.error(f"Error fetching classes: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/class-records/<class_id>', methods=['GET'])
@admin_required
def get_class_records_api(class_id):
    """Get all students in a class with exam status and scores."""
    try:
        records = get_class_records(class_id)
        return jsonify(records), 200
    except Exception as e:
        logger.error(f"Error fetching class records: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/class-records/student/<student_id>', methods=['PUT'])
@csrf.exempt
@admin_required
def update_student_exam_api(student_id):
    """Update a student's exam submission status and score."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        exam_submitted = data.get('exam_submitted')
        exam_score = data.get('exam_score')

        # Validate exam_score if provided
        if exam_score is not None:
            try:
                exam_score = float(exam_score)
                if exam_score < 0 or exam_score > 100:
                    return jsonify({"error": "exam_score must be between 0 and 100"}), 400
            except (ValueError, TypeError):
                return jsonify({"error": "exam_score must be a number"}), 400

        success = update_student_exam_status(student_id, exam_submitted, exam_score)
        if success:
            return jsonify({"message": "Student record updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update student record"}), 500

    except Exception as e:
        logger.error(f"Error updating student exam status: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/class-records/bulk-update', methods=['PUT'])
@csrf.exempt
@admin_required
def bulk_update_exam_api():
    """Bulk update exam status for multiple students."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        updates = data.get('updates', [])
        if not isinstance(updates, list):
            return jsonify({"error": "updates must be a list"}), 400

        result = bulk_update_exam_status(updates)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error bulk updating exam status: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


# --- Assessment API Endpoints ---

@app.route('/api/admin/assessments/<class_id>', methods=['GET'])
@admin_required
def get_assessments_api(class_id):
    """Get all assessments for a class."""
    try:
        assessments = get_assessments_by_class(class_id)
        return jsonify(assessments), 200
    except Exception as e:
        logger.error(f"Error fetching assessments: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/assessments', methods=['POST'])
@csrf.exempt
@admin_required
def create_assessment_api():
    """Create a new assessment for a class."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        class_id = data.get('class_id')
        name = data.get('name')

        if not class_id or not name:
            return jsonify({"error": "class_id and name are required"}), 400

        assessment = create_assessment(
            class_id=class_id,
            name=name,
            assessment_type=data.get('type', 'exam'),
            max_score=data.get('max_score', 100),
            weight=data.get('weight'),
            due_date=data.get('due_date'),
            description=data.get('description')
        )

        if assessment:
            return jsonify(assessment), 201
        else:
            return jsonify({"error": "Failed to create assessment"}), 500

    except Exception as e:
        logger.error(f"Error creating assessment: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/assessments/<assessment_id>', methods=['PUT'])
@csrf.exempt
@admin_required
def update_assessment_api(assessment_id):
    """Update an assessment."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        success = update_assessment(assessment_id, **data)

        if success:
            return jsonify({"message": "Assessment updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update assessment"}), 500

    except Exception as e:
        logger.error(f"Error updating assessment: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/assessments/<assessment_id>', methods=['DELETE'])
@csrf.exempt
@admin_required
def delete_assessment_api(assessment_id):
    """Delete an assessment."""
    try:
        success = delete_assessment(assessment_id)

        if success:
            return jsonify({"message": "Assessment deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete assessment"}), 500

    except Exception as e:
        logger.error(f"Error deleting assessment: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/assessments/<assessment_id>/stats', methods=['GET'])
@admin_required
def get_assessment_stats_api(assessment_id):
    """Get statistics for an assessment."""
    try:
        stats = get_assessment_stats(assessment_id)
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error fetching assessment stats: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


# --- Grade API Endpoints ---

@app.route('/api/admin/grades/<assessment_id>', methods=['GET'])
@admin_required
def get_grades_api(assessment_id):
    """Get all grades for an assessment."""
    try:
        grades = get_grades_by_assessment(assessment_id)
        return jsonify(grades), 200
    except Exception as e:
        logger.error(f"Error fetching grades: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/grades/class/<class_id>', methods=['GET'])
@admin_required
def get_class_grades_api(class_id):
    """Get all students with their grades for a class."""
    try:
        assessment_id = request.args.get('assessment_id')
        students = get_student_grades_for_class(class_id, assessment_id)
        return jsonify(students), 200
    except Exception as e:
        logger.error(f"Error fetching class grades: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/grades', methods=['POST'])
@csrf.exempt
@admin_required
def upsert_grade_api():
    """Create or update a student grade."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        student_id = data.get('student_id')
        assessment_id = data.get('assessment_id')

        if not student_id or not assessment_id:
            return jsonify({"error": "student_id and assessment_id are required"}), 400

        grade = upsert_student_grade(
            student_id=student_id,
            assessment_id=assessment_id,
            score=data.get('score'),
            submitted_at=data.get('submitted_at'),
            notes=data.get('notes'),
            feedback=data.get('feedback'),
            file_path=data.get('file_path')
        )

        if grade:
            return jsonify(grade), 200
        else:
            return jsonify({"error": "Failed to save grade"}), 500

    except Exception as e:
        logger.error(f"Error upserting grade: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@app.route('/api/admin/grades/bulk', methods=['POST'])
@csrf.exempt
@admin_required
def bulk_upsert_grades_api():
    """Bulk create/update grades for an assessment."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        assessment_id = data.get('assessment_id')
        grades = data.get('grades', [])

        if not assessment_id:
            return jsonify({"error": "assessment_id is required"}), 400

        if not isinstance(grades, list):
            return jsonify({"error": "grades must be a list"}), 400

        result = bulk_upsert_grades(assessment_id, grades)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error bulk upserting grades: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8788)