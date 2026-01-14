
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

def get_all_classes():
    try:
        response = supabase.table('classes').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Error fetching classes: {e}")
        return []

def get_all_students_for_class(class_id):
    try:
        response = supabase.table('students').select('*').eq('class_id', class_id).order('last_name').execute()
        return response.data
    except Exception as e:
        print(f"Error fetching students for class {class_id}: {e}")
        return []

def get_ungrouped_students_for_class(class_id):
    try:
        response = supabase.table('students').select('id, first_name, last_name, campus_id, group_id').eq('class_id', class_id).is_('group_id', 'null').order('last_name').execute()
        return response.data
    except Exception as e:
        print(f"Error fetching ungrouped students for class {class_id}: {e}")
        return []

def main():
    print("--- Verifying Classes ---")
    classes = get_all_classes()
    if classes:
        print(f"Found {len(classes)} classes:")
        for cls in classes:
            print(f"  Class ID: {cls['id']}, Course: {cls['course_code']}, Section: {cls['section']}")
        
        # Pick the first class to inspect students
        test_class_id = classes[0]['id']
        print(f"\n--- Inspecting students for class {classes[0]['course_code']} {classes[0]['section']} (ID: {test_class_id}) ---")

        all_students = get_all_students_for_class(test_class_id)
        if all_students:
            print(f"Total students in class: {len(all_students)}")
            for student in all_students:
                print(f"  Student: {student['first_name']} {student['last_name']} (Group ID: {student['group_id']})")
        else:
            print(f"No students found in class {test_class_id}.")

        ungrouped_students = get_ungrouped_students_for_class(test_class_id)
        if ungrouped_students:
            print(f"\nUngrouped students in class ({len(ungrouped_students)}):")
            for student in ungrouped_students:
                print(f"  - {student['first_name']} {student['last_name']} (ID: {student['id']})")
        else:
            print(f"\nNo ungrouped students found in class {test_class_id}. All might be grouped or none exist.")

    else:
        print("No classes found in the database.")

if __name__ == "__main__":
    main()
