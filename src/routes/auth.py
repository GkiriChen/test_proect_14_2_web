from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from src.database.db import get_db
from src.schemas import UserBan, UserModel, UserResponse, TokenModel, RequestEmail
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.email import send_email
from src.services.auth_admin import is_admin

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.

    :param body: Data for registering a new user.
    :type body: UserModel
    :param background_tasks: Background tasks.
    :type background_tasks: BackgroundTasks
    :param request: FastAPI request.
    :type request: Request
    :param db: Database session.
    :type db: AsyncSession
    :return: User object and a message indicating the successful user creation.
    :rtype: UserResponse
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    exist_user_name = await repository_users.get_user_by_username(body.username, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="An account for this email already exists")
    if exist_user_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="An account with this username already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(
        send_email, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

    """
    Authenticate a user and issue access tokens.

    :param body: Authentication data (email and password).
    :type body: OAuth2PasswordRequestForm
    :param db: Database session.
    :type db: AsyncSession
    :return: Access and refresh tokens for the user.
    :rtype: TokenModel
    """
    user = await repository_users.get_user_by_username(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    if user.ban:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You have been banned")

    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/logout", status_code=200)
async def logout(token: str = Depends(auth_service.oauth2_scheme)):
    """
    Log out the user and add their access_token to the "blacklist".

    :param token: The user's access_token for logging out.
    :type token: str
    """
    # Get the expiration time of the access_token
    payload = jwt.decode(token, auth_service.SECRET_KEY,
                         algorithms=[auth_service.ALGORITHM])
    expires_delta = payload["exp"] - payload["iat"]

    auth_service.add_to_blacklist(token, expires_delta)
    return {"message": "Successfully logged out"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: AsyncSession = Depends(get_db)):
    """
    Refresh the access token using the refresh token.

    :param credentials: Access credentials, including the refresh token.
    :type credentials: HTTPAuthorizationCredentials
    :param db: Database session.
    :type db: AsyncSession
    :return: Updated access and refresh tokens for the user.
    :rtype: TokenModel
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    Confirm a user's email using a confirmation token.

    :param token: Email confirmation token.
    :type token: str
    :param db: Database session.
    :type db: AsyncSession
    :return: A message indicating the email confirmation.
    :rtype: dict
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(get_db)):
    """
    Send an email confirmation request to a user.

    :param body: Data for the email confirmation request.
    :type body: RequestEmail
    :param background_tasks: Background tasks.
    :type background_tasks: BackgroundTasks
    :param request: FastAPI request.
    :type request: Request
    :param db: Database session.
    :type db: AsyncSession
    :return: A message indicating that an email has been sent for confirmation.
    :rtype: dict
    """
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}


@router.put("/ban", response_model=UserBan, dependencies=[Depends(is_admin)])
async def update_user_ban(
    username: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Update the ban status of a user.

    :param username: The username of the user to update.
    :type username: str
    :param current_user: The currently authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated user with the new ban status.
    :rtype: UserBan
    """

    user = await repository_users.update_user_ban(username, db)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
