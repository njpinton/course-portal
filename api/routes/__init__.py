"""Flask blueprints for the API routes.

This module provides modular route organization using Flask Blueprints.
Import blueprints from here and register them with the Flask app.

Usage:
    from api.routes import register_blueprints
    register_blueprints(app, limiter)
"""
from flask import Blueprint

# Import blueprints from modules
from .admin import admin_bp
from .courses import courses_bp
from .groups import groups_bp

# Blueprint definitions for routes still in index.py
# These will be populated as more routes are refactored
students_bp = Blueprint('students', __name__, url_prefix='/api')
submissions_bp = Blueprint('submissions', __name__, url_prefix='/api')
resources_bp = Blueprint('resources', __name__, url_prefix='/api')


def register_blueprints(app, limiter=None):
    """Register all blueprints with the Flask app.

    Args:
        app: Flask application instance
        limiter: Optional Flask-Limiter instance for rate limiting
    """
    # Initialize blueprints that need the limiter
    if limiter:
        from .admin import init_admin_routes
        init_admin_routes(limiter)

        # Apply rate limiting to login routes
        @limiter.limit("5 per minute", methods=["POST"])
        def limit_admin_login():
            pass

        @limiter.limit("10 per minute", methods=["POST"])
        def limit_group_login():
            pass

    # Register blueprints
    app.register_blueprint(courses_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(groups_bp)

    # These blueprints are defined but routes remain in index.py for now
    # Uncomment as routes are migrated:
    # app.register_blueprint(students_bp)
    # app.register_blueprint(submissions_bp)
    # app.register_blueprint(resources_bp)


__all__ = [
    'admin_bp',
    'courses_bp',
    'groups_bp',
    'students_bp',
    'submissions_bp',
    'resources_bp',
    'register_blueprints',
]
