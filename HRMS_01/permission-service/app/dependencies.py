"""Service dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from horilla_common.dependencies import create_auth_dependency
from horilla_common.jwt import TokenPayload

from app.config import get_settings
from app.database import get_db

settings = get_settings()
get_current_user, oauth2_scheme = create_auth_dependency(
    settings.jwt_secret_key, settings.jwt_algorithm
)

DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]


def require_permission(codename: str):
    async def _perm_check(
        current_user: Annotated[TokenPayload, Depends(get_current_user)],
    ) -> TokenPayload:
        if current_user.is_superuser:
            return current_user
        if codename not in current_user.permissions:
            raise HTTPException(status_code=403, detail=f"Permission denied: {codename}")
        return current_user
    return _perm_check
