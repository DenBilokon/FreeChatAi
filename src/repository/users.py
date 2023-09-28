import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import User
from src.schemas.user_schemas import UserModel


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    sq = select(User).filter_by(email=email)
    result = await db.execute(sq)
    user = result.scalar_one_or_none()
    logging.info(user)
    return user


async def create_user(body: UserModel, db: AsyncSession) -> User:
    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def get_user_info(name: str, db: AsyncSession):
    sq = select(User).filter_by(name=name)
    result = await db.execute(sq)
    user = result.scalar_one_or_none()
    return user


async def update_user_info(body: UserModel, name: str, db: AsyncSession):
    sq = select(User).filter_by(name=name)
    result = await db.execute(sq)
    updated_user = result.scalar_one_or_none()
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated_user.name = body.name
    updated_user.email = body.email
    await db.commit()
    return updated_user


async def block(email: str, body: UserModel, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if user:
        user.banned = body.banned
    await db.commit()
    return user
