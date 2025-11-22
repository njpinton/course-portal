import os
from supabase import create_client, Client

_supabase: Client = None
_init_attempted = False

def get_supabase_client() -> Client:
    """Get or create Supabase client with lazy initialization."""
    global _supabase, _init_attempted

    if _supabase is not None:
        return _supabase

    if _init_attempted:
        return None  # Already tried and failed

    _init_attempted = True

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_ANON_KEY")

    if not url or not key:
        print(f"WARNING: Supabase credentials not found in environment")
        return None

    try:
        _supabase = create_client(url, key)
        return _supabase
    except Exception as e:
        print(f"ERROR: Failed to initialize Supabase client: {e}")
        import traceback
        traceback.print_exc()
        return None

# Eagerly try to initialize, but don't fail if it doesn't work
supabase: Client = None
try:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_ANON_KEY")
    if url and key:
        supabase = create_client(url, key)
        _supabase = supabase  # Also set in lazy var
        _init_attempted = True
except Exception as e:
    print(f"DEBUG: Eager initialization failed: {e}, will use lazy init")
    # Ignore - lazy initialization will handle it on first use

def _get_client() -> Client:
    """Get Supabase client, using lazy initialization if needed."""
    global supabase
    if supabase is not None:
        return supabase
    return get_supabase_client()

# --- Supabase CRUD operations for Group Portal ---

def create_group(group_name: str, project_title: str) -> dict:
    if not supabase:
        print("Supabase client not initialized. Cannot create group.")
        return None
    try:
        response = supabase.table('groups').insert({
            "group_name": group_name,
            "project_title": project_title
        }).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error creating group: {e}")
        return None

def add_group_member(group_id: str, member_name: str) -> dict:
    if not supabase:
        print("Supabase client not initialized. Cannot add group member.")
        return None
    try:
        response = supabase.table('group_members').insert({
            "group_id": group_id,
            "member_name": member_name
        }).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error adding group member: {e}")
        return None

def add_group_document(group_id: str, document_title: str, file_path: str) -> dict:
    if not supabase:
        print("Supabase client not initialized. Cannot add group document.")
        return None
    try:
        response = supabase.table('group_documents').insert({
            "group_id": group_id,
            "document_title": document_title,
            "file_path": file_path
        }).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error adding group document: {e}")
        return None

def get_groups() -> list:
    if not supabase:
        print("Supabase client not initialized. Cannot get groups.")
        return []
    try:
        response = supabase.table('groups').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Error getting groups: {e}")
        return []

def get_group_details(group_id: str) -> dict:
    if not supabase:
        print("Supabase client not initialized. Cannot get group details.")
        return None
    try:
        group_response = supabase.table('groups').select('*').eq('id', group_id).execute()
        group_data = group_response.data[0] if group_response.data else None

        if group_data:
            members_response = supabase.table('group_members').select('*').eq('group_id', group_id).execute()
            documents_response = supabase.table('group_documents').select('*').eq('group_id', group_id).execute()
            group_data['members'] = members_response.data
            group_data['documents'] = documents_response.data
        return group_data
    except Exception as e:
        print(f"Error getting group details: {e}")
        return None

