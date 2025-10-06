from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models.user import User
from app.db.models.follower import Follower
from app.core import security
from app.websocket.endpoints import manager


async def get_by_id(db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def follow_user(db: AsyncSession, user_id: int, current_user: User):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    target_user = await get_by_id(db, user_id)

    # checking if already following
    check = select(Follower).where(
        Follower.follower_id == current_user.id, Follower.user_id == target_user.id
    )
    result = await db.execute(check)
    existing_follow = result.scalar_one_or_none()

    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following")

    follow = Follower(follower_id=current_user.id, user_id=target_user.id)
    db.add(follow)
    await db.commit()

    # Send real-time notification to user being followed
    message = f"{current_user.username} started following you."
    await manager.send_to_user(target_user.id, message)

    return target_user.username


async def unfollow_user(db: AsyncSession, user_id: int, current_user: User):
    target_user = await get_by_id(db, user_id)

    result = select(Follower).where(
        Follower.follower_id == current_user.id, Follower.user_id == target_user.id
    )
    result = await db.execute(result)
    follow_relation = result.scalar_one_or_none()

    if not follow_relation:
        raise HTTPException(status_code=400, detail="Not following this user")

    await db.delete(follow_relation)
    await db.commit()

    return target_user.username


async def change_password(payload, db: AsyncSession, current_user: User):
    if payload.new_password != payload.confirm_new_password:
        raise HTTPException(
            status_code=400,
            detail="confirm_new_password is not matching with new_password",
        )

    result = await db.execute(select(User).where(User.id == current_user.id))
    user = result.scalars().first()

    if not security.verify_password(payload.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Your old_password is incorrect")

    user.hashed_password = security.hash_password(payload.new_password)
    db.add(user)
    await db.commit()
    return user
