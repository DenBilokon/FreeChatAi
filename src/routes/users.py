from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.db import get_db
from src.database.models import User, Role
from src.repository.users import block, update_user_info, get_user_info

from src.schemas.user_schemas import UserResponse, UserModel
from src.services.auth import auth_service
from src.services.roles import RolesAccess

access_get = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_create = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_delete = RolesAccess([Role.superadmin, Role.admin])
access_block = RolesAccess([Role.superadmin, Role.admin])

router = APIRouter(prefix="/users", tags=["Users profile"])


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):

    return current_user


@router.get("/{username}/", response_model=UserResponse)
async def profile_info(username: str, db: AsyncSession = Depends(get_db)):

    user_info = await get_user_info(username, db)
    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info


@router.put('/{username}', response_model=UserResponse, dependencies=[Depends(access_update)])
async def profile_update(username: str, body: UserModel, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):

    if current_user.username != username and current_user.role in ('client', 'master'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own profile")

    updated_user = await update_user_info(body, username, db)

    return updated_user


@router.patch("/{email}/blacklist", response_model=UserResponse, dependencies=[Depends(access_block)])
async def block_user(email: str, body: UserModel, db: AsyncSession = Depends(get_db),
                        _: User = Depends(auth_service.get_current_user)):
    blocked_user = await block(email, body, db)
    if blocked_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return blocked_user
