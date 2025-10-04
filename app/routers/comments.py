from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import comment as comment_schema
from app.db.models import user as user_model
from app.db.session import get_db
from app.dependencies.user_deps import get_current_user
from app.services import comment_service
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/{post_id}", response_model=ResponseModel[comment_schema.CommentOut])
async def add_comment(
    post_id: int,
    payload: comment_schema.CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    await comment_service.add_comment_service(post_id, payload, db, current_user)
    return ResponseModel(
        success=True,
        message="Comment added successfully.",
    )
