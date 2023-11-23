import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User, Image
from src.repository.pictures import get_images, remove, get_image_from_id, edit_description

@pytest.mark.asyncio
async def test_get_images(session: AsyncSession):
    user = User(username="testuser", email="test@example.com", password="password")
    session.add(user)
    await session.commit()

    image1 = Image(description="Image 1", tags="tag1", user=user)
    image2 = Image(description="Image 2", tags="tag2", user=user)
    session.add_all([image1, image2])
    await session.commit()

    images = await get_images(user_id=user.id, db=session)

    assert isinstance(images, list)
    assert len(images) == 2
    assert images[0].description == "Image 1"
    assert images[1].description == "Image 2"

@pytest.mark.asyncio
async def test_remove(session: AsyncSession):

    user = User(username="testuser", email="test@example.com", password="password")
    session.add(user)
    await session.commit()

    image = Image(description="Test Image", tags="tag1", user=user)
    session.add(image)
    await session.commit()

    await remove(image_id=image.id, db=session)

    deleted_image = await get_image_from_id(image_id=image.id, db=session)
    assert deleted_image is None

@pytest.mark.asyncio
async def test_get_image_from_id(session: AsyncSession):
    user = User(username="testuser", email="test@example.com", password="password")
    session.add(user)
    await session.commit()

    image = Image(description="Test Image", tags="tag1", user=user)
    session.add(image)
    await session.commit()


    retrieved_image = await get_image_from_id(image_id=image.id, db=session)

    assert retrieved_image is not None
    assert retrieved_image.id == image.id
    assert retrieved_image.description == image.description

@pytest.mark.asyncio
async def test_edit_description(session: AsyncSession):

    user = User(username="testuser", email="test@example.com", password="password")
    session.add(user)
    await session.commit()


    image = Image(description="Test Image", tags="tag1", user=user)
    session.add(image)
    await session.commit()

    new_description = "New Description"

    await edit_description(image_id=image.id, new_description=new_description, db=session)

    updated_image = await get_image_from_id(image_id=image.id, db=session)
    assert updated_image is not None
    assert updated_image.description == new_description
