"""Group management API routes."""
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import logging

from ..utils.auth import admin_required, group_required, admin_or_group_required
from ..utils.validation import validate_input

logger = logging.getLogger(__name__)

groups_bp = Blueprint('groups', __name__)


@groups_bp.route('/api/groups', methods=['POST'])
def create_group_api():
    """Create a new group."""
    try:
        from supabase_client import (
            get_supabase_client, create_group, assign_student_to_group,
            update_group_credentials
        )
    except ImportError:
        return jsonify({"error": "Database module not available"}), 500

    supabase_client = get_supabase_client()
    if not supabase_client:
        logger.error("Supabase client not configured")
        return jsonify({"error": "Database not configured"}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        group_name = data.get('group_name', '').strip()
        project_title = data.get('project_title', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        class_id = data.get('class_id', '').strip()
        member_ids = data.get('member_ids', data.get('members', []))

        # Validate inputs
        is_valid, error_msg = validate_input(group_name, 100, "group_name")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        if project_title:
            is_valid, error_msg = validate_input(project_title, 255, "project_title")
            if not is_valid:
                return jsonify({"error": error_msg}), 400

        if not username:
            return jsonify({"error": "Username is required"}), 400

        is_valid, error_msg = validate_input(username, 100, "username")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        if not password or len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        if class_id:
            is_valid, error_msg = validate_input(class_id, 50, "class_id")
            if not is_valid:
                return jsonify({"error": error_msg}), 400

        if not isinstance(member_ids, list):
            return jsonify({"error": "members must be a list"}), 400

        if len(member_ids) > 50:
            return jsonify({"error": "Too many members (max 50)"}), 400

        # Create the group
        new_group = create_group(group_name, project_title, class_id)
        if new_group:
            group_id = new_group['id']
            logger.info(f"Created group {group_id} with name '{group_name}'")

            for student_id in member_ids:
                try:
                    if assign_student_to_group(group_id, student_id):
                        logger.info(f"Assigned student {student_id} to group {group_id}")
                except Exception as e:
                    logger.warning(f"Error assigning student {student_id}: {e}")

            password_hash = generate_password_hash(password)
            if update_group_credentials(group_id, username, password_hash):
                logger.info(f"Set credentials for group {group_id}")
                return jsonify(new_group), 201

            return jsonify({"error": "Failed to set group credentials"}), 500

        return jsonify({"error": "Failed to create group"}), 500

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error creating group: {e}", exc_info=True)

        if "duplicate key" in error_msg and "username" in error_msg:
            return jsonify({"error": "Username already exists"}), 400
        elif "23505" in error_msg:
            return jsonify({"error": "Username already taken"}), 400

        return jsonify({"error": "Failed to create group"}), 500


@groups_bp.route('/api/groups', methods=['GET'])
def get_groups_api():
    """Get all groups."""
    try:
        from supabase_client import get_supabase_client, get_groups
    except ImportError:
        return jsonify({"error": "Database module not available"}), 500

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        groups = get_groups()
        return jsonify(groups), 200
    except Exception as e:
        logger.error(f"Error getting groups: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@groups_bp.route('/api/groups/<group_id>', methods=['GET'])
def get_group_details_api(group_id: str):
    """Get details for a specific group."""
    try:
        from supabase_client import get_supabase_client, get_group_with_submissions
    except ImportError:
        return jsonify({"error": "Database module not available"}), 500

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        group_details = get_group_with_submissions(group_id)
        if group_details:
            return jsonify(group_details), 200
        return jsonify({"error": "Group not found"}), 404
    except Exception as e:
        logger.error(f"Error getting group details: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@groups_bp.route('/api/groups/<group_id>', methods=['DELETE'])
@admin_required
def delete_group_api(group_id: str):
    """Delete a group (admin only)."""
    try:
        from supabase_client import get_supabase_client, delete_group
    except ImportError:
        return jsonify({"error": "Database module not available"}), 500

    supabase_client = get_supabase_client()
    if not supabase_client:
        return jsonify({"error": "Database not configured"}), 500

    try:
        is_valid, error_msg = validate_input(group_id, 255, "group_id")
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        success = delete_group(group_id)
        if success:
            logger.info(f"Group {group_id} deleted successfully")
            return jsonify({"message": "Group deleted successfully"}), 200

        return jsonify({"error": "Failed to delete group"}), 500
    except Exception as e:
        logger.error(f"Error deleting group: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


@groups_bp.route('/api/groups/<group_id>/members', methods=['GET'])
def get_group_members_api(group_id: str):
    """Get all members of a group."""
    try:
        from supabase_client import get_group_members
    except ImportError:
        return jsonify({"error": "Database module not available"}), 500

    try:
        members = get_group_members(group_id)
        return jsonify(members), 200
    except Exception as e:
        logger.error(f"Error getting group members: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500


# --- GROUP AUTHENTICATION & PORTAL ---

@groups_bp.route('/group_login', methods=['GET', 'POST'])
def group_login():
    """Group login page."""
    if request.method == 'POST':
        try:
            from supabase_client import get_group_by_username, update_group_last_login

            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not username or not password:
                return render_template('group_login.html', error='Username and password are required')

            group = get_group_by_username(username)
            if not group:
                logger.warning(f"Login attempt with non-existent username: {username}")
                return render_template('group_login.html', error='Invalid username or password')

            if not check_password_hash(group.get('password_hash', ''), password):
                logger.warning(f"Failed login attempt for group: {username}")
                return render_template('group_login.html', error='Invalid username or password')

            session['group_id'] = group['id']
            session['group_name'] = group['group_name']
            session['is_group_logged_in'] = True

            update_group_last_login(group['id'])

            logger.info(f"Group login successful: {username}")
            return redirect(url_for('groups.group_submission_portal'))

        except Exception as e:
            logger.error(f"Error in group login: {e}", exc_info=True)
            return render_template('group_login.html', error='An error occurred')

    return render_template('group_login.html')


@groups_bp.route('/group_portal')
def group_portal():
    """Group portal page."""
    return render_template('group_portal_enhanced.html', is_admin=False)


@groups_bp.route('/group_submission_portal')
def group_submission_portal():
    """Group project submission portal."""
    if not session.get('is_group_logged_in'):
        logger.warning("Unauthorized access to group submission portal")
        return redirect(url_for('groups.group_login'))

    try:
        from supabase_client import get_group_with_submissions, get_class_by_id
        from ..config import PROJECTS, COURSES, COURSE_PROJECTS

        group_id = session.get('group_id')
        group_data = get_group_with_submissions(group_id)

        if not group_data:
            session.clear()
            return redirect(url_for('groups.group_login'))

        # Derive project from group's class
        project_id = 'ml-research-project'  # Default fallback
        course_id = 'cmsc173'  # Default fallback

        class_id = group_data.get('class_id')
        if class_id:
            class_data = get_class_by_id(class_id)
            if class_data:
                course_code = class_data.get('course_code', '')
                # Map course_code to project_id
                project_id = COURSE_PROJECTS.get(course_code, 'ml-research-project')
                # Derive course_id from project
                project_config = PROJECTS.get(project_id, {})
                course_id = project_config.get('course', 'cmsc173')

        project = PROJECTS.get(project_id, PROJECTS.get('ml-research-project', {}))
        course = COURSES.get(course_id, COURSES.get('cmsc173', {}))

        return render_template('group_submission_portal.html',
            group=group_data,
            project=project,
            course=course,
            is_admin=False
        )
    except Exception as e:
        logger.error(f"Error loading group submission portal: {e}", exc_info=True)
        return render_template('error.html', error='Error loading portal'), 500


@groups_bp.route('/group_logout')
def group_logout():
    """Group logout handler."""
    group_name = session.get('group_name', 'Unknown')
    session.pop('group_id', None)
    session.pop('group_name', None)
    session.pop('is_group_logged_in', None)

    logger.info(f"Group {group_name} logged out")
    return redirect(url_for('groups.group_login'))
