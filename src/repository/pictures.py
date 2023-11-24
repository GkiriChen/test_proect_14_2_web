from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy import func
from src.database.models import User, Image, Tag, TagsImages
from src.schemas_pictures import EditImageModel

from src.services.cloud_image import CloudImage
from cloudinary import CloudinaryImage
import qrcode


async def create_taglist(tags: str) -> list:
    """
    Create a list of tags from a string.

    :param tags: str: The string containing tags.
    :return: list: A list of tags.
    """
    return [tg for tg in tags.strip().split(' ') if '#' in tg][:5]


async def add_tags_to_db(tags: str, image, db: AsyncSession):
    """
    Add tags to the database.

    :param tags: str: The tags to add.
    :param image: Image: The image object.
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: None
    """
    tag_list = await create_taglist(tags)
    for tg in tag_list:
        psql = select(Tag).filter_by(tag=tg)
        result = await db.execute(psql)
        if not result.fetchone():
            new_tag = Tag(tag=tg)
            db.add(new_tag)
            await db.commit()
            await db.refresh(new_tag)
        else:
            psql = select(Tag.id).where(Tag.tag == tg)
            result = await db.execute(psql)
            new_tag = result.fetchone()
        tag_pic = TagsImages(image_id=image.id, tag_id=new_tag.id)
        db.add(tag_pic)
        await db.commit()
        await db.refresh(tag_pic)


async def create(description: str, tags, image_url: str, public_id: str, user: User, db: AsyncSession):
    """
    Create a new image in the database.

    :param description: str: The description of the image.
    :param tags: str: The tags to add.
    :param image_url: str: The URL of the image.
    :param public_id: str: The public ID of the image.
    :param user: User: The user object.
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: Image: The newly created image object.
    """
    image = Image(description=description, image_url=image_url,
                  public_id=public_id, user_id=user.id)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    await add_tags_to_db(tags, image, db)
    return image


async def get_images(limit: int, offset: int, user: User, db: AsyncSession):
    """
    Get a list of images from the database.

    :param limit: int: The number of images to return.
    :param offset: int: The number of images to skip.
    :param user: User: The user object.
    :param db: AsyncSession: A connection to our Postgres SQL database.

    :return: list: A list of image objects.
    """
    result = await db.execute(select(Image, Tag).filter(Image.user_id == user.id)
                              .order_by(Image.created_at.desc()).limit(limit).offset(offset))
    images = result.fetchall()
    if images:
        im_dick = []
        for o in images:
            im_dick.append(o[0])
        return im_dick
    else:
        return None
    
async def get_images_me(limit: int, offset: int, user: User, db: AsyncSession):
    '''
    The **get_images** function gets all the images from the database.
    
    :param limit: int: The number of images to return
    :param offset: int: The number of images to skip
    :param user: User: The user object
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: A list of image objects
    '''
   
    
    result = await db.execute(select(Image).filter(Image.user_id == user.id)
                              .order_by(Image.created_at.desc()).limit(limit).offset(offset))
    images = result.fetchall()
    if images:
        im_dick = []
        for o in images:
            im_dick.append(o[0])
        return im_dick
    else:
        return None



async def get_image(image_id: int, user: User, db: AsyncSession):
    """
    Get details of a single image from the database.

    :param image_id: int: The ID of the image to retrieve.
    :param user: User: The user object.
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: dict: A dictionary containing image details.
    """
    images_alias = aliased(Image, name="images")
    tags_images_alias = aliased(TagsImages, name="tags_images")
    tags_alias = aliased(Tag, name="tags")

    psql2 = await db.execute(
        select(
            images_alias.image_url,
            images_alias.qr_code_url,
            images_alias.description,
            images_alias.id,
            images_alias.created_at,
            images_alias.updated_at,
            images_alias.user_id,
            func.ARRAY_AGG(tags_alias.tag).label("tags")
        )
        .join(tags_images_alias, images_alias.id == tags_images_alias.image_id)
        .join(tags_alias, tags_images_alias.tag_id == tags_alias.id)
        .filter(images_alias.id == image_id)
        .group_by(images_alias.description, images_alias.id, images_alias.user_id)
    )

    result = psql2.fetchall()
    if result:
        result_dict = dict(result[0]._asdict())
        return result_dict
    else:
        return None


async def get_image_from_id(image_id: int, user: User, db: AsyncSession):
    """
    Get a single image by ID from the database.

    :param image_id: int: The ID of the image to retrieve.
    :param user: User: The user object.
    :param db: AsyncSession: A connection to our Postgres SQL database.

    :return: Image: The image object.
    """
    psql = await db.execute(select(Image).filter(Image.id == image_id, Image.user_id == user.id))
    image = psql.fetchone()
    return image[0]



