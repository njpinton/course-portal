import os
from dotenv import load_dotenv
from supabase import create_client
from werkzeug.security import generate_password_hash
import uuid

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Create a test group with known credentials
test_group_name = "TestGroupAddMember"
test_username = "testaddmember"
test_password = "test123"
test_password_hash = generate_password_hash(test_password)

print("=" * 100)
print("CREATING TEST GROUP WITH KNOWN CREDENTIALS")
print("=" * 100)

try:
    # Check if a group with this username already exists
    existing = supabase.table('groups').select('id').eq('username', test_username).execute()
    if existing.data:
        print(f"⚠️ Group with username '{test_username}' already exists")
        group_id = existing.data[0]['id']
        print(f"Group ID: {group_id}")
    else:
        # Create new group
        group_data = {
            'id': str(uuid.uuid4()),
            'group_name': test_group_name,
            'username': test_username,
            'password_hash': test_password_hash,
            'project_title': 'Test Project for Add Member',
            'created_at': 'now()'
        }

        result = supabase.table('groups').insert(group_data).execute()
        group_id = result.data[0]['id']
        print(f"✅ Created test group: {test_group_name}")
        print(f"   Group ID: {group_id}")

    print(f"\n📝 Test Credentials:")
    print(f"   Username: {test_username}")
    print(f"   Password: {test_password}")
    print(f"   Group ID: {group_id}")
    print("\n" + "=" * 100)
except Exception as e:
    print(f"❌ Error creating test group: {e}")
    import traceback
    traceback.print_exc()
