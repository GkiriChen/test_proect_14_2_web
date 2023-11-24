import pytest
from unittest.mock import AsyncMock
from sqlalchemy.future import select
from src.database.models import User


async def test_create_user(client, user, monkeypatch):
    """
    Test creating a new user through the signup API endpoint.

    Parameters:
    - client: TestClient - FastAPI test client.
    - user: dict - User data for signup.
    - monkeypatch: MonkeyPatch - Pytest monkeypatch fixture for mocking.

    The test checks if a new user can be successfully created, and the expected response details.
    """
    mock_send_email = AsyncMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def test_repeat_create_user(client, user):
    """
    Test attempting to create a user with an existing account.

    Parameters:
    - client: TestClient - FastAPI test client.
    - user: dict - User data for signup.

    The test checks if attempting to create a user with an existing account results in the expected conflict response.
    """
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client, user):
    """
    Test logging in with an unconfirmed email.

    Parameters:
    - client: TestClient - FastAPI test client.
    - user: dict - User data for login.

    The test checks if attempting to log in with an unconfirmed email results in the expected unauthorized response.
    """
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('username'),
              "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


@pytest.mark.asyncio
async def test_login_user(client, session, user):
    """
    Test logging in with a confirmed email.

    Parameters:
    - client: TestClient - FastAPI test client.
    - session: AsyncSession - Async database session.
    - user: dict - User data for login.

    The test checks if logging in with a confirmed email results in a successful login and the expected token type.
    """
    current_user: User = await session.execute(select(User).where(User.email == user.get('email')))
    current_user = current_user.scalar()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('username'),
              "password": user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, user):
    """
    Test logging in with an incorrect password.

    Parameters:
    - client: TestClient - FastAPI test client.
    - user: dict - User data for login.

    The test checks if attempting to log in with an incorrect password results in the expected unauthorized response.
    """
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('username'), "password": 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_login_wrong_email(client, user):
    """
    Test logging in with an incorrect email.

    Parameters:
    - client: TestClient - FastAPI test client.
    - user: dict - User data for login.

    The test checks if attempting to log in with an incorrect email results in the expected unauthorized response.
    """
    response = client.post(
        "/api/auth/login",
        data={"username": 'email', "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"
