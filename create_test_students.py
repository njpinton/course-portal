import os
import sys
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_ANON_KEY not set in environment.")
    sys.exit(1)

supabase = create_client(url, key)

# Get first class ID
try:
    classes = supabase.table('classes').select('id, course_code, section').limit(1).execute()
    if not classes.data:
        print("No classes found! Please create a class first.")
        sys.exit(1)

    class_id = classes.data[0]['id']
    print(f"Using class: {classes.data[0]['course_code']} Section {classes.data[0]['section']}")
    print(f"Class ID: {class_id}\n")
except Exception as e:
    print(f"Error fetching class: {e}")
    sys.exit(1)

# Test students data
test_students = [
    {
        'first_name': 'JUAN',
        'last_name': 'DELA CRUZ',
        'middle_name': 'SANTOS',
        'campus_id': '2024001',
        'email': 'jdelacruz@test.edu.ph',
        'program': 'BSCS',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    },
    {
        'first_name': 'MARIA',
        'last_name': 'SANTOS',
        'middle_name': 'REYES',
        'campus_id': '2024002',
        'email': 'msantos@test.edu.ph',
        'program': 'BSCS',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    },
    {
        'first_name': 'PEDRO',
        'last_name': 'GARCIA',
        'middle_name': 'LOPEZ',
        'campus_id': '2024003',
        'email': 'pgarcia@test.edu.ph',
        'program': 'BSIT',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    },
    {
        'first_name': 'ANA',
        'last_name': 'MARTINEZ',
        'middle_name': 'FLORES',
        'campus_id': '2024004',
        'email': 'amartinez@test.edu.ph',
        'program': 'BSCS',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    },
    {
        'first_name': 'JOSE',
        'last_name': 'RIVERA',
        'middle_name': 'CRUZ',
        'campus_id': '2024005',
        'email': 'jrivera@test.edu.ph',
        'program': 'BSIT',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    },
    {
        'first_name': 'LUISA',
        'last_name': 'HERNANDEZ',
        'middle_name': 'DIAZ',
        'campus_id': '2024006',
        'email': 'lhernandez@test.edu.ph',
        'program': 'BSCS',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    },
    {
        'first_name': 'CARLOS',
        'last_name': 'MENDOZA',
        'middle_name': 'RAMOS',
        'campus_id': '2024007',
        'email': 'cmendoza@test.edu.ph',
        'program': 'BSCS',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    },
    {
        'first_name': 'ISABELLA',
        'last_name': 'FERNANDEZ',
        'middle_name': 'TORRES',
        'campus_id': '2024008',
        'email': 'ifernandez@test.edu.ph',
        'program': 'BSIT',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    },
    {
        'first_name': 'MIGUEL',
        'last_name': 'GUTIERREZ',
        'middle_name': 'SANCHEZ',
        'campus_id': '2024009',
        'email': 'mgutierrez@test.edu.ph',
        'program': 'BSCS',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    },
    {
        'first_name': 'SOFIA',
        'last_name': 'RAMIREZ',
        'middle_name': 'MORALES',
        'campus_id': '2024010',
        'email': 'sramirez@test.edu.ph',
        'program': 'BSCS',
        'enlistment_status': 'Finalized',
        'class_id': class_id,
        'group_id': None
    }
]

print("Creating test students...")
print("=" * 60)

created_count = 0
for student in test_students:
    try:
        # Check if student already exists
        existing = supabase.table('students').select('id').eq('campus_id', student['campus_id']).execute()

        if existing.data:
            print(f"⚠️  {student['first_name']} {student['last_name']} (ID: {student['campus_id']}) - Already exists, skipping")
        else:
            result = supabase.table('students').insert(student).execute()
            print(f"✅ {student['first_name']} {student['last_name']} (ID: {student['campus_id']}) - Created successfully")
            created_count += 1
    except Exception as e:
        print(f"❌ {student['first_name']} {student['last_name']} - Error: {e}")

print("=" * 60)
print(f"\n✨ Summary: {created_count} new students created")
print(f"📋 Total test students available: {len(test_students)}")
print(f"\n🎓 All students are in class: {classes.data[0]['course_code']} Section {classes.data[0]['section']}")
print("\nYou can now test adding these students to your groups!")
