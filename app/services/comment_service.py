from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.db.models import post as post_model, comment as comment_model, user as user_model
from app.schemas import comment as comment_schema
from app.websocket.endpoints import manager

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

    # Send real-time notification to post author
    if post.author_id != current_user.id:
        message = f"{current_user.username} commented on your post: {payload.content}"
        await manager.send_to_user(post.author_id, message)

    return new_comment
