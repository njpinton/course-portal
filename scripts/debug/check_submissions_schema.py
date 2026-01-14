import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Get a sample submission to see what fields exist
response = supabase.table('group_submissions').select('*').limit(1).execute()
if response.data:
    print("group_submissions table columns:")
    for key in response.data[0].keys():
        print(f"  - {key}: {response.data[0][key]}")
else:
    print("No submissions found")
