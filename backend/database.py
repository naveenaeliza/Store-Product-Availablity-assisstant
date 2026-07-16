import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Read Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validate credentials
if not SUPABASE_URL:
    raise Exception("SUPABASE_URL not found in environment variables.")

if not SUPABASE_KEY:
    raise Exception("SUPABASE_KEY not found in environment variables.")

# Create Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def get_supabase_client() -> Client:
    """
    Returns the initialized Supabase client.
    """
    return supabase