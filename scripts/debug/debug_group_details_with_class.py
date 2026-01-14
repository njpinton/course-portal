
import os
import sys
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

supabase = create_client(url, key)

# Use a group_id that is known to have members
group_id = "2c994b97-9dd0-4fb0-bfac-e83fcefa4b92" # Dame Un Grrroup

def get_group_details_func(group_id: str) -> dict:
    # Replicating the logic from api/supabase_client.py
    if not supabase:
        print("Supabase client not initialized.")
        return None
    try:
        group_response = supabase.table('groups').select('*').eq('id', group_id).execute()
        group_data = group_response.data[0] if group_response.data else None

        if group_data:
            members_response = supabase.table('group_members').select('*').eq('group_id', group_id).execute()
            documents_response = supabase.table('group_documents').select('*').eq('group_id', group_id).execute()

            members_data = []
            group_class_id = None # Initialize class_id to None

            if members_response.data:
                student_ids = [member.get('student_id') for member in members_response.data if member.get('student_id')]

                students_data = {}
                if student_ids:
                    students_response = supabase.table('students').select('id, campus_id, class_id').in_('id', student_ids).execute()
                    if students_response.data:
                        students_data = {student['id']: student for student in students_response.data}

                for member in members_response.data:
                    processed_member = member.copy()
                    student_id = member.get('student_id')
                    student_info = students_data.get(student_id)

                    if student_info:
                        processed_member['campus_id'] = student_info.get('campus_id', 'N/A')
                        if not group_class_id:
                            group_class_id = student_info.get('class_id')
                    else:
                        processed_member['campus_id'] = 'N/A'

                    members_data.append(processed_member)
            
            # Fallback: If class_id is still not found via group_members, try to get it from students table directly
            if not group_class_id:
                first_student_in_group_response = supabase.table('students').select('class_id').eq('group_id', group_id).limit(1).execute()
                if first_student_in_group_response.data:
                    group_class_id = first_student_in_group_response.data[0].get('class_id')

            group_data['members'] = members_data
            group_data['documents'] = documents_response.data
            
            if group_class_id:
                group_data['class_id'] = group_class_id
            else:
                group_data['class_id'] = None

        return group_data
    except Exception as e:
        print(f"Error getting group details: {e}")
        return None

print(f"Fetching full group details for {group_id}...")
group_details_output = get_group_details_func(group_id)
print(json.dumps(group_details_output, indent=2))
