"""
Authentication Module
Validates JWT tokens from Supabase Auth
"""

import requests
from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")


def get_current_user(authorization: str = Header(None)):
    """
    Validates JWT token from Supabase Auth
    Returns the user object with user['id'], user['email'], etc.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Extract token from "Bearer <token>"
    token = authorization.replace("Bearer ", "").strip()
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token format")

    try:
        res = requests.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": SUPABASE_ANON_KEY
            },
            timeout=5
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth server error: {str(e)}")

    if res.status_code != 200:
        print(f"[DEBUG] Auth error: {res.status_code} - {res.text}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_data = res.json()
    
    # Verify user_data is a dictionary and has 'id'
    if not isinstance(user_data, dict):
        print(f"[DEBUG] User data is not dict: {type(user_data)}")
        raise HTTPException(status_code=401, detail="Invalid user data format")
    
    if "id" not in user_data:
        print(f"[DEBUG] User data missing 'id': {user_data.keys()}")
        raise HTTPException(status_code=401, detail="User ID not found in token")
    
    return user_data  # Returns dict with 'id', 'email', etc
