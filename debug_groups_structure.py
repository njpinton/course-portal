
import os
import sys
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_ANON_KEY not set")
    sys.exit(1)

supabase = create_client(url, key)

print("Fetching groups with members...")
try:
    response = supabase.table('groups').select('*, group_members(member_name)').eq('is_active', True).limit(2).execute()
    print(json.dumps(response.data, indent=2))
except Exception as e:
    print(f"Error: {e}")
