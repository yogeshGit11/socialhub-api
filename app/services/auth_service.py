from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import user as user_schema
from app.schemas import auth as auth_schema
from app.db.models import user as user_model
from app.core import security
from app.core.config import settings
from uuid import uuid4
import os
import shutil

async def signup_user(payload: user_schema.UserCreate, db: AsyncSession, profile_image: UploadFile = None):
    result = await db.execute(
        select(user_model.User).filter(user_model.User.email == payload.email)
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    image_path = None

    if profile_image:
        if not profile_image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid image file type")

        file_ext = os.path.splitext(profile_image.filename)[1]
        filename = f"{uuid4().hex}{file_ext}"
        folder_path = os.path.join(settings.MEDIA_DIR, "profile_images")
        os.makedirs(folder_path, exist_ok=True)

        full_path = os.path.join(folder_path, filename)

        os.makedirs(settings.MEDIA_DIR, exist_ok=True)

        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(profile_image.file, buffer)

        image_path = f"{settings.MEDIA_DIR}/{filename}".replace("./app/", "")

    new_user = user_model.User(
        username=payload.username,
        email=payload.email,
        password=security.hash_password(payload.password),
        date_of_birth=payload.date_of_birth,
        profile_image=image_path,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def login_user(payload: user_schema.UserLogin, db: AsyncSession):
    result = await db.execute(select(user_model.User).filter(user_model.User.email == payload.email))
    user = result.scalars().first()

    if not user or not security.verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Login failed. Incorrect email or password.")

    access_token = security.create_access_token(str(user.id))
    refresh_token = security.create_refresh_token(str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def refresh_token_service(refresh_token: auth_schema.RefreshToken):
    user = security.verify_refresh_token(refresh_token)

    access_token = security.create_access_token(str(user))
    refresh_token = security.create_refresh_token(str(user))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }