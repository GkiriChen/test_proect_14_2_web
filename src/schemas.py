from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

from pydantic import BaseModel, EmailStr
from src.database.models import UserRole


class ImageTagModel(BaseModel):
    tag_name: str


class ImageTagResponse(BaseModel):
    tag_name: str


class PhotoBase(BaseModel):
    description: str


class PhotoModels(PhotoBase):
    id: int
    user_id: int
    tags: List[ImageTagResponse]


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


class CommentRemoveSchema(BaseModel):
    id: int


class RoleModel(BaseModel):
    id: int
    role_name: str


class UserModel(BaseModel):
    """
    Model for a user. Contains user information for registration.

    :param username: The username of the user.
    :type username: str
    :param first_name: The first name of the user.
    :type first_name: str
    :param last_name: The first name of the user.
    :type last_name: str
    :param email: The email address of the user.
    :type email: str
    :param password: The user's password.
    :type password: str
    """
    username: str = Field(min_length=5, max_length=16)
    first_name: str = Field(min_length=0, max_length=25)
    last_name: str = Field(min_length=0, max_length=25)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Model for user data in the database. Extends BaseModel and includes additional user data.

    :param id: The unique identifier of the user.
    :type id: int
    :param role_id: The unique identifier of the user`s role.
    :type role_id: int
    :param username: The username of the user.
    :type username: str
    :param first_name: The first name of the user.
    :type first_name: str
    :param last_name: The last name of the user.
    :type last_name: str
    :param email: The email address of the user.
    :type email: str
    :param created_at: The date and time when the user account was created.
    :type created_at: datetime
    :param avatar: The URL to the user's avatar.
    :type avatar: str
    """
    id: int
    role_id: int
    username: str
    first_name: str
    last_name: str
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

    :param username: The new username for the user.
    :type username: Optional[str]
    :param first_name: The new first name for the user.
    :type first_name: Optional[str]
    :param last_name: The new last name for the user.
    :type last_name: Optional[str]
    :param email: The new email address for the user.
    :type email: Optional[EmailStr]
    """

    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
