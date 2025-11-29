
import os
import sys
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

supabase = create_client(url, key)

group_id = "42c4922d-e00a-493b-8c9b-c7dfdf992cd2"

print(f"Checking students for group {group_id}...")
try:
    response = supabase.table('students').select('*').eq('group_id', group_id).execute()
    print(json.dumps(response.data, indent=2))
except Exception as e:
    print(f"Error: {e}")
