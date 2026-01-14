import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Get the specific group ID from the test
group_id = 'bc8ca7b4-197d-4df3-b4fc-608b94c6ebcb'
response = supabase.table('groups').select('id, group_name, username, project_title').eq('id', group_id).execute()

if response.data:
    group = response.data[0]
    print(f"✅ Group found!")
    print(f"  Group: {group['group_name']}")
    print(f"  Username: {group['username']}")
    print(f"  Project Title: {repr(group['project_title'])}")
else:
    print(f"❌ Group with ID {group_id} not found")
