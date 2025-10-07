import os
import shutil
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import post as post_model, like as like_model, user as user_model, follower as follower_model
from app.core.config import settings
from app.schemas import post as post_schema
from sqlalchemy.orm import selectinload
from app.websocket.endpoints import manager
from app.email.tasks import notify_followers_new_post

async def create_post_service(
    background_tasks: BackgroundTasks,
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

    #get all followers of the current user
    result = await db.execute(
        select(follower_model.Follower).where(
            follower_model.Follower.user_id == current_user.id
        )
    )
    followers = result.scalars().all()
    follower_ids = [f.follower_id for f in followers]

    #real-time notification to followers
    message = f"{current_user.username} has created a new post."
    for follower_id in follower_ids:
        print(f"Follower ID: {follower_id}")
        await manager.send_to_user(follower_id, message)

    if follower_ids:
        result = await db.execute(
            select(user_model.User).where(user_model.User.id.in_(follower_ids))
        )
        follower_users = result.scalars().all()
        follower_emails = [user.email for user in follower_users if user.email]
    else:
        follower_emails = []

    if follower_emails:
        background_tasks.add_task(
            notify_followers_new_post,
            background_tasks,
            follower_emails,
            new_post.content,
            current_user.username
        )

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

    # Send real-time notification to post author
    if post.author_id != current_user.id:
        message = f"{current_user.username} liked your post."
        await manager.send_to_user(post.author_id, message)

    return new_like
