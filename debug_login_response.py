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
groups_response = supabase.table('groups').select('id, group_name, username, password_hash').neq('username', None).limit(1).execute()
group = groups_response.data[0]
group_username = group['username']
group_password_hash = group.get('password_hash')
test_password = "test123"

print(f"Group username: {group_username}")
print(f"Group password hash exists: {bool(group_password_hash)}")
print(f"Test password: {test_password}")
print()

# Login WITHOUT following redirects
print("=" * 100)
print("ATTEMPTING LOGIN")
print("=" * 100)
login_response = session.post(
    f"{BASE_URL}/group_login",
    data={"username": group_username, "password": test_password},
    allow_redirects=False
)

print(f"Status: {login_response.status_code}")
print(f"Response length: {len(login_response.text)} characters")
print()

# Check if the response contains an error message
if "error" in login_response.text.lower():
    # Extract the error message
    import re
    error_match = re.search(r'<div class="error-message">(.*?)</div>', login_response.text, re.DOTALL)
    if error_match:
        error_text = error_match.group(1).strip()
        print(f"Error message found: {error_text}")
    else:
        # Try another pattern
        error_match = re.search(r'error["\']>([^<]+)<', login_response.text)
        if error_match:
            print(f"Error message found: {error_match.group(1)}")
        else:
            print("No error message found in HTML")
            # Print first 1000 chars of response
            print("\nResponse preview:")
            print(login_response.text[:1500])
else:
    print("Response title:", login_response.text[login_response.text.find('<title>')+7:login_response.text.find('</title>')])