def delete_group(group_id: str) -> bool:
    if not supabase:
        print("Supabase client not initialized. Cannot delete group.")
        return False
    try:
        # Delete associated documents first
        supabase.table('group_documents').delete().eq('group_id', group_id).execute()
        # Delete associated members
        supabase.table('group_members').delete().eq('group_id', group_id).execute()
        # Delete the group itself
        response = supabase.table('groups').delete().eq('id', group_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error deleting group: {e}")
        return False

def get_project_stages() -> list:
    """Get all project stages."""
    if not supabase:
        return []
    try:
        response = supabase.table('project_stages').select('*').order('stage_number').execute()
        return response.data
    except Exception as e:
        print(f"Error getting project stages: {e}")
        return []

def update_stage_status(group_id: str, stage_id: str, status: str) -> dict:
    """Update the status of a stage for a group."""
    if not supabase:
        return None
    try:
        response = supabase.table('group_stage_status').update({
            'status': status
        }).eq('group_id', group_id).eq('stage_id', stage_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating stage status: {e}")
        return None

def get_project_models() -> list:
    """Get all available project models."""
    if not supabase:
        return []
    try:
        response = supabase.table('project_models').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Error getting project models: {e}")
        return []

def add_project_model(model_name: str, model_config: dict) -> dict:
    """Add a new project model."""
    if not supabase:
        return None
    try:
        response = supabase.table('project_models').insert({
            'model_name': model_name,
            'config': model_config
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error adding project model: {e}")
        return None

def get_stage_documents(stage_id: str) -> list:
    """Get all documents for a specific stage."""
    if not supabase:
        return []
    try:
        response = supabase.table('stage_documents').select('*').eq('stage_id', stage_id).execute()
        return response.data
    except Exception as e:
        print(f"Error getting stage documents: {e}")
        return []

def add_stage_document(stage_id: str, document_title: str, file_path: str) -> dict:
    """Add a document to a stage."""
    if not supabase:
        return None
    try:
        response = supabase.table('stage_documents').insert({
            'stage_id': stage_id,
            'document_title': document_title,
            'file_path': file_path
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error adding stage document: {e}")
        return None

def update_group_project_info(group_id: str, project_info: dict) -> dict:
    """Update project information for a group."""
    if not supabase:
        return None
    try:
        response = supabase.table('groups').update(project_info).eq('id', group_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating group project info: {e}")
        return None

def update_group_credentials(group_id: str, username: str, password_hash: str) -> bool:
    """Update group credentials."""
    if not supabase:
        return False
    try:
        response = supabase.table('groups').update({
            'username': username,
            'password_hash': password_hash
        }).eq('id', group_id).execute()
        success = response.data and len(response.data) > 0
        if not success:
            print(f"Warning: Update returned no data for group {group_id}")
        return success
    except Exception as e:
        error_msg = str(e)
        print(f"Error updating group credentials for {group_id}: {e}")
        # Re-raise the exception to be caught by the caller
        raise Exception(error_msg)

def get_group_by_username(username: str) -> dict:
    """Get group by username."""
    if not supabase:
        return None
    try:
        response = supabase.table('groups').select('*').eq('username', username).single().execute()
        return response.data
    except Exception as e:
        print(f"Error getting group by username: {e}")
        return None

def update_group_last_login(group_id: str) -> dict:
    """Update last login timestamp for a group."""
    if not supabase:
        return None
    try:
        from datetime import datetime
        response = supabase.table('groups').update({
            'last_login': datetime.utcnow().isoformat()
        }).eq('id', group_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating last login: {e}")
        return None

def get_group_with_submissions(group_id: str) -> dict:
    """Get group details including all submissions."""
    if not supabase:
        return None
    try:
        group = get_group_details(group_id)
        if group:
            submissions_response = supabase.table('group_submissions').select('*').eq('group_id', group_id).execute()
            group['submissions'] = submissions_response.data
        return group
    except Exception as e:
        print(f"Error getting group with submissions: {e}")
        return None

def submit_group_stage_work(group_id: str, stage_id: str, submission_data: dict) -> dict:
    """Submit work for a specific stage."""
    if not supabase:
        return None
    try:
        data_to_insert = {
            'group_id': group_id,
            'stage_id': stage_id,
            **submission_data
        }
        print(f"DEBUG: Inserting submission data: {data_to_insert}")
        response = supabase.table('group_submissions').insert(data_to_insert).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error submitting group stage work: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_group_feedback(group_id: str) -> list:
    """Get all feedback for a group."""
    if not supabase:
        return []
    try:
        response = supabase.table('group_feedback').select('*').eq('group_id', group_id).execute()
        return response.data
    except Exception as e:
        print(f"Error getting group feedback: {e}")
        return []

# --- ADMIN DASHBOARD HELPER FUNCTIONS ---

def get_all_submissions_with_groups() -> list:
    """Get all submissions with group information."""
    if not supabase:
        return []
    try:
        response = supabase.table('group_submissions').select(
            '*, groups(id, group_name, project_title)'
        ).order('submitted_at', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error getting all submissions: {e}")
        return []

def get_submission_by_id(submission_id: str) -> dict:
    """Get a single submission by ID with group details."""
    if not supabase:
        return None
    try:
        response = supabase.table('group_submissions').select(
            '*, groups(id, group_name, project_title, members:group_members(member_name))'
        ).eq('id', submission_id).single().execute()
        return response.data
    except Exception as e:
        print(f"Error getting submission by ID: {e}")
        return None

def get_submissions_by_group(group_id: str) -> list:
    """Get all submissions for a specific group."""
    if not supabase:
        return []
    try:
        response = supabase.table('group_submissions').select('*').eq('group_id', group_id).order('stage_number').execute()
        return response.data
    except Exception as e:
        print(f"Error getting submissions by group: {e}")
        return []

def get_submissions_by_stage(stage_number: int) -> list:
    """Get all submissions for a specific stage."""
    if not supabase:
        return []
    try:
        response = supabase.table('group_submissions').select(
            '*, groups(group_name, project_title)'
        ).eq('stage_number', stage_number).order('submitted_at', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error getting submissions by stage: {e}")
        return []

# --- Student Management Functions ---

def get_class_by_code_section(course_code: str, section: str) -> dict:
    """Get a class by course code and section."""
    client = _get_client()
    if not client:
        print(f"DEBUG: Client not available for query")
        return None
    try:
        print(f"DEBUG: Querying classes where course_code={course_code}, section={section}")
        # Try without .single() first to see if we get any results
        response = client.table('classes').select('*').eq('course_code', course_code).eq('section', section).execute()
        print(f"DEBUG: Query returned {len(response.data)} results")
        if response.data and len(response.data) > 0:
            print(f"DEBUG: Returning first result: {response.data[0]}")
            return response.data[0]
        else:
            print(f"DEBUG: No results found for {course_code} {section}")
            return None
    except Exception as e:
        print(f"Error getting class: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_students_by_class(class_id: str) -> list:
    """Get all students in a class."""
    client = _get_client()
    if not client:
        return []
    try:
        response = client.table('students').select('*').eq('class_id', class_id).order('last_name').execute()
        return response.data
    except Exception as e:
        print(f"Error getting students: {e}")
        return []

def get_ungrouped_students(class_id: str) -> list:
    """Get students in a class who haven't been assigned to a group yet."""
    client = _get_client()
    if not client:
        return []
    try:
        response = client.table('students').select('*').eq('class_id', class_id).is_('group_id', 'null').order('last_name').execute()
        return response.data
    except Exception as e:
        print(f"Error getting ungrouped students: {e}")
        return []

def get_grouped_students(class_id: str) -> list:
    """Get students in a class who have been assigned to a group."""
    client = _get_client()
    if not client:
        return []
    try:
        response = client.table('students').select('*').eq('class_id', class_id).not_('group_id', 'is', 'null').order('last_name').execute()
        return response.data
    except Exception as e:
        print(f"Error getting grouped students: {e}")
        return []

def assign_student_to_group(student_id: str, group_id: str) -> bool:
    """Assign a student to a group."""
    if not supabase:
        return False
    try:
        supabase.table('students').update({'group_id': group_id}).eq('id', student_id).execute()
        return True
    except Exception as e:
        print(f"Error assigning student to group: {e}")
        return False

def get_student_by_campus_id(campus_id: str) -> dict:
    """Get a student by campus ID."""
    if not supabase:
        return None
    try:
        response = supabase.table('students').select('*').eq('campus_id', campus_id).single().execute()
        return response.data
    except Exception as e:
        print(f"Error getting student: {e}")
        return None

def get_group_members(group_id: str) -> list:
    """Get all students in a group."""
    if not supabase:
        return []
    try:
        response = supabase.table('students').select('campus_id, first_name, last_name, email, program').eq('group_id', group_id).order('last_name').execute()
        return response.data
    except Exception as e:
        print(f"Error getting group members: {e}")
        return []

def unassign_student_from_group(student_id: str) -> bool:
    """Remove a student from their group."""
    if not supabase:
        return False
    try:
        supabase.table('students').update({'group_id': None}).eq('id', student_id).execute()
        return True
    except Exception as e:
        print(f"Error unassigning student: {e}")
        return False
