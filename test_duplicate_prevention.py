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
print("TESTING FIXED ADD MEMBER WITH DUPLICATE PREVENTION")
print("=" * 80)

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

# Login to test group
test_username = "testaddmember"
test_password = "test123"

print(f"\n2️⃣ Logging in as group: {test_username}")
login_response = session.post(
    f"{BASE_URL}/group_login",
    data={"username": test_username, "password": test_password},
    allow_redirects=True
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    exit(1)
print("✅ Login successful")

# Test NEW endpoint: Get available students (should exclude existing members)
print(f"\n3️⃣ Testing NEW endpoint: /api/group/members/available")
available_response = session.get(f"{BASE_URL}/api/group/members/available")
print(f"   Status: {available_response.status_code}")
if available_response.status_code == 200:
    available_students = available_response.json()
    print(f"✅ Got {len(available_students)} available students")

    # Check if our test student is in the list
    student_in_available = any(s['id'] == student_id for s in available_students)
    if student_in_available:
        print(f"   ✅ Test student IS in available list (not yet added)")
    else:
        print(f"   ❌ Test student NOT in available list (or already added)")
else:
    print(f"❌ Failed to fetch available students: {available_response.text}")

# Add the student
print(f"\n4️⃣ Adding {student_name} to the group...")
add_response = session.post(
    f"{BASE_URL}/api/group/members/add",
    json={"student_id": student_id},
    headers={"Content-Type": "application/json"}
)

print(f"   Status: {add_response.status_code}")
if add_response.status_code == 200:
    print(f"✅ Student added successfully")
else:
    print(f"❌ Failed to add student: {add_response.text}")
    exit(1)

# Test AGAIN: Get available students (should now EXCLUDE this student)
print(f"\n5️⃣ Testing endpoint AGAIN after adding student...")
available_response2 = session.get(f"{BASE_URL}/api/group/members/available")
if available_response2.status_code == 200:
    available_students2 = available_response2.json()
    print(f"✅ Got {len(available_students2)} available students")

    student_in_available2 = any(s['id'] == student_id for s in available_students2)
    if student_in_available2:
        print(f"   ❌ PROBLEM: Test student STILL in available list (duplicate prevention failed!)")
    else:
        print(f"   ✅ FIXED: Test student NOT in available list (successfully filtered out)")
else:
    print(f"❌ Failed to fetch available students: {available_response2.text}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
