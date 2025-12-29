import jwt
import datetime

JWT_SECRET = "7uDDSaQRMZT5b/O4KFjvdqhTt2eiXrN1iLUWyCvMnbrVUoy839mQG2lNkihoY4yWEgj1xJJVOppGHOld4oNIcQ=="
USER_ID = "b5c20485-31a1-4534-b953-1cdb9f1fb9ed"

payload = {
    "sub": USER_ID,
    "role": "authenticated",
    "aud": "authenticated",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
}

token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
print(token)
