"""JWT token creation and validation."""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    user_id: int
    employee_id: Optional[int] = None
    is_superuser: bool = False
    is_staff: bool = False
    exp: Optional[int] = None
    type: str = "access"


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def create_access_token(
    data: dict[str, Any],
    secret_key: str,
    algorithm: str = "HS256",
    expires_minutes: int = 30,
) -> str:
    to_encode = data.copy()
    if "is_superuser" not in to_encode:
        to_encode["is_superuser"] = False
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def create_refresh_token(
    data: dict[str, Any],
    secret_key: str,
    algorithm: str = "HS256",
    expires_days: int = 7,
) -> str:
    to_encode = data.copy()
    if "is_superuser" not in to_encode:
        to_encode["is_superuser"] = False
    expire = datetime.now(timezone.utc) + timedelta(days=expires_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_token(token: str, secret_key: str, algorithm: str = "HS256") -> TokenPayload:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return TokenPayload(**payload)
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
