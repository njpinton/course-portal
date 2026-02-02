"""Course and module display routes."""
import os
from flask import Blueprint, render_template, send_from_directory
import logging

from ..config import COURSES, PROJECTS, MODULE_CATEGORIES

logger = logging.getLogger(__name__)

courses_bp = Blueprint('courses', __name__)


def get_available_modules(course_id: str = None) -> dict:
    """Dynamically discover available module templates for a course.

    Args:
        course_id: The course identifier (e.g., 'cmsc173').

    Returns:
        Dict of available modules keyed by module number.
    """
    if not course_id:
        return {}

    course = COURSES.get(course_id)
    if not course:
        return {}

    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'courses', course_id)
    available = {}

    for module_num, module_info in course.get('modules', {}).items():
        filename = module_info['filename']
        filepath = os.path.join(templates_dir, filename)

        if os.path.exists(filepath):
            available[module_num] = module_info

    return available


@courses_bp.route('/')
def index():
    """Course Hub - main landing page with all courses."""
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


@courses_bp.route('/course/<course_id>')
def course_detail(course_id: str):
    """Course detail page with modules and projects."""
    if course_id not in COURSES:
        return render_template('error.html', error='Course not found'), 404

    course = COURSES[course_id]
    course_projects = [PROJECTS[pid] for pid in course.get('projects', []) if pid in PROJECTS]

    return render_template('course_detail.html',
        course=course,
        course_id=course_id,
        projects=course_projects,
        categories=MODULE_CATEGORIES,
        courses=COURSES,
        active_course=course_id
    )


@courses_bp.route('/course/<course_id>/module/<module_id>')
def show_module(course_id: str, module_id: str):
    """Display a specific module for a course."""
    try:
        module_number = int(module_id)
    except ValueError:
        module_number = module_id

    course = COURSES.get(course_id)
    if not course:
        return render_template('error.html',
            error_title="Course Not Found",
            error_message=f"Course '{course_id}' does not exist.",
            back_url="/",
            back_text="Back to Course Hub"
        ), 404

    available_modules = get_available_modules(course_id)

    if module_number not in available_modules:
        return render_template('error.html',
            error_title="Module Not Found",
            error_message=f"Module {module_number} not found in {course['code']}.",
            back_url=f"/course/{course_id}",
            back_text=f"Back to {course['code']}"
        ), 404

    # Optional: Track view count via Supabase
    view_count = 0
    try:
        from api.utils.supabase_client import get_supabase_client
        supabase_client = get_supabase_client()
        if supabase_client:
            supabase_client.rpc('increment_module_view', {'module_id': module_number}).execute()
            response = supabase_client.table('module_views').select('view_count').eq('module_number', module_number).execute()
            if response.data:
                view_count = response.data[0]['view_count']
            logger.info(f"Course {course_id} Module {module_number} view count: {view_count}")
    except Exception as e:
        logger.error(f"Error tracking module view: {e}", exc_info=True)
        view_count = 0

    module = available_modules[module_number]
    template_path = f"courses/{course_id}/{module['filename']}"
    return render_template(template_path, view_count=view_count, course=course, course_id=course_id)


@courses_bp.route('/favicon.ico')
def favicon():
    """Return empty favicon to avoid 404s."""
    return '', 204


@courses_bp.route('/images/<path:filename>')
def serve_images(filename: str):
    """Serve images from the images directory."""
    images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
    return send_from_directory(images_dir, filename)
