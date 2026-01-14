#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

BASE_URL = "http://127.0.0.1:8788"
session = requests.Session()

print("=" * 80)
print("TESTING MEMBERS DISPLAY IN GROUP SUBMISSION PORTAL")
print("=" * 80)

# Login to test group
test_username = "testaddmember"
test_password = "test123"

print(f"\n1️⃣ Logging in as group: {test_username}")
login_response = session.post(
    f"{BASE_URL}/group_login",
    data={"username": test_username, "password": test_password},
    allow_redirects=True
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    exit(1)

print("✅ Login successful")

# Get the group ID from the database
print(f"\n2️⃣ Getting group ID from database...")
group_response = supabase.table('groups').select('id').eq('username', test_username).execute()
if not group_response.data:
    print("❌ Could not find group in database")
    exit(1)

group_id = group_response.data[0]['id']
print(f"✅ Found group ID: {group_id[:8]}...")

# Get the group submission portal
print(f"\n3️⃣ Getting group submission portal...")
portal_response = session.get(f"{BASE_URL}/group_submission_portal")
if portal_response.status_code != 200:
    print(f"❌ Failed to get portal: {portal_response.status_code}")
    exit(1)

print("✅ Portal loaded successfully")

# Check if members are in the HTML
print(f"\n4️⃣ Checking if members are displayed in portal HTML...")
if "loadMemberContributions" in portal_response.text:
    print("✅ Member contributions section found in HTML")
else:
    print("❌ Member contributions section NOT found in HTML")

# Get members from database to compare
print(f"\n5️⃣ Getting members from database...")
members_response = supabase.table('group_members').select('*').eq('group_id', group_id).execute()
db_members = members_response.data if members_response.data else []

print(f"   Found {len(db_members)} members in database:")
for member in db_members:
    print(f"   - {member.get('member_name', 'Unknown')} (ID: {member.get('student_id', 'N/A')[:8]}...)")

if len(db_members) == 0:
    print("   ⚠️  No members found in database")
else:
    print(f"   ✅ {len(db_members)} members found")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
