"""Database client using SQLAlchemy for PostgreSQL operations.

This module provides database abstraction for the presenter app,
replacing Supabase client with direct PostgreSQL queries via SQLAlchemy.
"""
import os
import json
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Union
from sqlalchemy import text
from database import (
    execute_raw_sql, execute_insert, execute_update,
    row_to_dict, rows_to_dicts, get_db_context
)

logger = logging.getLogger(__name__)

# Database connection check
def get_supabase_client():
    """Compatibility function - returns True if database is configured."""
    return os.environ.get('DATABASE_URL') is not None

def get_supabase_admin_client():
    """Compatibility function for admin operations."""
    return os.environ.get('DATABASE_URL') is not None


# --- Group CRUD Operations ---

def create_group(group_name: str, project_title: str, class_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Create a new group."""
    try:
        query = """
            INSERT INTO groups (group_name, project_title, class_id, is_active, created_at)
            VALUES (:group_name, :project_title, :class_id, TRUE, NOW())
            RETURNING *
        """
        params = {
            'group_name': group_name,
            'project_title': project_title,
            'class_id': class_id
        }

        with get_db_context() as db:
            result = db.execute(text(query), params)
            group = result.fetchone()
            logger.info(f"Group created: {group.id if group else 'unknown'}")
            return row_to_dict(group)
    except Exception as e:
        logger.error(f"Error creating group '{group_name}': {e}", exc_info=True)
        return None


def add_group_member(group_id: str, member_name: str, student_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Add a member to a group."""
    try:
        query = """
            INSERT INTO group_members (group_id, member_name, student_id, created_at)
            VALUES (:group_id, :member_name, :student_id, NOW())
            RETURNING *
        """
        params = {
            'group_id': group_id,
            'member_name': member_name,
            'student_id': student_id
        }

        with get_db_context() as db:
            result = db.execute(text(query), params)
            member = result.fetchone()
            logger.info(f"Member '{member_name}' (student ID: {student_id}) added to group {group_id}")
            return row_to_dict(member)
    except Exception as e:
        logger.error(f"Error adding member '{member_name}' to group {group_id}: {e}", exc_info=True)
        return None


def add_group_document(group_id: str, document_title: str, file_path: str) -> Optional[Dict[str, Any]]:
    """Add a document to a group."""
    try:
        query = """
            INSERT INTO group_documents (group_id, document_title, file_path, created_at)
            VALUES (:group_id, :document_title, :file_path, NOW())
            RETURNING *
        """
        params = {
            'group_id': group_id,
            'document_title': document_title,
            'file_path': file_path
        }

        with get_db_context() as db:
            result = db.execute(text(query), params)
            document = result.fetchone()
            logger.info(f"Document '{document_title}' added to group {group_id}")
            return row_to_dict(document)
    except Exception as e:
        logger.error(f"Error adding document to group {group_id}: {e}", exc_info=True)
        return None


def get_groups() -> List[Dict[str, Any]]:
    """Get all active groups with members, using batch queries to avoid N+1."""
    try:
        # Query 1: Get all active groups
        groups_query = "SELECT * FROM groups WHERE is_active = TRUE ORDER BY created_at DESC"
        groups = rows_to_dicts(execute_raw_sql(groups_query))

        if not groups:
            return []

        # Collect all group IDs for batch query
        group_ids = [g['id'] for g in groups if g.get('id')]

        # Query 2: Batch fetch all members for all groups
        members_query = """
            SELECT * FROM group_members
            WHERE group_id = ANY(:group_ids)
            ORDER BY created_at
        """
        all_members = execute_raw_sql(members_query, {'group_ids': group_ids})
        all_members = rows_to_dicts(all_members)

        # Collect all student IDs for batch query
        student_ids = list(set(m['student_id'] for m in all_members if m.get('student_id')))

        # Query 3: Batch fetch all students
        students_map = {}
        if student_ids:
            students_query = """
                SELECT id, first_name, last_name, email, campus_id
                FROM students
                WHERE id = ANY(:student_ids)
            """
            students = execute_raw_sql(students_query, {'student_ids': student_ids})
            students_map = {s.id: row_to_dict(s) for s in students}

        # Build members map by group_id
        members_by_group = {}
        for member in all_members:
            group_id = member.get('group_id')
            if group_id not in members_by_group:
                members_by_group[group_id] = []

            # Enrich member with student data
            student_id = member.get('student_id')
            if student_id and student_id in students_map:
                student = students_map[student_id]
                member['first_name'] = student.get('first_name', '')
                member['last_name'] = student.get('last_name', '')
                member['member_name'] = f"{student.get('first_name', '')} {student.get('last_name', '')}".strip()
                member['email'] = student.get('email', '')
                member['campus_id'] = student.get('campus_id', '')

            members_by_group[group_id].append(member)

        # Attach members to groups
        for group in groups:
            group['group_members'] = members_by_group.get(group.get('id'), [])

        logger.info(f"Retrieved {len(groups)} groups with enriched member data (3 queries)")
        return groups
    except Exception as e:
        logger.error(f"Error getting groups: {e}", exc_info=True)
        return []


def get_group_details(group_id: str) -> Optional[Dict[str, Any]]:
    """Get detailed information about a specific group."""
    try:
        # Get group
        group_query = "SELECT * FROM groups WHERE id = :group_id"
        group_rows = execute_raw_sql(group_query, {'group_id': group_id})

        if not group_rows:
            return None

        group = row_to_dict(group_rows[0])

        # Get members
        members_query = "SELECT * FROM group_members WHERE group_id = :group_id"
        members = rows_to_dicts(execute_raw_sql(members_query, {'group_id': group_id}))

        # Get documents
        docs_query = "SELECT * FROM group_documents WHERE group_id = :group_id"
        documents = rows_to_dicts(execute_raw_sql(docs_query, {'group_id': group_id}))

        group['members'] = members
        group['documents'] = documents

        logger.info(f"Retrieved group {group_id} with {len(members)} members and {len(documents)} documents")
        return group
    except Exception as e:
        logger.error(f"Error getting group details for {group_id}: {e}", exc_info=True)
        return None


def delete_group(group_id: str) -> bool:
    """Delete a group and all associated data."""
    try:
        with get_db_context() as db:
            # Delete associated documents
            db.execute(text("DELETE FROM group_documents WHERE group_id = :group_id"), {'group_id': group_id})
            # Delete associated members
            db.execute(text("DELETE FROM group_members WHERE group_id = :group_id"), {'group_id': group_id})
            # Delete associated submissions
            db.execute(text("DELETE FROM group_submissions WHERE group_id = :group_id"), {'group_id': group_id})
            # Delete the group itself
            result = db.execute(text("DELETE FROM groups WHERE id = :group_id RETURNING id"), {'group_id': group_id})
            deleted = result.fetchone()

            logger.info(f"Group {group_id} deleted successfully")
            return deleted is not None
    except Exception as e:
        logger.error(f"Error deleting group {group_id}: {e}", exc_info=True)
        return False


# --- Project Stages & Tracking ---

def get_project_stages(group_id: str) -> List[Dict[str, Any]]:
    """Fetch all project stages for a group."""
    try:
        query = """
            SELECT * FROM project_stages
            WHERE group_id = :group_id
            ORDER BY stage_number ASC
        """
        stages = rows_to_dicts(execute_raw_sql(query, {'group_id': group_id}))
        logger.info(f"Retrieved {len(stages)} stages for group {group_id}")
        return stages
    except Exception as e:
        logger.error(f"Error getting project stages for group {group_id}: {e}", exc_info=True)
        return []


def update_stage_status(stage_id: str, status: str, grade: Optional[float] = None, feedback: Optional[str] = None) -> bool:
    """Update project stage status, grade, and feedback."""
    try:
        query = """
            UPDATE project_stages
            SET status = :status,
                grade = COALESCE(:grade, grade),
                feedback = COALESCE(:feedback, feedback),
                updated_at = NOW()
            WHERE id = :stage_id
            RETURNING id
        """
        params = {
            'stage_id': stage_id,
            'status': status,
            'grade': grade,
            'feedback': feedback
        }

        rows_affected = execute_update(query, params)
        logger.info(f"Stage {stage_id} updated with status: {status}")
        return rows_affected > 0
    except Exception as e:
        logger.error(f"Error updating stage {stage_id}: {e}", exc_info=True)
        return False


def get_project_models(group_id: str) -> List[Dict[str, Any]]:
    """Fetch all trained models for a group."""
    try:
        query = """
            SELECT * FROM project_models
            WHERE group_id = :group_id
            ORDER BY created_at DESC
        """
        models = rows_to_dicts(execute_raw_sql(query, {'group_id': group_id}))
        logger.info(f"Retrieved {len(models)} models for group {group_id}")
        return models
    except Exception as e:
        logger.error(f"Error getting project models for group {group_id}: {e}", exc_info=True)
        return []


def add_project_model(group_id: str, model_name: str, model_type: str, metrics: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add a trained model result to the database."""
    try:
        # Build dynamic columns based on metrics
        metric_cols = ', '.join(metrics.keys())
        metric_vals = ', '.join(f":{k}" for k in metrics.keys())

        query = f"""
            INSERT INTO project_models (group_id, model_name, model_type, {metric_cols}, created_at)
            VALUES (:group_id, :model_name, :model_type, {metric_vals}, NOW())
            RETURNING *
        """

        params = {
            'group_id': group_id,
            'model_name': model_name,
            'model_type': model_type,
            **metrics
        }

        with get_db_context() as db:
            result = db.execute(text(query), params)
            model = result.fetchone()
            logger.info(f"Model '{model_name}' added for group {group_id}")
            return row_to_dict(model)
    except Exception as e:
        logger.error(f"Error adding model '{model_name}' for group {group_id}: {e}", exc_info=True)
        return None


def get_stage_documents(group_id: str, stage_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch documents for a specific stage or all stages."""
    try:
        if stage_id:
            query = """
                SELECT * FROM stage_documents
                WHERE group_id = :group_id AND stage_id = :stage_id
                ORDER BY created_at DESC
            """
            params = {'group_id': group_id, 'stage_id': stage_id}
        else:
            query = """
                SELECT * FROM stage_documents
                WHERE group_id = :group_id
                ORDER BY created_at DESC
            """
            params = {'group_id': group_id}

        documents = rows_to_dicts(execute_raw_sql(query, params))
        logger.info(f"Retrieved {len(documents)} stage documents for group {group_id}")
        return documents
    except Exception as e:
        logger.error(f"Error getting stage documents for group {group_id}: {e}", exc_info=True)
        return []


def add_stage_document(group_id: str, stage_id: str, document_title: str, document_type: str,
                      file_path: str, file_size: Optional[int] = None, uploaded_by: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Add a document to a specific project stage."""
    try:
        query = """
            INSERT INTO stage_documents
            (group_id, stage_id, document_title, document_type, file_path, file_size, uploaded_by, created_at)
            VALUES (:group_id, :stage_id, :document_title, :document_type, :file_path, :file_size, :uploaded_by, NOW())
            RETURNING *
        """
        params = {
            'group_id': group_id,
            'stage_id': stage_id,
            'document_title': document_title,
            'document_type': document_type,
            'file_path': file_path,
            'file_size': file_size,
            'uploaded_by': uploaded_by
        }

        with get_db_context() as db:
            result = db.execute(text(query), params)
            doc = result.fetchone()
            logger.info(f"Stage document '{document_title}' added for stage {stage_id}")
            return row_to_dict(doc)
    except Exception as e:
        logger.error(f"Error adding stage document '{document_title}': {e}", exc_info=True)
        return None


def update_group_project_info(group_id: str, problem_statement: str = None, dataset_source: str = None,
                              dataset_size: int = None, title: str = None, description: str = None,
                              objectives: str = None, methodology: str = None) -> bool:
    """Update group's project information."""
    try:
        updates = []
        params = {'group_id': group_id}

        if problem_statement is not None:
            updates.append("problem_statement = :problem_statement")
            params['problem_statement'] = problem_statement
        if dataset_source is not None:
            updates.append("dataset_source = :dataset_source")
            params['dataset_source'] = dataset_source
        if dataset_size is not None:
            updates.append("dataset_size = :dataset_size")
            params['dataset_size'] = dataset_size
        if title is not None:
            updates.append("project_title = :project_title")
            params['project_title'] = title
        if description is not None:
            updates.append("project_description = :project_description")
            params['project_description'] = description
        if objectives is not None:
            updates.append("project_objectives = :project_objectives")
            params['project_objectives'] = objectives
        if methodology is not None:
            updates.append("project_methodology = :project_methodology")
            params['project_methodology'] = methodology

        if not updates:
            return True

        query = f"""
            UPDATE groups
            SET {', '.join(updates)}
            WHERE id = :group_id
            RETURNING id
        """

        rows_affected = execute_update(query, params)
        logger.info(f"Project info updated for group {group_id}")
        return rows_affected > 0
    except Exception as e:
        logger.error(f"Error updating group project info for {group_id}: {e}", exc_info=True)
        return False


# --- Group Authentication ---

def update_group_credentials(group_id: str, username: str, password_hash: str) -> bool:
    """Update group credentials (username and password hash)."""
    try:
        query = """
            UPDATE groups
            SET username = :username, password_hash = :password_hash
            WHERE id = :group_id
            RETURNING id
        """
        params = {'group_id': group_id, 'username': username, 'password_hash': password_hash}
        rows_affected = execute_update(query, params)
        logger.info(f"Group credentials updated for {username}")
        return rows_affected > 0
    except Exception as e:
        logger.error(f"Error updating group credentials: {e}", exc_info=True)
        return False


def get_group_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Fetch group by username (only active groups)."""
    try:
        query = "SELECT * FROM groups WHERE username = :username AND is_active = TRUE"
        rows = execute_raw_sql(query, {'username': username})
        if rows:
            logger.info(f"Retrieved group for username: {username}")
            return row_to_dict(rows[0])
        return None
    except Exception as e:
        logger.error(f"Error getting group by username {username}: {e}", exc_info=True)
        return None


def update_group_last_login(group_id: str) -> bool:
    """Update last login timestamp for group."""
    try:
        query = "UPDATE groups SET last_login = NOW() WHERE id = :group_id RETURNING id"
        rows_affected = execute_update(query, {'group_id': group_id})
        logger.info(f"Updated last login for group {group_id}")
        return rows_affected > 0
    except Exception as e:
        logger.error(f"Error updating last login for group {group_id}: {e}", exc_info=True)
        return False


def get_group_with_submissions(group_id: str) -> Optional[Dict[str, Any]]:
    """Get group details with all submissions and feedback."""
    try:
        # Get group
        group_query = "SELECT * FROM groups WHERE id = :group_id"
        group_rows = execute_raw_sql(group_query, {'group_id': group_id})

        if not group_rows:
            return None

        group = row_to_dict(group_rows[0])

        # Get members
        members_query = "SELECT * FROM group_members WHERE group_id = :group_id"
        members = rows_to_dicts(execute_raw_sql(members_query, {'group_id': group_id}))

        # Batch fetch students if needed
        student_ids = list(set(m['student_id'] for m in members if m.get('student_id')))
        students_map = {}
        if student_ids:
            students_query = """
                SELECT id, first_name, last_name, email, campus_id
                FROM students
                WHERE id = ANY(:student_ids)
            """
            students = execute_raw_sql(students_query, {'student_ids': student_ids})
            students_map = {s.id: row_to_dict(s) for s in students}

        # Enrich members with student data
        for member in members:
            student_id = member.get('student_id')
            if student_id and student_id in students_map:
                student = students_map[student_id]
                member['first_name'] = student.get('first_name', '')
                member['last_name'] = student.get('last_name', '')
                member['member_name'] = f"{student.get('first_name', '')} {student.get('last_name', '')}".strip()
                member['email'] = student.get('email', '')
                member['campus_id'] = student.get('campus_id', '')

        group['members'] = members

        # Get submissions
        submissions_query = """
            SELECT * FROM group_submissions
            WHERE group_id = :group_id
            ORDER BY stage_number ASC
        """
        group['submissions'] = rows_to_dicts(execute_raw_sql(submissions_query, {'group_id': group_id}))

        # Get feedback
        feedback_query = "SELECT * FROM group_feedback WHERE group_id = :group_id"
        feedback_rows = execute_raw_sql(feedback_query, {'group_id': group_id})
        group['feedback'] = {fb.stage_number: row_to_dict(fb) for fb in feedback_rows}

        logger.info(f"Retrieved group {group_id} with {len(members)} members")
        return group
    except Exception as e:
        logger.error(f"Error getting group with submissions: {e}", exc_info=True)
        return None


def submit_group_stage_work(group_id: str, stage_id: str, submission_data: dict) -> Optional[Dict[str, Any]]:
    """Submit work for a group stage."""
    try:
        stage_number = submission_data.get('stage_number')
        if not stage_number:
            logger.error("stage_number is required in submission_data")
            return None

        # Check if submission exists
        check_query = """
            SELECT id FROM group_submissions
            WHERE group_id = :group_id AND stage_number = :stage_number
        """
        existing = execute_raw_sql(check_query, {'group_id': group_id, 'stage_number': stage_number})

        if existing:
            # Update existing submission
            update_fields = []
            params = {'group_id': group_id, 'stage_number': stage_number}

            for field in ['summary_markdown', 'presentation_link', 'content', 'file_path',
                         'file_name', 'file_size', 'file_mime_type']:
                if submission_data.get(field):
                    update_fields.append(f"{field} = :{field}")
                    params[field] = submission_data[field]

            if update_fields:
                query = f"""
                    UPDATE group_submissions
                    SET {', '.join(update_fields)}, updated_at = NOW()
                    WHERE group_id = :group_id AND stage_number = :stage_number
                    RETURNING *
                """
                with get_db_context() as db:
                    result = db.execute(text(query), params)
                    submission = result.fetchone()
                    logger.info(f"Updated submission for group {group_id}, stage {stage_number}")
                    return row_to_dict(submission)
        else:
            # Create new submission
            query = """
                INSERT INTO group_submissions
                (group_id, stage_number, summary_markdown, presentation_link, content,
                 file_path, file_name, file_size, file_mime_type, created_at, updated_at)
                VALUES (:group_id, :stage_number, :summary_markdown, :presentation_link, :content,
                        :file_path, :file_name, :file_size, :file_mime_type, NOW(), NOW())
                RETURNING *
            """
            params = {
                'group_id': group_id,
                'stage_number': stage_number,
                'summary_markdown': submission_data.get('summary_markdown'),
                'presentation_link': submission_data.get('presentation_link'),
                'content': submission_data.get('content'),
                'file_path': submission_data.get('file_path'),
                'file_name': submission_data.get('file_name'),
                'file_size': submission_data.get('file_size'),
                'file_mime_type': submission_data.get('file_mime_type')
            }

            with get_db_context() as db:
                result = db.execute(text(query), params)
                submission = result.fetchone()
                logger.info(f"Created submission for group {group_id}, stage {stage_number}")
                return row_to_dict(submission)
    except Exception as e:
        logger.error(f"Error submitting stage work: {e}", exc_info=True)
        return None


def get_group_feedback(group_id: str) -> List[Dict[str, Any]]:
    """Get all feedback for a group."""
    try:
        query = "SELECT * FROM group_feedback WHERE group_id = :group_id ORDER BY stage_number"
        feedback = rows_to_dicts(execute_raw_sql(query, {'group_id': group_id}))
        logger.info(f"Retrieved {len(feedback)} feedback entries for group {group_id}")
        return feedback
    except Exception as e:
        logger.error(f"Error getting feedback for group {group_id}: {e}", exc_info=True)
        return []


# --- Student Operations ---

def get_student_by_id(student_id: str) -> Optional[Dict[str, Any]]:
    """Fetch student by ID."""
    try:
        query = "SELECT * FROM students WHERE id = :student_id"
        rows = execute_raw_sql(query, {'student_id': student_id})
        if rows:
            logger.info(f"Retrieved student record for ID {student_id}")
            return row_to_dict(rows[0])
        return None
    except Exception as e:
        logger.error(f"Error getting student by ID {student_id}: {e}", exc_info=True)
        return None


def get_student_by_campus_id(campus_id: str) -> Optional[Dict[str, Any]]:
    """Fetch student by campus ID."""
    try:
        query = "SELECT * FROM students WHERE campus_id = :campus_id"
        rows = execute_raw_sql(query, {'campus_id': campus_id})
        if rows:
            logger.info(f"Retrieved student record for campus ID {campus_id}")
            return row_to_dict(rows[0])
        return None
    except Exception as e:
        logger.error(f"Error getting student by campus ID {campus_id}: {e}", exc_info=True)
        return None


def get_class_by_code_section(course_code: str, section: str) -> Optional[Dict[str, Any]]:
    """Fetch class by course code and section."""
    try:
        query = "SELECT * FROM classes WHERE course_code = :course_code AND section = :section"
        rows = execute_raw_sql(query, {'course_code': course_code, 'section': section})
        if rows:
            logger.info(f"Retrieved class for {course_code} Section {section}")
            return row_to_dict(rows[0])
        return None
    except Exception as e:
        logger.error(f"Error getting class for {course_code} Section {section}: {e}", exc_info=True)
        return None


def get_class_by_id(class_id: str) -> Optional[Dict[str, Any]]:
    """Fetch class by ID."""
    try:
        query = "SELECT * FROM classes WHERE id = :class_id"
        rows = execute_raw_sql(query, {'class_id': class_id})
        if rows:
            return row_to_dict(rows[0])
        return None
    except Exception as e:
        logger.error(f"Error getting class by ID {class_id}: {e}", exc_info=True)
        return None


def get_students_by_class(class_id: str) -> List[Dict[str, Any]]:
    """Get all students in a class."""
    try:
        query = """
            SELECT * FROM students
            WHERE class_id = :class_id
            ORDER BY last_name, first_name
        """
        students = rows_to_dicts(execute_raw_sql(query, {'class_id': class_id}))
        logger.info(f"Retrieved {len(students)} students for class {class_id}")
        return students
    except Exception as e:
        logger.error(f"Error getting students for class {class_id}: {e}", exc_info=True)
        return []


def get_ungrouped_students(class_id: str) -> List[Dict[str, Any]]:
    """Get students who are not assigned to any group."""
    try:
        query = """
            SELECT * FROM students
            WHERE class_id = :class_id AND group_id IS NULL
            ORDER BY last_name, first_name
        """
        students = rows_to_dicts(execute_raw_sql(query, {'class_id': class_id}))
        logger.info(f"Retrieved {len(students)} ungrouped students for class {class_id}")
        return students
    except Exception as e:
        logger.error(f"Error getting ungrouped students: {e}", exc_info=True)
        return []


def get_grouped_students(class_id: str) -> List[Dict[str, Any]]:
    """Get students who are assigned to a group."""
    try:
        query = """
            SELECT s.*, g.group_name, g.project_title
            FROM students s
            JOIN groups g ON s.group_id = g.id
            WHERE s.class_id = :class_id AND s.group_id IS NOT NULL
            ORDER BY g.group_name, s.last_name, s.first_name
        """
        students = rows_to_dicts(execute_raw_sql(query, {'class_id': class_id}))
        logger.info(f"Retrieved {len(students)} grouped students for class {class_id}")
        return students
    except Exception as e:
        logger.error(f"Error getting grouped students: {e}", exc_info=True)
        return []


def assign_student_to_group(group_id: str, student_id: str) -> bool:
    """Assign a student to a group."""
    try:
        # Get student info
        student = get_student_by_id(student_id)
        if not student:
            logger.warning(f"Student {student_id} not found")
            return False

        if student.get('group_id'):
            logger.warning(f"Student {student_id} already in group {student.get('group_id')}")
            return False

        # Update student's group_id
        update_query = """
            UPDATE students
            SET group_id = :group_id
            WHERE id = :student_id
            RETURNING id
        """
        rows_affected = execute_update(update_query, {'group_id': group_id, 'student_id': student_id})

        if rows_affected > 0:
            # Add to group_members table
            member_name = f"{student.get('first_name', '')} {student.get('last_name', '')}".strip()
            if not member_name:
                member_name = student.get('campus_id', student_id)

            add_group_member(group_id, member_name, student_id=student_id)
            logger.info(f"Student {student_id} assigned to group {group_id}")
            return True

        return False
    except Exception as e:
        logger.error(f"Error assigning student {student_id} to group {group_id}: {e}", exc_info=True)
        return False


def get_group_members(group_id: str) -> List[Dict[str, Any]]:
    """Get all members of a group."""
    try:
        query = "SELECT * FROM group_members WHERE group_id = :group_id ORDER BY created_at"
        members = rows_to_dicts(execute_raw_sql(query, {'group_id': group_id}))
        logger.info(f"Retrieved {len(members)} members for group {group_id}")
        return members
    except Exception as e:
        logger.error(f"Error getting group members for {group_id}: {e}", exc_info=True)
        return []


def unassign_student_from_group(student_id: str) -> bool:
    """Remove a student from their group."""
    try:
        with get_db_context() as db:
            # Get student's current group_id before unassigning
            student = get_student_by_id(student_id)
            if not student or not student.get('group_id'):
                logger.warning(f"Student {student_id} is not in a group")
                return False

            group_id = student['group_id']

            # Remove from group_members table
            db.execute(text("DELETE FROM group_members WHERE student_id = :student_id"), {'student_id': student_id})

            # Update student's group_id to NULL
            db.execute(text("UPDATE students SET group_id = NULL WHERE id = :student_id"), {'student_id': student_id})

            logger.info(f"Student {student_id} unassigned from group {group_id}")
            return True
    except Exception as e:
        logger.error(f"Error unassigning student {student_id}: {e}", exc_info=True)
        return False


# --- File Storage Operations (Placeholder - needs implementation) ---

def upload_submission_file(file, storage_filename: str, content_type: str) -> Optional[str]:
    """Upload file to storage. TODO: Implement file storage."""
    logger.warning("upload_submission_file called but not implemented - file storage needed")
    return storage_filename


def get_submission_file_url(filename: str) -> Optional[str]:
    """Get URL for a submission file. TODO: Implement file storage."""
    logger.warning("get_submission_file_url called but not implemented")
    return f"/uploads/{filename}"


def delete_submission_file(filename: str) -> bool:
    """Delete a submission file. TODO: Implement file storage."""
    logger.warning("delete_submission_file called but not implemented")
    return True


def submit_stage_work(group_id: str, stage_id: str, student_id: str, content: str = None,
                     file_path: str = None, file_name: str = None) -> Optional[Dict[str, Any]]:
    """Submit work for a project stage. TODO: Verify implementation."""
    logger.warning("submit_stage_work called - may need updates for new schema")
    return None


def get_group_submissions(group_id: str) -> List[Dict[str, Any]]:
    """Get all submissions for a group."""
    try:
        query = """
            SELECT * FROM group_submissions
            WHERE group_id = :group_id
            ORDER BY stage_number ASC
        """
        submissions = rows_to_dicts(execute_raw_sql(query, {'group_id': group_id}))
        logger.info(f"Retrieved {len(submissions)} submissions for group {group_id}")
        return submissions
    except Exception as e:
        logger.error(f"Error getting submissions for group {group_id}: {e}", exc_info=True)
        return []


# --- Course Resources ---

def get_course_resources(course_code: str) -> List[Dict[str, Any]]:
    """Get all resources for a course."""
    try:
        query = """
            SELECT * FROM course_resources
            WHERE course_code = :course_code
            ORDER BY display_order ASC
        """
        resources = rows_to_dicts(execute_raw_sql(query, {'course_code': course_code}))
        logger.info(f"Retrieved {len(resources)} resources for course {course_code}")
        return resources
    except Exception as e:
        logger.error(f"Error getting resources for course {course_code}: {e}", exc_info=True)
        return []


def get_resource_by_id(resource_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific resource by ID."""
    try:
        query = "SELECT * FROM course_resources WHERE id = :resource_id"
        rows = execute_raw_sql(query, {'resource_id': resource_id})
        if rows:
            return row_to_dict(rows[0])
        return None
    except Exception as e:
        logger.error(f"Error getting resource {resource_id}: {e}", exc_info=True)
        return None


def create_resource(course_code: str, title: str, resource_type: str, content: Dict[str, Any],
                   display_order: int = 0) -> Optional[Dict[str, Any]]:
    """Create a new course resource."""
    try:
        query = """
            INSERT INTO course_resources
            (course_code, title, resource_type, content, display_order, created_at, updated_at)
            VALUES (:course_code, :title, :resource_type, :content, :display_order, NOW(), NOW())
            RETURNING *
        """
        params = {
            'course_code': course_code,
            'title': title,
            'resource_type': resource_type,
            'content': json.dumps(content),
            'display_order': display_order
        }

        with get_db_context() as db:
            result = db.execute(text(query), params)
            resource = result.fetchone()
            logger.info(f"Created resource '{title}' for course {course_code}")
            return row_to_dict(resource)
    except Exception as e:
        logger.error(f"Error creating resource: {e}", exc_info=True)
        return None


def update_resource(resource_id: str, title: str = None, content: Dict[str, Any] = None) -> bool:
    """Update a course resource."""
    try:
        updates = []
        params = {'resource_id': resource_id}

        if title is not None:
            updates.append("title = :title")
            params['title'] = title
        if content is not None:
            updates.append("content = :content")
            params['content'] = json.dumps(content)

        if not updates:
            return True

        query = f"""
            UPDATE course_resources
            SET {', '.join(updates)}, updated_at = NOW()
            WHERE id = :resource_id
            RETURNING id
        """

        rows_affected = execute_update(query, params)
        logger.info(f"Updated resource {resource_id}")
        return rows_affected > 0
    except Exception as e:
        logger.error(f"Error updating resource {resource_id}: {e}", exc_info=True)
        return False


def delete_resource(resource_id: str) -> bool:
    """Delete a course resource."""
    try:
        query = "DELETE FROM course_resources WHERE id = :resource_id RETURNING id"
        rows_affected = execute_update(query, {'resource_id': resource_id})
        logger.info(f"Deleted resource {resource_id}")
        return rows_affected > 0
    except Exception as e:
        logger.error(f"Error deleting resource {resource_id}: {e}", exc_info=True)
        return False


def reorder_resources(resource_ids: List[str]) -> bool:
    """Reorder resources by updating display_order."""
    try:
        with get_db_context() as db:
            for order, resource_id in enumerate(resource_ids):
                db.execute(
                    text("UPDATE course_resources SET display_order = :order WHERE id = :resource_id"),
                    {'order': order, 'resource_id': resource_id}
                )
            logger.info(f"Reordered {len(resource_ids)} resources")
            return True
    except Exception as e:
        logger.error(f"Error reordering resources: {e}", exc_info=True)
        return False


def get_resource_counts_by_course() -> Dict[str, int]:
    """Get resource counts grouped by course."""
    try:
        query = """
            SELECT course_code, COUNT(*) as count
            FROM course_resources
            GROUP BY course_code
        """
        rows = execute_raw_sql(query)
        counts = {row.course_code: row.count for row in rows}
        logger.info(f"Retrieved resource counts for {len(counts)} courses")
        return counts
    except Exception as e:
        logger.error(f"Error getting resource counts: {e}", exc_info=True)
        return {}


# --- Class Records ---

def get_all_classes() -> List[Dict[str, Any]]:
    """Get all classes."""
    try:
        query = "SELECT * FROM classes ORDER BY course_code, section"
        classes = rows_to_dicts(execute_raw_sql(query))
        logger.info(f"Retrieved {len(classes)} classes")
        return classes
    except Exception as e:
        logger.error(f"Error getting all classes: {e}", exc_info=True)
        return []


def get_class_records(class_id: str) -> List[Dict[str, Any]]:
    """Get all student records for a class."""
    try:
        query = """
            SELECT s.*, g.group_name
            FROM students s
            LEFT JOIN groups g ON s.group_id = g.id
            WHERE s.class_id = :class_id
            ORDER BY s.last_name, s.first_name
        """
        records = rows_to_dicts(execute_raw_sql(query, {'class_id': class_id}))
        logger.info(f"Retrieved {len(records)} class records for {class_id}")
        return records
    except Exception as e:
        logger.error(f"Error getting class records for {class_id}: {e}", exc_info=True)
        return []


def update_student_exam_status(student_id: str, exam_type: str, status: str) -> bool:
    """Update a student's exam status."""
    try:
        field_map = {
            'midterm': 'midterm_exam_status',
            'final': 'final_exam_status'
        }

        field = field_map.get(exam_type)
        if not field:
            logger.error(f"Invalid exam type: {exam_type}")
            return False

        query = f"""
            UPDATE students
            SET {field} = :status
            WHERE id = :student_id
            RETURNING id
        """
        rows_affected = execute_update(query, {'student_id': student_id, 'status': status})
        logger.info(f"Updated {exam_type} status for student {student_id} to {status}")
        return rows_affected > 0
    except Exception as e:
        logger.error(f"Error updating exam status: {e}", exc_info=True)
        return False


def bulk_update_exam_status(student_ids: List[str], exam_type: str, status: str) -> int:
    """Bulk update exam status for multiple students."""
    try:
        field_map = {
            'midterm': 'midterm_exam_status',
            'final': 'final_exam_status'
        }

        field = field_map.get(exam_type)
        if not field:
            logger.error(f"Invalid exam type: {exam_type}")
            return 0

        query = f"""
            UPDATE students
            SET {field} = :status
            WHERE id = ANY(:student_ids)
        """
        rows_affected = execute_update(query, {'student_ids': student_ids, 'status': status})
        logger.info(f"Bulk updated {exam_type} status for {rows_affected} students")
        return rows_affected
    except Exception as e:
        logger.error(f"Error bulk updating exam status: {e}", exc_info=True)
        return 0


# --- Assessments and Grades ---

def get_assessments_by_class(class_id: str) -> List[Dict[str, Any]]:
    """Get all assessments for a class."""
    try:
        query = """
            SELECT * FROM assessments
            WHERE class_id = :class_id
            ORDER BY due_date DESC
        """
        assessments = rows_to_dicts(execute_raw_sql(query, {'class_id': class_id}))
        logger.info(f"Retrieved {len(assessments)} assessments for class {class_id}")
        return assessments
    except Exception as e:
        logger.error(f"Error getting assessments for class {class_id}: {e}", exc_info=True)
        return []


def create_assessment(class_id: str, title: str, assessment_type: str, max_score: float,
                     due_date: str = None) -> Optional[Dict[str, Any]]:
    """Create a new assessment."""
    try:
        query = """
            INSERT INTO assessments
            (class_id, title, assessment_type, max_score, due_date, created_at)
            VALUES (:class_id, :title, :assessment_type, :max_score, :due_date, NOW())
            RETURNING *
        """
        params = {
            'class_id': class_id,
            'title': title,
            'assessment_type': assessment_type,
            'max_score': max_score,
            'due_date': due_date
        }

        with get_db_context() as db:
            result = db.execute(text(query), params)
            assessment = result.fetchone()
            logger.info(f"Created assessment '{title}' for class {class_id}")
            return row_to_dict(assessment)
    except Exception as e:
        logger.error(f"Error creating assessment: {e}", exc_info=True)
        return None


def update_assessment(assessment_id: str, title: str = None, max_score: float = None,
                     due_date: str = None) -> bool:
    """Update an assessment."""
    try:
        updates = []
        params = {'assessment_id': assessment_id}

        if title is not None:
            updates.append("title = :title")
            params['title'] = title
        if max_score is not None:
            updates.append("max_score = :max_score")
            params['max_score'] = max_score
        if due_date is not None:
            updates.append("due_date = :due_date")
            params['due_date'] = due_date

        if not updates:
            return True

        query = f"""
            UPDATE assessments
            SET {', '.join(updates)}
            WHERE id = :assessment_id
            RETURNING id
        """

        rows_affected = execute_update(query, params)
        logger.info(f"Updated assessment {assessment_id}")
        return rows_affected > 0
    except Exception as e:
        logger.error(f"Error updating assessment {assessment_id}: {e}", exc_info=True)
        return False


def delete_assessment(assessment_id: str) -> bool:
    """Delete an assessment."""
    try:
        with get_db_context() as db:
            # Delete associated grades first
            db.execute(text("DELETE FROM student_grades WHERE assessment_id = :assessment_id"),
                      {'assessment_id': assessment_id})
            # Delete the assessment
            result = db.execute(text("DELETE FROM assessments WHERE id = :assessment_id RETURNING id"),
                              {'assessment_id': assessment_id})
            deleted = result.fetchone()
            logger.info(f"Deleted assessment {assessment_id}")
            return deleted is not None
    except Exception as e:
        logger.error(f"Error deleting assessment {assessment_id}: {e}", exc_info=True)
        return False


def get_grades_by_assessment(assessment_id: str) -> List[Dict[str, Any]]:
    """Get all grades for an assessment."""
    try:
        query = """
            SELECT sg.*, s.first_name, s.last_name, s.campus_id
            FROM student_grades sg
            JOIN students s ON sg.student_id = s.id
            WHERE sg.assessment_id = :assessment_id
            ORDER BY s.last_name, s.first_name
        """
        grades = rows_to_dicts(execute_raw_sql(query, {'assessment_id': assessment_id}))
        logger.info(f"Retrieved {len(grades)} grades for assessment {assessment_id}")
        return grades
    except Exception as e:
        logger.error(f"Error getting grades for assessment {assessment_id}: {e}", exc_info=True)
        return []


def get_student_grades_for_class(student_id: str, class_id: str) -> List[Dict[str, Any]]:
    """Get all grades for a student in a class."""
    try:
        query = """
            SELECT sg.*, a.title, a.assessment_type, a.max_score
            FROM student_grades sg
            JOIN assessments a ON sg.assessment_id = a.id
            WHERE sg.student_id = :student_id AND a.class_id = :class_id
            ORDER BY a.due_date DESC
        """
        grades = rows_to_dicts(execute_raw_sql(query, {'student_id': student_id, 'class_id': class_id}))
        logger.info(f"Retrieved {len(grades)} grades for student {student_id} in class {class_id}")
        return grades
    except Exception as e:
        logger.error(f"Error getting student grades: {e}", exc_info=True)
        return []


def upsert_student_grade(student_id: str, assessment_id: str, score: float,
                        feedback: str = None) -> Optional[Dict[str, Any]]:
    """Insert or update a student grade."""
    try:
        query = """
            INSERT INTO student_grades (student_id, assessment_id, score, feedback, created_at, updated_at)
            VALUES (:student_id, :assessment_id, :score, :feedback, NOW(), NOW())
            ON CONFLICT (student_id, assessment_id)
            DO UPDATE SET score = :score, feedback = :feedback, updated_at = NOW()
            RETURNING *
        """
        params = {
            'student_id': student_id,
            'assessment_id': assessment_id,
            'score': score,
            'feedback': feedback
        }

        with get_db_context() as db:
            result = db.execute(text(query), params)
            grade = result.fetchone()
            logger.info(f"Upserted grade for student {student_id}, assessment {assessment_id}")
            return row_to_dict(grade)
    except Exception as e:
        logger.error(f"Error upserting grade: {e}", exc_info=True)
        return None


def bulk_upsert_grades(grades: List[Dict[str, Any]]) -> int:
    """Bulk insert or update multiple grades."""
    try:
        count = 0
        with get_db_context() as db:
            for grade_data in grades:
                query = """
                    INSERT INTO student_grades (student_id, assessment_id, score, feedback, created_at, updated_at)
                    VALUES (:student_id, :assessment_id, :score, :feedback, NOW(), NOW())
                    ON CONFLICT (student_id, assessment_id)
                    DO UPDATE SET score = :score, feedback = :feedback, updated_at = NOW()
                """
                db.execute(text(query), grade_data)
                count += 1

        logger.info(f"Bulk upserted {count} grades")
        return count
    except Exception as e:
        logger.error(f"Error bulk upserting grades: {e}", exc_info=True)
        return 0


def get_assessment_stats(assessment_id: str) -> Dict[str, Any]:
    """Get statistics for an assessment."""
    try:
        query = """
            SELECT
                COUNT(*) as total_submissions,
                AVG(score) as average_score,
                MIN(score) as min_score,
                MAX(score) as max_score
            FROM student_grades
            WHERE assessment_id = :assessment_id
        """
        rows = execute_raw_sql(query, {'assessment_id': assessment_id})
        if rows:
            stats = row_to_dict(rows[0])
            logger.info(f"Retrieved stats for assessment {assessment_id}")
            return stats
        return {}
    except Exception as e:
        logger.error(f"Error getting assessment stats: {e}", exc_info=True)
        return {}
