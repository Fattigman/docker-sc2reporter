import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException
from jose import JWTError

from authentication import (
    verify_password,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user,
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample user for testing
sample_user = {
    "username": "testuser",
    "password": "$2b$12$5/7p/.eeFzwG326rFbNfNOZepLQSPvrslrvCJu4//ZukzygyM1d6m",  # Hash for "password"
    "disabled": False,
}


def test_verify_password():
    assert (
        verify_password("password", sample_user["password"]) == True
    ), "Correct password test failed"
    assert (
        verify_password("wrongpassword", sample_user["password"]) == False
    ), "Wrong password test failed"


@pytest.mark.asyncio
async def test_authenticate_user_valid():
    with patch("authentication.get_user", return_value=sample_user):
        user = await authenticate_user("testuser", "password")
        assert user == sample_user


@pytest.mark.asyncio
async def test_authenticate_user_invalid():
    with patch("authentication.get_user", return_value=sample_user):
        user = await authenticate_user("testuser", "wrongpassword")
        assert user is False


@pytest.mark.asyncio
async def test_authenticate_user_not_found():
    with patch("authentication.get_user", return_value=None):
        user = await authenticate_user("testuser", "password")
        assert user is False


def test_create_access_token():
    token = create_access_token({"sub": "testuser"})
    assert token is not None


@pytest.mark.asyncio
async def test_get_current_user_valid():
    # Mocking the decode function to return valid data
    with patch("jose.jwt.decode", return_value={"sub": "testuser"}):
        with patch("authentication.get_user", return_value=sample_user):
            user = await get_current_user("valid_token")
            assert user == sample_user


@pytest.mark.asyncio
async def test_get_current_user_invalid():
    with patch("jose.jwt.decode", side_effect=JWTError()):
        with pytest.raises(HTTPException):
            await get_current_user("invalid_token")


@pytest.mark.asyncio
async def test_get_current_active_user_valid():
    user = await get_current_active_user(sample_user)
    assert user == sample_user


@pytest.mark.asyncio
async def test_get_current_active_user_disabled():
    disabled_user = {**sample_user, "disabled": True}
    with pytest.raises(HTTPException):
        await get_current_active_user(disabled_user)
