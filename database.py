import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env
load_dotenv()

# Read credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validate credentials
if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase credentials not found. Check your .env file.")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_supabase_client():
    """
    Returns the initialized Supabase client.
    """
    return supabase