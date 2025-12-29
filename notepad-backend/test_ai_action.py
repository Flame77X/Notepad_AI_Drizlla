import requests
import os
from dotenv import load_dotenv

load_dotenv()

# We need a valid JWT token to test the protected /chat endpoint
# For this test, we will assume we can get one, OR we temporarily bypass auth for a local test?
# Since bypassing auth requires code changes, we will use the `auth.py` logic if we had a token.
# BUT, getting a token programmatically requires a valid user login.
# Instead, we will simulate the behavior by manually invoking the function? No, that's unit testing.
# Let's try to login using the test user we created earlier to get a token.

API_URL = "http://127.0.0.1:8000"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_token():
    # Login to get token
    import requests
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {"apikey": SUPABASE_KEY, "Content-Type": "application/json"}
    # Use the email we debugged earlier
    payload = {"email": "rahul.test.debug+1@gmail.com", "password": "password123456"}
    
    # NOTE: If email is not confirmed, this might fail with "Email not confirmed"
    # If so, we can't fully automated test without a confirmed user.
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code != 200:
        print(f"Login failed: {res.text}")
        return None
    return res.json()["access_token"]

def main():
    print("1. Getting Auth Token...")
    token = get_token()
    if not token:
        print("❌ Could not get token (User might need email confirmation).")
        print("Skipping automated test. Please verify manually in UI.")
        return

    print("2. Sending Command: 'Create a note called AutoTest with content Success'")
    headers = {"Authorization": f"Bearer {token}"}
    
    # We send a natural language message
    files = {
        'message': (None, 'Create a note called AutoTest with content Success'),
    }
    
    try:
        res = requests.post(f"{API_URL}/chat", headers=headers, files=files)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.json()}")
        
        if "created the note" in res.json().get("reply", ""):
            print("✅ AI successfully processed the action!")
        else:
            print("⚠️ AI Reply didn't indicate success. Check logs.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
