"""Authentication utilities for admin and group sessions."""
from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt
from flask import request, session, jsonify, current_app
from ..config import JWT_ALGORITHM, JWT_EXPIRATION_HOURS


def generate_admin_token():
    """Generate a JWT token for authenticated admin sessions."""
    now = datetime.now(timezone.utc)
    payload = {
        'is_admin': True,
        'exp': now + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': now
    }
    token = jwt.encode(payload, current_app.secret_key, algorithm=JWT_ALGORITHM)
    return token


def verify_admin_token(token):
    """Verify JWT token and return True if valid admin token."""
    try:
        payload = jwt.decode(token, current_app.secret_key, algorithms=[JWT_ALGORITHM])
        return payload.get('is_admin') == True
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False


def get_admin_token_from_request():
    """Extract JWT token from request (cookie or header)."""
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
    """Check if current request is from authenticated admin."""
    token = get_admin_token_from_request()
    if token and verify_admin_token(token):
        return True
    # Fallback to session for backwards compatibility
    return session.get('is_admin') == True


def admin_required(f):
    """Decorator to require admin authentication for API routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin_authenticated():
            return jsonify({"error": "Admin authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_page_required(f):
    """Decorator to require admin authentication for page routes (redirects to login)."""
    from flask import redirect, url_for
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin_authenticated():
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def group_required(f):
    """Decorator to require group authentication via session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('group_id'):
            return jsonify({"error": "Group login required"}), 401
        return f(*args, **kwargs)
    return decorated_function


def group_owner_required(f):
    """Decorator to require that logged-in group owns the resource."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        group_id = kwargs.get('group_id')
        session_group_id = session.get('group_id')

        if not session_group_id:
            return jsonify({"error": "Group login required"}), 401

        if str(session_group_id) != str(group_id):
            return jsonify({"error": "Access denied to this group"}), 403

        return f(*args, **kwargs)
    return decorated_function


def admin_or_group_required(f):
    """Decorator to allow admin OR the owning group."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Admins always allowed
        if is_admin_authenticated():
            return f(*args, **kwargs)

        # Check if logged-in group owns resource
        group_id = kwargs.get('group_id')
        if session.get('group_id') and str(session.get('group_id')) == str(group_id):
            return f(*args, **kwargs)

        return jsonify({"error": "Access denied"}), 403
    return decorated_function


def get_current_user():
    """Get currently authenticated user info."""
    if is_admin_authenticated():
        return {'type': 'admin', 'id': None}
    if session.get('group_id'):
        return {'type': 'group', 'id': session['group_id']}
    if session.get('student_id'):
        return {'type': 'student', 'id': session['student_id']}
    return None
