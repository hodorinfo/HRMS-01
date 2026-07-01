import urllib.request, json

req = urllib.request.Request('http://127.0.0.1:8001/api/v1/auth/login', 
                             data=b'username=admin@horilla.com&password=admin123',
                             headers={'Content-Type': 'application/x-www-form-urlencoded'})
try:
    resp = urllib.request.urlopen(req)
    token = json.loads(resp.read())['access_token']
    
    req2 = urllib.request.Request('http://127.0.0.1:8003/api/v1/attendance', 
                                  headers={'Authorization': f'Bearer {token}'})
    resp2 = urllib.request.urlopen(req2)
    print(resp2.read().decode('utf-8'))
except Exception as e:
    print(e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
