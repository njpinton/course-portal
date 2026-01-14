import os
import sys
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_ANON_KEY not set in environment.")
    sys.exit(1)

supabase = create_client(url, key)

def test_student_structure():
    try:
        # Get one student to see the exact structure
        response = supabase.table('students').select('*').limit(1).execute()
        if response.data:
            student = response.data[0]
            print("Sample student structure:")
            print(json.dumps(student, indent=2))

            print("\n--- Key fields ---")
            print(f"first_name: '{student.get('first_name', 'MISSING')}'")
            print(f"last_name: '{student.get('last_name', 'MISSING')}'")
            print(f"campus_id: '{student.get('campus_id', 'MISSING')}'")
            print(f"full_name: '{student.get('full_name', 'MISSING')}'")
            print(f"name: '{student.get('name', 'MISSING')}'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_student_structure()
