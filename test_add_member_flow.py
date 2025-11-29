import os
import requests
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Setup
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

BASE_URL = "http://127.0.0.1:8788"
session = requests.Session()

print("=" * 100)
print("TESTING GROUP ADD MEMBER FLOW")
print("=" * 100)

# Get an ungrouped student
print("\n1️⃣ Getting an ungrouped student...")
ungrouped_response = supabase.table('students').select('id, first_name, last_name').is_('group_id', 'null').limit(1).execute()
if not ungrouped_response.data:
    print("❌ No ungrouped students available")
    exit(1)

student = ungrouped_response.data[0]
student_id = student['id']
student_name = f"{student.get('first_name', '')} {student.get('last_name', '')}"
print(f"✅ Found student: {student_name} (ID: {student_id[:8]}...)")

# Test credentials
test_username = "testaddmember"
test_password = "test123"

print(f"\n2️⃣ Attempting group login with username: {test_username}")
login_response = session.post(
    f"{BASE_URL}/group_login",
    data={"username": test_username, "password": test_password},
    allow_redirects=True
)

print(f"   Status: {login_response.status_code}")
if login_response.status_code != 200:
    print(f"❌ Login failed with status {login_response.status_code}")
    exit(1)

# Check if we got the submission portal
if "add-member-modal" in login_response.text:
    print("✅ Successfully logged in and accessed submission portal")
    print("✅ Add Member modal HTML found")
else:
    print("❌ Failed to access submission portal or modal not found")
    if "Group Login" in login_response.text:
        print("   (Still showing login page - credentials failed)")
    exit(1)

# Test the API endpoint to fetch ungrouped students
print(f"\n3️⃣ Fetching list of ungrouped students from API...")
students_response = session.get(f"{BASE_URL}/api/students/ungrouped/all")
print(f"   Status: {students_response.status_code}")
if students_response.status_code == 200:
    students = students_response.json()
    print(f"✅ Successfully fetched {len(students)} ungrouped students")
else:
    print(f"❌ Failed to fetch students: {students_response.status_code}")
    print(f"   Response: {students_response.text}")

# Try to add a member
print(f"\n4️⃣ Adding {student_name} to the group...")
add_response = session.post(
    f"{BASE_URL}/api/group/members/add",
    json={"student_id": student_id},
    headers={"Content-Type": "application/json"}
)

print(f"   Status: {add_response.status_code}")
if add_response.status_code == 200:
    result = add_response.json()
    if result.get('success'):
        print(f"✅ Successfully added student to group!")
        print(f"   Response: {result.get('message')}")
    else:
        print(f"❌ Add failed: {result.get('error', 'Unknown error')}")
elif add_response.status_code == 401:
    print("❌ Unauthorized - Group not properly logged in")
    print(f"   Response: {add_response.json()}")
else:
    print(f"❌ Add member failed with status {add_response.status_code}")
    print(f"   Response: {add_response.text}")

print("\n" + "=" * 100)
print("TEST COMPLETED")
print("=" * 100)
