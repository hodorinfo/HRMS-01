"""FastAPI dependencies for auth and permissions."""

from typing import Annotated, Callable, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from horilla_common.jwt import TokenPayload, decode_token
from horilla_common.permissions import check_permission, require_write_permission


def create_auth_dependency(secret_key: str, algorithm: str = "HS256"):
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/api/v1/auth/login")

    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenPayload:
        try:
            payload = decode_token(token, secret_key, algorithm)
            if payload.type != "access":
                raise HTTPException(status_code=401, detail="Invalid token type")
            return payload
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

    return get_current_user, oauth2_scheme


def create_permission_dependency(
    permission_service_url: str,
    module: str,
    action: str,
    get_current_user: Callable,
):
    async def require_permission(
        request: Request,
        current_user: Annotated[TokenPayload, Depends(get_current_user)],
    ) -> TokenPayload:
        if current_user.is_superuser:
            return current_user
        if not require_write_permission(request.method):
            return current_user
        allowed = await check_permission(
            permission_service_url,
            request.headers.get("Authorization", "").replace("Bearer ", ""),
            module,
            action,
            user_id=current_user.user_id,
        )
        if not allowed:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user

    return require_permission
