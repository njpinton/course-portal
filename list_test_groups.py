import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Get all groups
response = supabase.table('groups').select('id, group_name, project_title, created_at').order('created_at', desc=True).execute()

print("=" * 120)
print("ALL GROUPS IN DATABASE")
print("=" * 120)

test_groups = []
for group in response.data:
    group_name = group.get('group_name', 'N/A')
    project_title = group.get('project_title', 'N/A')
    created_at = group.get('created_at', 'N/A')
    group_id = group['id']

    # Identify test groups (ones with "test" in name or generic test data)
    is_test = any(keyword in group_name.lower() for keyword in ['test', 'sample', 'demo', 'tmp'])

    status = "🧪 TEST" if is_test else "✓ PROD"
    print(f"{status} | {group_name[:30]:30} | {project_title[:40]:40} | {created_at}")

    if is_test:
        test_groups.append({
            'id': group_id,
            'name': group_name,
            'project': project_title,
            'created': created_at
        })

print("=" * 120)
print(f"\nFound {len(test_groups)} TEST groups to delete:")
print("=" * 120)

for i, group in enumerate(test_groups, 1):
    print(f"\n{i}. Group: {group['name']}")
    print(f"   Project: {group['project']}")
    print(f"   Created: {group['created']}")
    print(f"   ID: {group['id']}")

print("\n" + "=" * 120)
print(f"Total test groups to delete: {len(test_groups)}")
print("=" * 120)
