import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Test group IDs to delete
test_group_ids = [
    'fc29a64c-2c15-4b5d-8a7e-4d1df18332b4',
    '8541de90-2504-4ad5-9819-6408eae12802',
    '928c1c7f-6998-4f64-8661-a49cc37b3e7b',
    '62f75280-0393-4171-96c2-1b837eee2779',
    '7bf655ac-865a-4a6f-96e0-701c73253b4f',
    '080c5e79-dec7-45dd-9ac0-e2bf8084b6d7',
    '1ea825d7-7517-41c0-88bf-5dc6e585e8ea'
]

print("=" * 100)
print("DELETING TEST GROUPS FROM DATABASE")
print("=" * 100)

deleted_count = 0
for group_id in test_group_ids:
    try:
        # Get group name before deleting
        group_response = supabase.table('groups').select('group_name').eq('id', group_id).execute()
        group_name = group_response.data[0]['group_name'] if group_response.data else 'Unknown'

        # Delete from group_members first (foreign key constraint)
        supabase.table('group_members').delete().eq('group_id', group_id).execute()

        # Delete from group_documents
        supabase.table('group_documents').delete().eq('group_id', group_id).execute()

        # Delete from group_submissions
        supabase.table('group_submissions').delete().eq('group_id', group_id).execute()

        # Delete from groups
        supabase.table('groups').delete().eq('id', group_id).execute()

        print(f"✅ Deleted: {group_name} ({group_id})")
        deleted_count += 1
    except Exception as e:
        print(f"❌ Failed to delete {group_id}: {e}")

print("=" * 100)
print(f"\n✨ Successfully deleted {deleted_count}/{len(test_group_ids)} test groups!")
print("=" * 100)
