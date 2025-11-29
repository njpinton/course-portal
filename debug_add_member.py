#!/usr/bin/env python3
"""Debug script to understand the add member bug"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Test IDs from the logs
group_id = "cedba4eb-dab8-4f2c-8853-726dab465e95"
student_id = "f800e15e-8f83-4476-8fc7-9d84fbcbcf14"

print("=" * 80)
print("Testing Supabase query behavior")
print("=" * 80)

# Test 1: Query with correct student ID
print("\n1. Testing query with CORRECT student ID:")
print(f"   student_id = {student_id}")
try:
    response = supabase.table('students').select('group_id, first_name, last_name, campus_id').eq('id', student_id).execute()
    print(f"   ✅ Query successful: {response.data}")
except Exception as e:
    print(f"   ❌ Query failed: {e}")

# Test 2: Query with GROUP ID instead (what the logs showed)
print("\n2. Testing query with GROUP ID instead of student ID:")
print(f"   id = {group_id} (this is the GROUP ID, not student ID!)")
try:
    response = supabase.table('students').select('group_id, first_name, last_name, campus_id').eq('id', group_id).execute()
    print(f"   ✅ Query successful: {response.data}")
except Exception as e:
    print(f"   ❌ Query failed: {e}")

# Test 3: Query with .single()
print("\n3. Testing query with .single() on non-existent ID:")
try:
    response = supabase.table('students').select('group_id, first_name, last_name').eq('id', group_id).single().execute()
    print(f"   ✅ Query successful: {response.data}")
except Exception as e:
    print(f"   ❌ Query failed: {e}")

print("\n" + "=" * 80)
