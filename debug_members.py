
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

print("Fetching first 5 group_members...")
try:
    response = supabase.table('group_members').select('*').limit(5).execute()
    print(json.dumps(response.data, indent=2))
    
    if response.data:
        group_id = response.data[0]['group_id']
        print(f"\nChecking group {group_id}...")
        group_resp = supabase.table('groups').select('*, group_members(*)').eq('id', group_id).execute()
        print(json.dumps(group_resp.data, indent=2))

except Exception as e:
    print(f"Error: {e}")