async def get_image_from_url(image_url: str, user: User, db: AsyncSession):
    """
    Get a single image by URL from the database.

    :param image_url: str: The URL of the image to retrieve.
    :param user: User: The user object.
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: Image: The image object.
    """
    psql = select(Image).filter(Image.image_url ==
                                image_url, Image.user_id == user.id)
    result = await db.execute(psql)
    image = result.fetchone()
    return image


async def remove(image_id: int, user: User, db: AsyncSession):
    """
    Delete a single image from the database.

    :param image_id: int: The ID of the image to delete.
    :param user: User: The user object.
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: Image: The deleted image object.
    """
    image = await get_image_from_id(image_id, user, db)
    if image:
        await db.delete(image)
        await db.commit()
        return image
    else:
        return None

async def remove_admin(id: int, db: AsyncSession):
    '''
    The **remove** function deletes a single image from the database.
        
    :param image_id: int: The id of the image to delete
    :param user: User: The user object
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: A image object
    '''
    image = await db.get(Image, id)
    if image:
        await db.delete(image)
        await db.commit()
        return image
    else:
        return None

async def image_editor(image_id: int, body: EditImageModel, user: User, db: AsyncSession):
    """
    Edit a single image in the database.

    :param image_id: int: The ID of the image to edit.
    :param body: EditImageModel: The body of the request.
    :param user: User: The user object.
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: Image: The edited image object.
    """
    image = await get_image_from_id(image_id, user, db)
    if image:
        edit_data = []

        if body.circle.use_filter and body.circle.height and body.circle.width:
            trans_list = [{'gravity': "face", 'height': f"{body.circle.height}", 'width': f"{body.circle.width}",
                           'crop': "thumb"},
                          {'radius': "max"}]
            [edit_data.append(elem) for elem in trans_list]
        if body.effect.use_filter:
            effect = ""
            if body.effect.art_audrey:
                effect = "art:audrey"
            if body.effect.art_zorro:
                effect = "art:zorro"
            if body.effect.blur:
                effect = "blur:300"
            if body.effect.cartoonify:
                effect = "cartoonify"
            if effect:
                edit_data.append({"effect": f"{effect}"})
        if body.resize.use_filter and body.resize.height and body.resize.height:
            crop = ""
            if body.resize.crop:
                crop = "crop"
            if body.resize.fill:
                crop = "fill"
            if crop:
                trans_list = [{"gravity": "auto",
                               'height': f"{body.resize.height}",
                               'width': f"{body.resize.width}",
                               'crop': f"{crop}"}]
                [edit_data.append(elem) for elem in trans_list]
        if body.rotate.use_filter and body.rotate.width and body.rotate.degree:
            trans_list = [{'width': f"{body.rotate.width}", 'crop': "scale"}, {'angle': "vflip"},
                          {'angle': f"{body.rotate.degree}"}]
            [edit_data.append(elem) for elem in trans_list]
        if edit_data:
            CloudImage()

            new_image = CloudinaryImage(image.public_id).image(
                transformation=edit_data)
            new_image = new_image[10:-3]
            image.image_url = new_image
            image.updated_at = datetime.now()
            await db.commit()
            await db.refresh(image)
            return image


async def edit_description(image_id: int, description: str, user: User, db: AsyncSession):
    """
    Edit the description of a single image in the database.

    :param image_id: int: The ID of the image to edit.
    :param description: str: The new description for the image.
    :param user: User: The user object.
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: Image: The edited image object.
    """
    image = await get_image_from_id(image_id, user, db)
    if image:
        image.description = description
        await db.commit()
        await db.refresh(image)
        return image


async def qr_code_generator(image_id: int, user: User, db: AsyncSession):
    """
    Generate a QR code for a single image in the database.

    :param image_id: int: The ID of the image to generate the QR code for.
    :param user: User: The user object.
    :param db: AsyncSession: A connection to our Postgres SQL database.
    :return: Image: The image object with the generated QR code URL.
    """
    image = await get_image_from_id(image_id, user, db)
    if image:
        image_url = image.image_url
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(image_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        img.save(f'./src/services/qrcodes/{image_id}.png')
        public_id = CloudImage.generate_name_image()
        file = f'./src/services/qrcodes/{image_id}.png'
        CloudImage.upload(file, public_id, overwrite=False)
        image_url = CloudImage.get_url_for_image(public_id)


        # f'./src/services/qrcodes/{image_id}.png'
        image.qr_code_url = image_url
        await db.commit()
        await db.refresh(image)
        return image
