from database import get_supabase_client

db = get_supabase_client()

try:
    response = db.table("products").select("*").execute()
    print("✅ Connected Successfully!")
    print(response.data)
except Exception as e:
    print("❌ Connection Failed")
    print(e)