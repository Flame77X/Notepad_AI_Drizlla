from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Error: Missing env vars")
    exit(1)

print(f"Connecting to {url}...")
try:
    supabase: Client = create_client(url, key)
    print("Client created successfully.")
    
    # Try a simple select to verify connection (anon key usually allows reading public tables if RLS permits, or just existence check)
    # We will try to sign up a test user to see the raw error
    email = "rahul.test.debug+1@gmail.com"
    password = "password123456"
    
    print(f"Attempting to sign up {email}...")
    res = supabase.auth.sign_up({"email": email, "password": password})
    
    print("Sign Up Result:", res)

except Exception as e:
    print(f"Error: {e}")
