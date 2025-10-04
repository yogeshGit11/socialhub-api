from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.db.models import post as post_model, comment as comment_model, user as user_model
from app.schemas import comment as comment_schema

async def add_comment_service(
    post_id: int,
    payload: comment_schema.CommentCreate,
    db: AsyncSession,
    current_user: user_model.User
):
    result = await db.execute(
        select(post_model.Post).where(post_model.Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = comment_model.Comment(
        content=payload.content,
        post_id=post.id,
        author_id=current_user.id
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return new_comment
