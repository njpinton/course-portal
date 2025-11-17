import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key) if url and key else None

def get_supabase_client() -> Client:
    return supabase

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
