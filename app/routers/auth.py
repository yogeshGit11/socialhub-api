from fastapi import APIRouter, Depends, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import user as user_schema
from app.schemas import auth as auth_schema
from app.schemas.response import ResponseModel
from app.db.session import get_db
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=ResponseModel[user_schema.UserOut])
async def signup_user(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    profile_image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
):
    payload = user_schema.UserCreate(
        email=email,
        username=username,
        password=password,
        profile_image=profile_image.filename if profile_image else None
    )

    new_user = await auth_service.signup_user(payload, db, profile_image)
    return ResponseModel(
        success=True,
        message="User registered successfully",
        data=new_user
    )

@router.post("/login", response_model=ResponseModel[auth_schema.Token])
async def login(payload: user_schema.UserLogin, db: AsyncSession = Depends(get_db)):
    tokens = await auth_service.login_user(payload, db)
    return ResponseModel(
        success=True,
        message="Login successful",
        data={
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"]
        }
    )

@router.post("/refresh", response_model=auth_schema.Token)
def refresh(payload: auth_schema.RefreshToken):
    return auth_service.refresh_token_service(payload.refresh_token)
