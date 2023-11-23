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
    """
    Fixture function to provide an instance of the Auth class for testing.

    Returns:
    - Auth: Auth instance.
    """
    return Auth()


async def test_create_access_token(auth_service):
    """
    Test the `create_access_token` method of the Auth class.

    The method should create an access token without errors.

    Raises:
    - AssertionError: If the token is None.
    """
    user_data = {"sub": "test@example.com"}
    expires_delta = 3600  # 1 hour
    token = await auth_service.create_access_token(user_data, expires_delta)
    assert token is not None


async def test_create_refresh_token(auth_service):
    """
    Test the `create_refresh_token` method of the Auth class.

    The method should create a refresh token without errors.

    Raises:
    - AssertionError: If the token is None.
    """
    user_data = {"sub": "test@example.com"}
    expires_delta = 86400  # 1 day
    token = await auth_service.create_refresh_token(user_data, expires_delta)
    assert token is not None


async def test_decode_refresh_token(auth_service):
    """
    Test the `decode_refresh_token` method of the Auth class.

    The method should decode a refresh token without errors.

    Raises:
    - AssertionError: If the decoded email is not as expected.
    """
    user_data = {"sub": "test@example.com"}
    expires_delta = 86400  # 1 day
    refresh_token = await auth_service.create_refresh_token(user_data, expires_delta)

    decoded_email = await auth_service.decode_refresh_token(refresh_token)
    assert decoded_email == "test@example.com"


def test_verify_password(auth_service):
    """
    Test the `verify_password` method of the Auth class.

    The method should verify a password hash correctly.

    Raises:
    - AssertionError: If the verification results are not as expected.
    """
    plain_password = "testpassword"
    hashed_password = auth_service.get_password_hash(plain_password)

    assert auth_service.verify_password(
        plain_password, hashed_password) is True
    assert auth_service.verify_password(
        "wrongpassword", hashed_password) is False


async def test_create_email_token(auth_service):
    """
    Test the `create_email_token` method of the Auth class.

    The method should create an email token without errors.

    Raises:
    - AssertionError: If the token is None.
    """
    email_token_data = {"sub": "test@example.com"}
    email_token = auth_service.create_email_token(email_token_data)
    assert email_token is not None


async def test_get_email_from_token(auth_service):
    """
    Test the `get_email_from_token` method of the Auth class.

    The method should decode an email token without errors.

    Raises:
    - AssertionError: If the decoded email is not as expected.
    """
    email_token_data = {"sub": "test@example.com"}
    email_token = auth_service.create_email_token(email_token_data)

    decoded_email = await auth_service.get_email_from_token(email_token)
    assert decoded_email == "test@example.com"
