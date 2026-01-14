"""Application configuration and constants."""
import os
import secrets
import logging
from dotenv import load_dotenv

# Load environment variables
if os.path.exists('.env.local'):
    load_dotenv('.env.local')
load_dotenv('.env')

logger = logging.getLogger(__name__)

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

# JWT configuration
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# Module definitions (legacy - use COURSES[course_id]["modules"] instead)
# This is kept for backwards compatibility but should be deprecated
MODULES = {}

# Course definitions - scalable structure for multiple courses
# Note: Module filenames are relative to api/templates/courses/<course_id>/
COURSES = {
    "cmsc173": {
        "code": "CMSC 173",
        "title": "Machine Learning",
        "description": "Fundamentals of machine learning algorithms and applications",
        "icon": "brain",
        "color": "#1B5E4F",
        "modules": {
            "intro": {"title": "Welcome to CMSC 173", "filename": "intro-welcome.html", "category": "fundamentals"},
            0: {"title": "Introduction to Machine Learning", "filename": "00-intro-combined.html", "category": "fundamentals"},
            1: {"title": "Parameter Estimation", "filename": "01-parameter-estimation.html", "category": "fundamentals"},
            2: {"title": "Linear Regression", "filename": "02-linear-regression.html", "category": "fundamentals"},
            3: {"title": "Regularization", "filename": "03-regularization.html", "category": "fundamentals"},
            4: {"title": "Exploratory Data Analysis", "filename": "04-eda.html", "category": "model-selection"},
            5: {"title": "Model Selection", "filename": "05-model-selection.html", "category": "model-selection"},
            6: {"title": "Cross Validation", "filename": "06-cross-validation.html", "category": "model-selection"},
            7: {"title": "PCA", "filename": "07-pca.html", "category": "classification"},
            8: {"title": "Logistic Regression", "filename": "08-logistic-regression.html", "category": "classification"},
            9: {"title": "Classification", "filename": "09-classification.html", "category": "classification"},
            10: {"title": "Kernel Methods", "filename": "10-kernel-methods.html", "category": "classification"},
            11: {"title": "Clustering", "filename": "11-clustering.html", "category": "deep-learning"},
            12: {"title": "Neural Networks", "filename": "12-neural-networks.html", "category": "deep-learning"},
            13: {"title": "Advanced Neural Networks", "filename": "13-advanced-nn.html", "category": "deep-learning"},
        },
        "projects": ["ml-research-project"],
        "is_active": True,
    },
    "cmsc178": {
        "code": "CMSC 178",
        "title": "Digital Image Processing",
        "description": "Fundamentals of digital image processing and computer vision",
        "icon": "image",
        "color": "#4A90A4",
        "modules": {
            1: {"title": "Introduction to Digital Image Processing", "filename": "01-introduction.html", "category": "fundamentals"},
            2: {"title": "Storage and Compression", "filename": "02-storage-compression.html", "category": "fundamentals"},
            3: {"title": "Image Processing Fundamentals", "filename": "03-fundamentals.html", "category": "fundamentals"},
            4: {"title": "Image Enhancement and Filtering", "filename": "04-enhancement-filtering.html", "category": "enhancement"},
            5: {"title": "Image Restoration", "filename": "05-restoration.html", "category": "enhancement"},
            6: {"title": "Geometric Transformations", "filename": "06-geometric-transformations.html", "category": "transformations"},
            7: {"title": "Feature Extraction", "filename": "07-feature-extraction.html", "category": "transformations"},
            8: {"title": "Segmentation and Morphology", "filename": "08-segmentation-morphology.html", "category": "segmentation"},
            9: {"title": "Computer Vision & Deep Learning I", "filename": "09-cv-deep-learning-1.html", "category": "deep-learning"},
            10: {"title": "Computer Vision & Deep Learning II", "filename": "10-cv-deep-learning-2.html", "category": "deep-learning"},
            11: {"title": "Generative Models", "filename": "11-generative-models.html", "category": "deep-learning"},
        },
        "projects": ["dip-research-project"],
        "is_active": True,
    },
}

# Project definitions - tracks group projects across courses
PROJECTS = {
    "ml-research-project": {
        "id": "ml-research-project",
        "title": "ML Research Project",
        "description": "Apply machine learning to a real-world research problem",
        "course": "cmsc173",
        "stages": 5,
        "stage_names": [
            "Problem Definition",
            "Data Collection & EDA",
            "Model Development",
            "Evaluation & Analysis",
            "Final Presentation"
        ],
    },
    "dip-research-project": {
        "id": "dip-research-project",
        "title": "DIP Research Project",
        "description": "Apply image processing techniques to a real-world problem",
        "course": "cmsc178",
        "stages": 5,
        "stage_names": [
            "Problem Definition",
            "Data Collection & Preprocessing",
            "Algorithm Implementation",
            "Evaluation & Analysis",
            "Final Presentation"
        ],
    },
}

# Module categories for grouping in UI
# Note: Categories are shared across courses - add course-specific ones as needed
MODULE_CATEGORIES = {
    # Shared categories
    "fundamentals": {"title": "Fundamentals", "order": 1},
    "deep-learning": {"title": "Deep Learning", "order": 4},
    # CMSC 173 - Machine Learning categories
    "model-selection": {"title": "Model Selection & Validation", "order": 2},
    "classification": {"title": "Classification Methods", "order": 3},
    # CMSC 178 - Digital Image Processing categories
    "enhancement": {"title": "Image Enhancement", "order": 2},
    "transformations": {"title": "Transformations & Features", "order": 3},
    "segmentation": {"title": "Segmentation", "order": 3},
}


def get_secret_key():
    """Get or generate Flask secret key."""
    secret_key = os.environ.get('FLASK_SECRET_KEY')
    if not secret_key:
        is_production = os.environ.get('VERCEL_ENV') == 'production'
        if is_production:
            vercel_url = os.environ.get('VERCEL_URL', 'localhost')
            secret_key = f"vercel-{vercel_url}-{os.environ.get('VERCEL_GIT_COMMIT_SHA', 'dev')[:16]}"
            logger.warning("Using derived FLASK_SECRET_KEY from Vercel environment.")
        else:
            secret_key = secrets.token_urlsafe(32)
            logger.warning("Generated temporary FLASK_SECRET_KEY for development.")
    return secret_key
