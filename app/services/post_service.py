import os
import shutil
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import post as post_model, like as like_model, user as user_model
from app.core.config import settings
from app.schemas import post as post_schema
from sqlalchemy.orm import selectinload

async def create_post_service(
    payload: post_schema.PostCreate,
    image: UploadFile,
    db: AsyncSession,
    current_user: user_model.User
):
    image_path = None

    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid image file type")

        file_ext = os.path.splitext(image.filename)[1]
        filename = f"{uuid4().hex}{file_ext}"
        full_path = os.path.join(settings.MEDIA_DIR, filename)

        folder_path = os.path.join(settings.MEDIA_DIR, "post_images")
        os.makedirs(folder_path, exist_ok=True)

        full_path = os.path.join(folder_path, filename)

        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_path = f"{settings.MEDIA_DIR}/{filename}".replace("./app/", "")

    new_post = post_model.Post(
        content=payload,
        author_id=current_user.id,
        image=image_path
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


async def get_posts_service(db: AsyncSession):
    result = await db.execute(select(post_model.Post).options(selectinload(post_model.Post.comments)))
    posts = result.scalars().all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No posts available.")
    return posts


async def like_post_service(
    post_id: int,
    db: AsyncSession,
    current_user: user_model.User
):
    post = await db.get(post_model.Post,post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    result = await db.execute(
        select(like_model.Like).where(
            like_model.Like.post_id == post_id,
            like_model.Like.user_id == current_user.id
        )
    )
    existing_like = result.scalars().first()

    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")

    new_like = like_model.Like(post_id=post_id, user_id=current_user.id)
    db.add(new_like)
    await db.commit()
    await db.refresh(new_like)

    return new_like
