import pytest
from sqlalchemy.future import select
from src.database.models import Base, User, Image, Tag, TagsImages
from src.repository.pictures import (
    create_taglist, add_tags_to_db, create, get_images,
    get_image, get_image_from_id, get_image_from_url,
    remove, image_editor, edit_description, qr_code_generator
)
from src.schemas_pictures import EditImageModel


@pytest.mark.asyncio
async def test_create_taglist():
    """Test create_taglist function."""
    tags = "tag1 tag2 #tag3 tag4 #tag5"
    result = await create_taglist(tags)
    assert result == ["#tag3", "#tag5"]


@pytest.mark.asyncio
async def test_create(session, user):
    """Test create function."""
    db = session

    user_instance = User(**user)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)

    description = "Test Image"
    tags = "#tag1 #tag2"
    image_url = "https://example.com/test.jpg"
    public_id = "test_public_id"

    result = await db.execute(select(Image))
    assert result.fetchall() == []

    image = await create(description, tags, image_url, public_id, user_instance, db)

    assert image is not None
    assert image.id is not None
    assert image.description == description

    result = await db.execute(select(TagsImages))
    tags_images = result.fetchall()
    assert tags_images != []
    assert len(tags_images) == len(tags.split())

    await remove(image.id, user_instance, db)
    await db.delete(user_instance)
    await db.commit()


@pytest.mark.asyncio
async def test_add_tags_to_db(session, user):
    """Test add_tags_to_db function."""
    db = session
    description = "Test Image"
    tags = "#tag4 #tag6"
    image_url = "https://example.com/test.jpg"
    public_id = "test_public_id"

    user_instance = User(**user)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)

    image = await create(description, tags, image_url, public_id, user_instance, db)

    await add_tags_to_db(tags, image, db)

    result = await db.execute(select(TagsImages).filter_by(image_id=image.id))
    tags_images = result.fetchall()
    assert len(tags_images) == 6

    await db.delete(user_instance)
    await db.commit()


@pytest.mark.asyncio
async def test_get_images(session, user):
    """Test get_images function."""
    db = session
    limit = 5
    offset = 0

    user_instance = User(**user)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)

    for i in range(10):
        description = f"Image {i}"
        tags = f"#tag{i}"
        image_url = f"https://example.com/image{i}.jpg"
        public_id = f"public_id_{i}"
        await create(description, tags, image_url, public_id, user_instance, db)

    result = await get_images(limit, offset, user_instance, db)
    assert result is not None
    assert len(result) == limit

    await db.delete(user_instance)
    await db.commit()


@pytest.mark.asyncio
async def test_get_image_from_id(session, user):
    """Test get_image_from_id function."""
    db = session

    user_instance = User(**user)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)

    description = "Test Image 2"
    tags = "#tag1 #tag2"
    image_url = "https://example.com/test2.jpg"
    public_id = "test_public_id_2"

    image = await create(description, tags, image_url, public_id, user_instance, db)

    result = await get_image_from_id(image.id, user_instance, db)
    assert result is not None
    assert result.description == description

    await db.delete(user_instance)
    await db.commit()


@pytest.mark.asyncio
async def test_get_image_from_url(session, user):
    """Test get_image_from_url function."""
    db = session

    user_instance = User(**user)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)

    description = "Test Image 3"
    tags = "#tag1 #tag2"
    image_url = "https://example.com/test3.jpg"
    public_id = "test_public_id_3"

    image = await create(description, tags, image_url, public_id, user_instance, db)

    result = await get_image_from_url(image_url, user_instance, db)
    assert result is not None
    assert result[0].id == image.id

    await db.delete(user_instance)
    await db.commit()


@pytest.mark.asyncio
async def test_remove(session, user):
    """Test remove function."""
    db = session

    user_instance = User(**user)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)

    description = "Test Image 4"
    tags = "#tag1 #tag2"
    image_url = "https://example.com/test4.jpg"
    public_id = "test_public_id_4"

    image = await create(description, tags, image_url, public_id, user_instance, db)

    result = await remove(image.id, user_instance, db)
    assert result is not None
    assert result.id == image.id

    result = await db.execute(select(Image).filter_by(id=image.id))
    assert result.fetchone() is None

    await db.delete(user_instance)
    await db.commit()


@pytest.mark.asyncio
async def test_image_editor(session, user):
    """Test image_editor function."""
    db = session

    user_instance = User(**user)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)

    description = "Test Image 5"
    tags = "#tag1 #tag2"
    image_url = "https://example.com/test5.jpg"
    public_id = "test_public_id_5"

    image = await create(description, tags, image_url, public_id, user_instance, db)

    body = EditImageModel(circle={"use_filter": True, "height": 100, "width": 100},
                          effect={"use_filter": True, "art_audrey": True},
                          resize={"use_filter": True, "height": 200,
                                  "width": 200, "crop": True},
                          rotate={"use_filter": True, "width": 300, "degree": 90})
    result = await image_editor(image.id, body, user_instance, db)
    assert result is not None
    assert result.id == image.id
    assert result.image_url != image_url

    await db.delete(user_instance)
    await db.commit()


@pytest.mark.asyncio
async def test_edit_description(session, user):
    """Test edit_description function."""
    db = session

    user_instance = User(**user)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)

    description = "Test Image 6"
    tags = "#tag1 #tag2"
    image_url = "https://example.com/test6.jpg"
    public_id = "test_public_id_6"

    image = await create(description, tags, image_url, public_id, user_instance, db)

    new_description = "Updated Description"
    result = await edit_description(image.id, new_description, user_instance, db)
    assert result is not None
    assert result.id == image.id
    assert result.description == new_description

    await db.delete(user_instance)
    await db.commit()


@pytest.mark.asyncio
async def test_qr_code_generator(session, user):
    """Test qr_code_generator function."""
    db = session

    user_instance = User(**user)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)

    description = "Test Image 7"
    tags = "#tag1 #tag2"
    image_url = "https://example.com/test7.jpg"
    public_id = "test_public_id_7"

    image = await create(description, tags, image_url, public_id, user_instance, db)

    result = await qr_code_generator(image.id, user_instance, db)
    assert result is not None
    assert result.id == image.id
    assert result.qr_code_url is not None

    await db.delete(user_instance)
    await db.commit()
