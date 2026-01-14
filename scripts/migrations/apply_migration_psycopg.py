import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

# Construct connection string properly
# The password has special characters, so we need to handle it carefully
host = "aws-0-ap-southeast-1.pooler.supabase.com"
port = 6543
database = "postgres"
user = "postgres.pmbhrbqdkhxhgjvtqrna"
password = "Arnel@070701"  # Fixed - @ should only separate user from host, not be in password

try:
    # Create connection using connection parameters (safer than URL string)
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    
    # Execute migration
    migration_sql = """
    ALTER TABLE IF EXISTS public.groups
    ADD COLUMN IF NOT EXISTS problem_statement TEXT,
    ADD COLUMN IF NOT EXISTS dataset_source TEXT,
    ADD COLUMN IF NOT EXISTS dataset_size TEXT;
    """
    
    cursor.execute(migration_sql)
    conn.commit()
    print("✅ Migration applied successfully!")
    
    # Verify columns were added
    cursor.execute("""
    SELECT column_name FROM information_schema.columns 
    WHERE table_name = 'groups' ORDER BY column_name;
    """)
    columns = cursor.fetchall()
    print("\nGroups table columns:")
    for col in columns:
        print(f"  - {col[0]}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
