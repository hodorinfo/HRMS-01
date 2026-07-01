"""Service dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from horilla_common.dependencies import create_auth_dependency
from horilla_common.jwt import TokenPayload

from app.config import get_settings
from app.database import get_db
from app.models import User

settings = get_settings()
get_current_user, oauth2_scheme = create_auth_dependency(
    settings.jwt_secret_key, settings.jwt_algorithm
)

DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]


async def verify_token_version(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenPayload:
    result = await db.execute(select(User.token_version).where(User.id == current_user.user_id))
    row = result.scalar_one_or_none()
    if row is None or row != current_user.token_version:
        raise HTTPException(status_code=401, detail="Token has been revoked")
    return current_user


def require_permission(codename: str):
    async def _perm_check(
        current_user: Annotated[TokenPayload, Depends(verify_token_version)],
    ) -> TokenPayload:
        if current_user.is_superuser:
            return current_user
        if codename not in current_user.permissions:
            raise HTTPException(status_code=403, detail=f"Permission denied: {codename}")
        return current_user
    return _perm_check
