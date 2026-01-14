"""Admin dashboard and management routes."""
import os
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash
import logging

from ..utils.auth import (
    generate_admin_token, admin_required, admin_page_required, is_admin_authenticated
)
from ..utils.validation import validate_input
from ..config import JWT_EXPIRATION_HOURS, COURSES

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)

# Import rate limiter from the main app (will be set during registration)
limiter = None


def init_admin_routes(app_limiter):
    """Initialize the admin blueprint with the app's rate limiter."""
    global limiter
    limiter = app_limiter


@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page and handler."""
    # Rate limiting is applied via decorator in main app
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not username or not password:
                logger.warning("Login attempt with empty credentials")
                return render_template('admin_login.html', error='Username and password are required')

            admin_username = os.environ.get('ADMIN_USERNAME', '')
            admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH', '')

            if not admin_username or not admin_password_hash:
                logger.error("Admin credentials not properly configured")
                return render_template('admin_login.html', error='Server misconfiguration')

            if username == admin_username and check_password_hash(admin_password_hash, password):
                token = generate_admin_token()
                response = redirect(url_for('admin.admin_dashboard'))

                response.set_cookie(
                    'admin_token',
                    token,
                    max_age=JWT_EXPIRATION_HOURS * 3600,
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                session['logged_in'] = True
                session['is_admin'] = True

                logger.info(f"Admin login successful for user {username}")
                return response

            logger.warning(f"Failed login attempt for user: {username}")
            return render_template('admin_login.html', error='Invalid username or password')

        except Exception as e:
            logger.error(f"Error in admin login: {e}", exc_info=True)
            return render_template('admin_login.html', error='An error occurred')

    return render_template('admin_login.html')


@admin_bp.route('/admin')
def admin_redirect():
    """Redirect /admin to dashboard or login."""
    if is_admin_authenticated():
        return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('admin.admin_login'))


@admin_bp.route('/admin_dashboard')
@admin_page_required
def admin_dashboard():
    """Admin dashboard page."""
    return render_template('admin_dashboard.html', courses=COURSES)


@admin_bp.route('/admin_roster')
@admin_page_required
def admin_roster():
    """Student roster management page."""
    return render_template('admin_student_roster.html')


@admin_bp.route('/admin_submissions')
@admin_page_required
def admin_submissions():
    """Submissions viewer page."""
    return render_template('admin_submissions.html')


@admin_bp.route('/admin_resources')
@admin_page_required
def admin_resources():
    """Resource management page."""
    return render_template('admin_resources.html', courses=COURSES)


@admin_bp.route('/admin_class_records')
@admin_page_required
def admin_class_records():
    """Class records management page - track exam submissions and scores."""
    return render_template('admin_class_records.html')


@admin_bp.route('/admin_logout')
def admin_logout():
    """Admin logout handler."""
    session.pop('logged_in', None)
    session.pop('is_admin', None)

    response = redirect(url_for('admin.admin_login'))
    response.delete_cookie('admin_token')

    logger.info("Admin logged out")
    return response
