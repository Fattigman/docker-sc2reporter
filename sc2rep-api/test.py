from fastapi.testclient import TestClient

from api.main import app
import json
client = TestClient(app)

def test_login():
    payload = "grant_type=&username=Test&password=Test&client_id=&client_secret="
    response = client.post('/login/token/', 
        headers={'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'},
        data=payload,
        )
    print('Testing /login/token...')
    print(vars(response))
    assert response.status_code == 200
    print('OK!')


def test_read_main():
    response = client.get("/")
    print('Testing "/" endpoint...')
    assert response.status_code == 200
    print('OK!')
    test_login()
    

test_read_main()