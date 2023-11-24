from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ImageTagModel(BaseModel):
    """
    The **ImageTagModel** class defines the structure for representing a single image tag.
    
    :param tag: str: The tag associated with the image.
    """
    tag: str


class ImageCircleModel(BaseModel):
    """
    The **ImageCircleModel** class defines the structure for representing the circular transformation parameters of an image.
    
    :param use_filter: bool: A flag indicating whether to apply circular transformation.
    :param height: int: The height of the circular transformation.
    :param width: int: The width of the circular transformation.
    """
    use_filter: bool = False
    height: int = Field(ge=0, default=400)
    width: int = Field(ge=0, default=400)


class ImageEffectModel(BaseModel):
    """
    The **ImageEffectModel** class defines the structure for representing the artistic effects to apply to an image.
    
    :param use_filter: bool: A flag indicating whether to apply artistic effects.
    :param art_audrey: bool: A flag indicating whether to apply the Audrey artistic effect.
    :param art_zorro: bool: A flag indicating whether to apply the Zorro artistic effect.
    :param cartoonify: bool: A flag indicating whether to apply a cartoonifying effect.
    :param blur: bool: A flag indicating whether to apply a blurring effect.
    """
    use_filter: bool = False
    art_audrey: bool = False
    art_zorro: bool = False
    cartoonify: bool = False
    blur: bool = False


class ImageResizeModel(BaseModel):
    """
    The **ImageResizeModel** class defines the structure for representing the resizing parameters of an image.
    
    :param use_filter: bool: A flag indicating whether to apply resizing.
    :param crop: bool: A flag indicating whether to crop the image during resizing.
    :param fill: bool: A flag indicating whether to fill the image during resizing.
    :param height: int: The height of the resized image.
    :param width: int: The width of the resized image.
    """
    use_filter: bool = False
    crop: bool = False
    fill: bool = False
    height: int = Field(ge=0, default=400)
    width: int = Field(ge=0, default=400)


class ImageRotateModel(BaseModel):
    """
    The **ImageRotateModel** class defines the structure for representing the rotation parameters of an image.
    
    :param use_filter: bool: A flag indicating whether to apply rotation.
    :param width: int: The width of the rotated image.
    :param degree: int: The degree of rotation (should be between -360 and 360).
    """
    use_filter: bool = False
    width: int = Field(ge=0, default=400)
    degree: int = Field(ge=-360, le=360, default=45)


class EditImageModel(BaseModel):
    """
    The **EditImageModel** class defines the structure for representing the editing parameters of an image.
    
    :param circle: ImageCircleModel: Circular transformation parameters.
    :param effect: ImageEffectModel: Artistic effects parameters.
    :param resize: ImageResizeModel: Resizing parameters.
    :param rotate: ImageRotateModel: Rotation parameters.
    """
    circle: ImageCircleModel
    effect: ImageEffectModel
    resize: ImageResizeModel
    rotate: ImageRotateModel


class ImageBase(BaseModel):
    """
    The **ImageBase** class defines the base structure for representing an image.
    
    :param image_url: str: The URL of the image.
    :param description: Optional[str]: The optional description of the image.
    """
    image_url: str = Field(max_length=500)
    description: Optional[str] = Field(max_length=500)
    qr_code_url: Optional[str]

class ImageModel(ImageBase):
    """
    The **ImageModel** class defines the structure for representing a detailed image with additional metadata.
    
    :param id: int: The unique identifier of the image.
    :param created_at: datetime: The timestamp when the image was created.
    :param updated_at: Optional[datetime]: The timestamp when the image was last updated.
    :param user_id: int: The user ID associated with the image.
    :param tags: List[str]: The list of tags associated with the image.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int
    tags: List[str]

    class Config:
        from_attributes = True



class ImageModellist(ImageBase):
    """
    The **ImageModellist** class defines the structure for representing a simplified image without additional metadata.
    
    :param id: int: The unique identifier of the image.
    :param created_at: datetime: The timestamp when the image was created.
    :param updated_at: Optional[datetime]: The timestamp when the image was last updated.
    :param user_id: int: The user ID associated with the image.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int

    class Config:
        from_attributes = True


class ImageResponseCreated(ImageModelCreate):

    """
    The **ImageResponseCreated** class defines the structure for representing a response when an image is successfully created.
    
    :param detail: str: The detail message indicating the success of the creation.
    """

    detail: str = "Image successfully created"

    class Config:
        from_attributes = True



class ImageResponseUpdated(ImageModelCreate):

    """
    The **ImageResponseUpdated** class defines the structure for representing a response when an image's description is successfully updated.
    
    :param detail: str: The detail message indicating the success of the update.
    """

    detail: str = "Image description successfully updated"

    class Config:
        from_attributes = True



class ImageResponseEdited(ImageModelCreate):

    """
    The **ImageResponseEdited** class defines the structure for representing a response when an image is successfully edited.
    
    :param detail: str: The detail message indicating the success of the edit.
    """

    detail: str = "Image successfully edited"

    class Config:
        from_attributes = True
