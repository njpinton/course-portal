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
groups_response = supabase.table('groups').select('id, group_name, username').neq('username', None).limit(1).execute()
group = groups_response.data[0]
group_username = group['username']
test_password = "test123"

print(f"Group username: {group_username}")
print(f"Test password: {test_password}")
print()

# Login WITHOUT following redirects
print("=" * 100)
print("STEP 1: Login (NO redirect following)")
print("=" * 100)
login_response = session.post(
    f"{BASE_URL}/group_login",
    data={"username": group_username, "password": test_password},
    allow_redirects=False  # Don't follow redirect
)

print(f"Status: {login_response.status_code}")
print(f"Headers: {dict(login_response.headers)}")
print(f"Cookies after login: {dict(session.cookies)}")
if login_response.status_code == 302:
    print(f"Redirect to: {login_response.headers.get('Location')}")
print()

# Now try to access the portal WITH the cookies we have
print("=" * 100)
print("STEP 2: Access submission portal (WITH redirect following)")
print("=" * 100)
portal_response = session.get(f"{BASE_URL}/group_submission_portal", allow_redirects=True)
print(f"Status: {portal_response.status_code}")
print(f"Cookies: {dict(session.cookies)}")
print(f"Response contains 'add-member-modal': {'add-member-modal' in portal_response.text}")
print(f"Response title: {portal_response.text[portal_response.text.find('<title>')+7:portal_response.text.find('</title>')]}")
print()

# Try the add member endpoint
print("=" * 100)
print("STEP 3: Try add member endpoint")
print("=" * 100)
add_response = session.post(
    f"{BASE_URL}/api/group/members/add",
    json={"student_id": "test-id"},
    headers={"Content-Type": "application/json"}
)
print(f"Status: {add_response.status_code}")
print(f"Response: {add_response.json()}")
