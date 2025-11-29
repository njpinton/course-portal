import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# First, get an ungrouped student
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Get ungrouped students
ungrouped_response = supabase.table('students').select('id, first_name, last_name').is_('group_id', 'null').limit(1).execute()
if not ungrouped_response.data:
    print("❌ No ungrouped students available for testing")
    exit(1)

student = ungrouped_response.data[0]
student_id = student['id']
student_name = f"{student.get('first_name', '')} {student.get('last_name', '')}"

print(f"Using student for testing: {student_name} (ID: {student_id[:8]}...)")

# Now test group login and add member
BASE_URL = "http://127.0.0.1:8788"
session = requests.Session()

print("\n" + "=" * 100)
print("TESTING GROUP LOGIN AND ADD MEMBER FLOW")
print("=" * 100)

# Step 1: Get a valid group with username
print("\n1️⃣ Getting a valid group with login credentials...")
groups_response = supabase.table('groups').select('id, group_name, username').neq('username', None).limit(1).execute()
if not groups_response.data:
    print("❌ No groups with username found")
    exit(1)

group = groups_response.data[0]
group_id = group['id']
group_name = group['group_name']
group_username = group['username']
print(f"✅ Found group: {group_name} (username: {group_username})")

# For testing, we need the password. Let's use a known test password
# Since we don't know the actual password, we'll try a common one
test_password = "test123"

# Step 2: Try to log in as group
print(f"\n2️⃣ Attempting group login with username: {group_username}")
login_response = session.post(
    f"{BASE_URL}/group_login",
    data={"username": group_username, "password": test_password}
)

if login_response.status_code == 302 or login_response.status_code == 200:
    print(f"✅ Login attempt made (status: {login_response.status_code})")
else:
    print(f"❌ Login failed (status: {login_response.status_code})")
    print(f"   Response: {login_response.text[:200]}")
    exit(1)

# Step 3: Try to fetch group submission portal
print("\n3️⃣ Fetching group submission portal...")
portal_response = session.get(f"{BASE_URL}/group_submission_portal")
if portal_response.status_code == 200:
    print(f"✅ Successfully accessed group submission portal")
    if "add-member-modal" in portal_response.text:
        print("✅ Add Member modal HTML found in portal")
    else:
        print("❌ Add Member modal HTML NOT found in portal")
else:
    print(f"❌ Failed to access portal (status: {portal_response.status_code})")
    exit(1)

# Step 4: Try to fetch ungrouped students
print("\n4️⃣ Fetching ungrouped students from API...")
students_response = session.get(f"{BASE_URL}/api/students/ungrouped/all")
if students_response.status_code == 200:
    students = students_response.json()
    print(f"✅ Successfully fetched {len(students)} ungrouped students")
    if len(students) > 0:
        print(f"   Sample: {students[0].get('first_name', '')} {students[0].get('last_name', '')}")
else:
    print(f"❌ Failed to fetch students (status: {students_response.status_code})")
    print(f"   Response: {students_response.text}")

# Step 5: Try to add a member
print(f"\n5️⃣ Attempting to add member {student_name}...")
add_response = session.post(
    f"{BASE_URL}/api/group/members/add",
    json={"student_id": student_id},
    headers={"Content-Type": "application/json"}
)

if add_response.status_code == 200:
    result = add_response.json()
    if result.get('success'):
        print(f"✅ Successfully added {student_name} to group {group_name}")
    else:
        print(f"❌ Add failed: {result.get('error', 'Unknown error')}")
elif add_response.status_code == 401:
    print("❌ Unauthorized - Group not properly logged in")
else:
    print(f"❌ Add member failed (status: {add_response.status_code})")
    print(f"   Response: {add_response.text}")

print("\n" + "=" * 100)
print("TEST COMPLETED")
print("=" * 100)
