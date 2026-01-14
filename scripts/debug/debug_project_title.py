import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Get the test group
response = supabase.table('groups').select('id, group_name, project_title').eq('username', 'testaddmember').execute()

if response.data:
    group = response.data[0]
    print(f"Group: {group['group_name']}")
    print(f"ID: {group['id']}")
    print(f"Project Title (raw): {repr(group['project_title'])}")
    print(f"Project Title length: {len(group['project_title']) if group['project_title'] else 0}")
else:
    print("Group not found")
