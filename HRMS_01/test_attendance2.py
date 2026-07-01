import urllib.request, json
import jwt

token = jwt.encode(
    {"user_id": 1, "email": "admin@horilla.com", "tenant_id": "public"},
    "change-me-in-production-use-openssl-rand-hex-32",
    algorithm="HS256"
)

req2 = urllib.request.Request('http://127.0.0.1:8003/api/v1/attendance', 
                              headers={'Authorization': f'Bearer {token}'})
try:
    resp2 = urllib.request.urlopen(req2)
    print(resp2.read().decode('utf-8'))
except Exception as e:
    print(e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
