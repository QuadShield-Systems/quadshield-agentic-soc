import os

from dotenv import load_dotenv
from supabase import create_client

# ============================================
# LOAD ENV VARIABLES
# ============================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ============================================
# INITIALIZE CLIENT
# ============================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ============================================
# INSERT SECURITY RESULT
# ============================================

def insert_security_result(data):

    try:

        response = supabase.table(
            "security_logs"
        ).insert(data).execute()

        print("\n[+] Result inserted into Supabase\n")

        return response

    except Exception as error:

        print(f"\n[DB ERROR] {str(error)}")