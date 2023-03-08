import json

from .test_base import client


def test_root():
    response = client.get("/")
    print('Testing "/" endpoint...')
    assert response.status_code == 200
    print('OK!')

def test_login():
    payload = "grant_type=&username=Test&password=Test&client_id=&client_secret="
    response = client.post('/login/token', 
        headers={'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'},
        data=payload,
        )
    print('Testing /login/token...')
    assert response.status_code == 200
    print('OK!')


def test_read_main():
    test_root()
    test_login()
    

test_read_main()