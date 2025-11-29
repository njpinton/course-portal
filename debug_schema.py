import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Get groups table schema
response = supabase.table('groups').select('*').limit(1).execute()
if response.data:
    print("Groups table columns:")
    for key in response.data[0].keys():
        print(f"  - {key}")
else:
    print("No groups found")
