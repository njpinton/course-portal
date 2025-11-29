import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Get all groups with this username
response = supabase.table('groups').select('id, group_name, username, project_title').eq('username', 'testaddmember').execute()

if response.data:
    print(f"Found {len(response.data)} group(s) with username 'testaddmember':")
    for group in response.data:
        print(f"\n  Group: {group['group_name']}")
        print(f"  ID: {group['id']}")
        print(f"  Project Title: {repr(group['project_title'])}")
else:
    print("No groups found")
