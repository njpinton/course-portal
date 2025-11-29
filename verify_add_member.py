#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Check if the student is now in the group
student_id = "f800e15e-8f83-4476-8fc7-9d84fbcbcf14"
group_id = "cedba4eb-dab8-4f2c-8853-726dab465e95"

response = supabase.table('students').select('id, first_name, last_name, group_id').eq('id', student_id).execute()

if response.data:
    student = response.data[0]
    print(f"\n✅ Student in database:")
    print(f"   Name: {student['first_name']} {student['last_name']}")
    print(f"   Group ID: {student['group_id']}")
    if student['group_id'] == group_id:
        print(f"   ✅ Correctly assigned to group!")
    else:
        print(f"   ❌ Not assigned to the correct group")
else:
    print("❌ Student not found")

# Also check group_members table
print(f"\n📋 Members in group {group_id[:8]}...")
members_response = supabase.table('group_members').select('*').eq('group_id', group_id).execute()
print(f"   Total members: {len(members_response.data)}")
for member in members_response.data[-3:]:  # Show last 3
    print(f"   - {member['member_name']}")
