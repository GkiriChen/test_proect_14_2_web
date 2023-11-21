import pytest
from src.services.auth import Auth


test_user_data = {
    "email": "test@example.com",
    "password": "testpassword",
}

test_secret_key = "testsecretkey"
test_algorithm = "HS256"


@pytest.fixture
def auth_service():
    return Auth()


async def test_create_access_token(auth_service):
    user_data = {"sub": "test@example.com"}
    expires_delta = 3600  
    token = await auth_service.create_access_token(user_data, expires_delta)
    assert token is not None


async def test_create_refresh_token(auth_service):
    user_data = {"sub": "test@example.com"}
    expires_delta = 86400  
    token = await auth_service.create_refresh_token(user_data, expires_delta)
    assert token is not None


async def test_decode_refresh_token(auth_service):
    user_data = {"sub": "test@example.com"}
    expires_delta = 86400  # 1 день
    refresh_token = await auth_service.create_refresh_token(user_data, expires_delta)

    decoded_email = await auth_service.decode_refresh_token(refresh_token)
    assert decoded_email == "test@example.com"


def test_verify_password(auth_service):
    plain_password = "testpassword"
    hashed_password = auth_service.get_password_hash(plain_password)

    assert auth_service.verify_password(
        plain_password, hashed_password) is True
    assert auth_service.verify_password(
        "wrongpassword", hashed_password) is False


async def test_create_email_token(auth_service):
    email_token_data = {"sub": "test@example.com"}
    email_token = auth_service.create_email_token(email_token_data)
    assert email_token is not None


async def test_get_email_from_token(auth_service):
    email_token_data = {"sub": "test@example.com"}
    email_token = auth_service.create_email_token(email_token_data)

    decoded_email = await auth_service.get_email_from_token(email_token)
    assert decoded_email == "test@example.com"


def test_add_to_blacklist(auth_service):
    access_token = "test_access_token"
    expires_delta = 3600  
    auth_service.add_to_blacklist(access_token, expires_delta)

    assert auth_service.r.get(f"blacklist:{access_token}") is not None
