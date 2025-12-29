# get_supabase_token.py
# Run:  python get_supabase_token.py
# It will print a Supabase access token you can use as
#   Authorization: Bearer <token>
# in Swagger and in your frontend.

from supabase import create_client, Client

# 1) Your project settings (from Supabase → Settings → API)
SUPABASE_URL = "https://ehbuobqvofyvaeqqgmpu.supabase.co"
SUPABASE_ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVoYnVvYnF2b2Z5dmFlcXFnbXB1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY0OTc0NjEsImV4cCI6MjA4MjA3MzQ2MX0."
    "zxTlw-RH3KdGIqhNhPAJMb3qPdCvMgiJJG2lZI88qqE"
)

# 2) Your Supabase Auth user (from Authentication → Users)
EMAIL = "rahulsandeshx3000@gmail.com"
PASSWORD = "1234"  # make sure this matches the password set in Supabase Auth

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def main() -> None:
    # Sign in with email/password and print the access token
    res = supabase.auth.sign_in_with_password(
        {"email": EMAIL, "password": PASSWORD}
    )

    session = res.session
    if session is None:
        raise RuntimeError("No session returned; check email/password in Supabase Auth.")

    print("ACCESS TOKEN:\n")
    print(session.access_token)


if __name__ == "__main__":
    main()
