import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Remaining test group IDs that have students
remaining_group_ids = [
    '8541de90-2504-4ad5-9819-6408eae12802',  # test (MARIA SANTOS)
    '7bf655ac-865a-4a6f-96e0-701c73253b4f'   # test (JUAN DELA CRUZ)
]

print("=" * 100)
print("REMOVING STUDENTS FROM TEST GROUPS")
print("=" * 100)

for group_id in remaining_group_ids:
    try:
        # Get group name
        group_response = supabase.table('groups').select('group_name').eq('id', group_id).execute()
        group_name = group_response.data[0]['group_name'] if group_response.data else 'Unknown'

        # Get students in this group
        students_response = supabase.table('students').select('id, first_name, last_name').eq('group_id', group_id).execute()
        student_count = len(students_response.data)

        if student_count > 0:
            # Remove group_id from students
            supabase.table('students').update({'group_id': None}).eq('group_id', group_id).execute()
            print(f"✅ Removed {student_count} students from '{group_name}'")

            # Delete group_members
            supabase.table('group_members').delete().eq('group_id', group_id).execute()

            # Delete group_documents
            supabase.table('group_documents').delete().eq('group_id', group_id).execute()

            # Delete group_submissions
            supabase.table('group_submissions').delete().eq('group_id', group_id).execute()

            # Now delete the group
            supabase.table('groups').delete().eq('id', group_id).execute()
            print(f"✅ Deleted group: {group_name} ({group_id})")
        else:
            print(f"⚠️  No students found in group {group_id}")

    except Exception as e:
        print(f"❌ Failed to delete {group_id}: {e}")

print("=" * 100)
print("\n✨ All test groups have been cleaned up!")
print("=" * 100)
