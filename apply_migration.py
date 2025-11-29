import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

# Read and execute the migration
migration_sql = """
ALTER TABLE IF EXISTS public.groups
ADD COLUMN IF NOT EXISTS problem_statement TEXT,
ADD COLUMN IF NOT EXISTS dataset_source TEXT,
ADD COLUMN IF NOT EXISTS dataset_size TEXT;
"""

try:
    result = supabase.query(migration_sql)
    print("✅ Migration applied successfully!")
except Exception as e:
    print(f"❌ Error applying migration: {e}")
    # Try an alternative approach - use RPC or manual insertion
    print("Attempting alternative approach...")
