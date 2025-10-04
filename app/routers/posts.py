from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas import post as post_schema
from app.db.models import user as user_model
from app.db.session import get_db
from app.dependencies.user_deps import get_current_user
from app.services import post_service
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/create-post", response_model=ResponseModel[post_schema.PostOut])
async def create_post(
    content: str = Form(...),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    new_post = await post_service.create_post_service(content, image, db, current_user)
    return ResponseModel(
        success=True,
        message="Post added successfully",
        data=new_post
    )

@router.get("/", response_model=ResponseModel[List[post_schema.PostOut]])
async def get_posts(db: AsyncSession = Depends(get_db)):
    posts = await post_service.get_posts_service(db)
    return ResponseModel(
        success=True,
        message="Posts retrieved successfully.",
        data=posts
    )

@router.post("/{post_id}/like",response_model=ResponseModel[None])
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    await post_service.like_post_service(post_id, db, current_user)
    return ResponseModel(
        success=True,
        message="Post Liked"
    )
