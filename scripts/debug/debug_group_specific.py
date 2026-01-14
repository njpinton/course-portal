
import os
import sys
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

supabase = create_client(url, key)

group_id = "2c994b97-9dd0-4fb0-bfac-e83fcefa4b92" # Dame Un Grrroup

print(f"Fetching group {group_id}...")
try:
    response = supabase.table('groups').select('*, group_members(member_name)').eq('id', group_id).execute()
    print(json.dumps(response.data, indent=2))
except Exception as e:
    print(f"Error: {e}")
