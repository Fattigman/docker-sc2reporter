import json

from .test_base import client


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_login():
    payload = "grant_type=&username=Test&password=Test&client_id=&client_secret="
    response = client.post(
        "/login/token/",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json",
        },
        data=payload,
    )
    assert response.status_code == 200
