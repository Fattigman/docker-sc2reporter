import json

from .test_base import client


def test_root():
    response = client.get("/")
    assert response.status_code == 200
