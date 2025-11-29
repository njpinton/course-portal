import os
import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Setup
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

BASE_URL = "http://127.0.0.1:8788"
session = requests.Session()

# Get a valid group with username
print("Getting a valid group with login credentials...")
groups_response = supabase.table('groups').select('id, group_name, username').neq('username', None).limit(1).execute()
if not groups_response.data:
    print("No groups with username found")
    exit(1)

group = groups_response.data[0]
group_username = group['username']
test_password = "test123"

print(f"Group username: {group_username}")

# Try to log in as group
print(f"Attempting group login with username: {group_username}")
login_response = session.post(
    f"{BASE_URL}/group_login",
    data={"username": group_username, "password": test_password}
)

print(f"Login response status: {login_response.status_code}")
print(f"Login response cookies: {session.cookies}")

# Fetch group submission portal
print("\nFetching group submission portal...")
portal_response = session.get(f"{BASE_URL}/group_submission_portal")
print(f"Portal response status: {portal_response.status_code}")
print(f"Portal response length: {len(portal_response.text)} characters")

# Save the response to a file for inspection
with open('/tmp/portal_response.html', 'w') as f:
    f.write(portal_response.text)

print("\nResponse saved to /tmp/portal_response.html")

# Check for the modal
if "add-member-modal" in portal_response.text:
    print("✅ Add Member modal HTML found in portal")
else:
    print("❌ Add Member modal HTML NOT found in portal")
    print(f"\nFirst 2000 characters of response:\n{portal_response.text[:2000]}")
