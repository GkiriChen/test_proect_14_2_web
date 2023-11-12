
from typing import Optional
from pydantic import BaseModel, EmailStr
from src.database.models import UserRole


class RequestRoleConfig:
    arbitrary_types_allowed = True

class RequestRole(BaseModel):
    email: EmailStr
    role: UserRole
    
    class Config(RequestRoleConfig):
        pass



class CommentSchema(BaseModel):
    text: str = "some text"
    photo_id: int


class CommentList(BaseModel):
    limit: int = 10
    offset: int = 0
    photo_id: int


class CommentUpdateSchems(BaseModel):
    id: int
    text: str


class CommentResponse(BaseModel):
    username: str
    text: str
    photo_id: int


class CommentRemoveSchema(BaseModel):
    id: int
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field



class UserModel(BaseModel):
    """
    Model for a user. Contains user information for registration.

    :param username: The username of the user.
    :type username: str
    :param email: The email address of the user.
    :type email: str
    :param password: The user's password.
    :type password: str
    """
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Model for user data in the database. Extends BaseModel and includes additional user data.

    :param id: The unique identifier of the user.
    :type id: int
    :param username: The username of the user.
    :type username: str
    :param email: The email address of the user.
    :type email: str
    :param created_at: The date and time when the user account was created.
    :type created_at: datetime
    :param avatar: The URL to the user's avatar.
    :type avatar: str
    """
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Model for a user response. Contains user data and a detail message.

    :param user: The user's data.
    :type user: UserDb
    :param detail: A message indicating the success of a user-related operation.
    :type detail: str
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Model for an authentication token.

    :param access_token: The access token.
    :type access_token: str
    :param refresh_token: The refresh token.
    :type refresh_token: str
    :param token_type: The token type (default is "bearer").
    :type token_type: str
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    Model for requesting email-related operations.

    :param email: The email address for email-related operations.
    :type email: EmailStr
    """
    email: EmailStr

class UpdateUserProfileModel(BaseModel):
    """
    Model for updating a user's profile.

    :param avatar: The new avatar URL for the user.
    :type avatar: Optional[str]
    :param username: The new username for the user.
    :type username: Optional[str]
    :param email: The new email address for the user.
    :type email: Optional[EmailStr]
    """
    avatar: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]

