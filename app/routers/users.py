from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.user_deps import get_current_user
from app.schemas import user as user_schema
from app.db.models import user as user_model
from app.services import user_service
from app.db.session import get_db
from app.schemas.response import ResponseModel
from app.schemas.user import PasswordChnage

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=ResponseModel[user_schema.UserOut])
async def get_me(current_user: user_model.User = Depends(get_current_user)):
    return ResponseModel(
        success=True,
        message="MY info retrieved successfully.",
        data=current_user
    )

@router.get("/{user_id}", response_model=ResponseModel[user_schema.UserOut])
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_by_id(db,user_id)
    return ResponseModel(
        success=True,
        message="User info retrieved successfully.",
        data=user
    )

@router.post("/{user_id}/follow", response_model=ResponseModel[None])
async def follow_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    username = await user_service.follow_user(db, user_id, current_user)
    return ResponseModel(
        success=True,
        message=f"You are now following {username}"
     )

@router.post("/{user_id}/unfollow", response_model=ResponseModel[None])
async def unfollow_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    username = await user_service.unfollow_user(db, user_id, current_user)
    return ResponseModel(
        success=True,
        message=f"You unfollowed {username}"
     )

@router.post("/changepassword",response_model=ResponseModel[None])
async def change_password(payload:PasswordChnage,db:AsyncSession=Depends(get_db),current_user:user_model.User=Depends(get_current_user)):
    await user_service.change_password(payload,db,current_user)
    return ResponseModel(
        success=True,
        message="Password changed successfully"
    )