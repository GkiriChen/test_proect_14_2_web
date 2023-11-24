from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field
from src.database.models import UserRole


class ImageTagModel(BaseModel):
    """
    Model for representing an image tag.
    
    :param tag_name: The name of the tag.
    :type tag_name: str
    """
    tag_name: str


class ImageTagResponse(BaseModel):
    """
    Model for representing the response of an image tag.
    
    :param tag_name: The name of the tag.
    :type tag_name: str
    """
    tag_name: str


class PhotoBase(BaseModel):
    """
    Base model for representing photo information.
    
    :param description: The description of the photo.
    :type description: str
    """
    description: str


class PhotoModels(PhotoBase):
    """
    Model for representing detailed photo information.
    
    :param id: The unique identifier of the photo.
    :type id: int
    :param user_id: The user ID associated with the photo.
    :type user_id: int
    :param tags: The list of tags associated with the photo.
    :type tags: List[ImageTagResponse]
    """
    id: int
    user_id: int
    tags: List[ImageTagResponse]


class RequestRoleConfig:
    arbitrary_types_allowed = True


class RequestRole(BaseModel):
    """
    Model for representing a role request.
    
    :param email: The email address associated with the user.
    :type email: EmailStr
    :param role: The requested user role.
    :type role: UserRole
    """
    email: EmailStr
    role: UserRole

    class Config(RequestRoleConfig):
        pass


class CommentSchema(BaseModel):
    """
    Schema for creating a comment.
    
    :param text: The text content of the comment.
    :type text: str
    :param photo_id: The ID of the photo to which the comment is associated.
    :type photo_id: int
    """
    id: int
    text: str = "some text"
    photo_id: int


class CommentList(BaseModel):
    """
    Schema for listing comments.
    
    :param limit: The maximum number of comments to retrieve.
    :type limit: int
    :param offset: The offset for paginating through comments.
    :type offset: int
    :param photo_id: The ID of the photo for which comments are to be retrieved.
    :type photo_id: int
    """
    limit: int = 10
    offset: int = 0
    photo_id: int


class CommentUpdateSchems(BaseModel):
    """
    Schema for updating a comment.
    
    :param id: The ID of the comment to be updated.
    :type id: int
    :param text: The new text for the comment.
    :type text: str
    """
    id: int
    text: str


class CommentRemoveSchema(BaseModel):
    """
    Schema for removing a comment.
    
    :param id: The ID of the comment to be removed.
    :type id: int
    """
    id: int


class RoleModel(BaseModel):
    """
    Model for representing a user role.
    
    :param id: The ID of the role.
    :type id: int
    :param role_name: The name of the role.
    :type role_name: str
    """
    id: int
    role_name: str


class UserModel(BaseModel):
    """
    Model for representing user information for registration.
    
    :param username: The username of the user.
    :type username: str
    :param first_name: The first name of the user.
    :type first_name: str
    :param last_name: The last name of the user.
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
    Model for user data in the database.
    
    :param id: The unique identifier of the user.
    :type id: int
    :param role_id: The unique identifier of the user's role.
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
    Model for a user response.
    
    :param user: The user's data.
    :type user: UserDb
    :param detail: A message indicating the success of a user-related operation.
    :type detail: str
    """
    user: UserDb
    detail: str = "User successfully created"


class UserBan(UserDb):
    """
    Model for user ban information.
    
    :param ban: Boolean indicating the ban status of the user.
    :type ban: bool
    """
    ban: bool


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
    """
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
