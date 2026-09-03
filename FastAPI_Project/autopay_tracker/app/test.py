from FastAPI_Project.autopay_tracker.app.security.jwt import create_access_token, decode_access_token

token = create_access_token({"user_id": 5})
print(token)   # long encoded string

payload = decode_access_token(token)
print(payload)   # {'user_id': 5, 'exp': ...}

print(decode_access_token("garbage-invalid-token"))   # None