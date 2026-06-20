from fastapi import APIRouter, Depends, HTTPException, status, Request
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from horilla_common.jwt import create_access_token, create_refresh_token, decode_token
from app.config import get_settings
from app.database import get_db
from app.dependencies import CurrentUser, DbSession
from app.models import Employee, User
from app.schemas import LoginRequest, TokenResponse, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False

@router.post("/login", response_model=TokenResponse)
async def login(request: Request, db: DbSession):
    content_type = request.headers.get("content-type", "")
    username = None
    password = None

    if "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        username = form_data.get("username")
        password = form_data.get("password")
    else:
        try:
            json_data = await request.json()
            username = json_data.get("username")
            password = json_data.get("password")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid request format")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    emp_result = await db.execute(select(Employee).where(Employee.employee_user_id == user.id))
    employee = emp_result.scalar_one_or_none()
    token_data = {
        "sub": user.username,
        "user_id": user.id,
        "employee_id": employee.id if employee else None,
        "is_superuser": user.is_superuser,
        "is_staff": user.is_staff,
    }
    return TokenResponse(
        access_token=create_access_token(token_data, settings.jwt_secret_key, settings.jwt_algorithm, settings.jwt_access_token_expire_minutes),
        refresh_token=create_refresh_token(token_data, settings.jwt_secret_key, settings.jwt_algorithm, settings.jwt_refresh_token_expire_days),
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token, settings.jwt_secret_key, settings.jwt_algorithm)
        if payload.type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        token_data = payload.model_dump(exclude={"exp", "type"})
        return TokenResponse(
            access_token=create_access_token(token_data, settings.jwt_secret_key, settings.jwt_algorithm, settings.jwt_access_token_expire_minutes),
            refresh_token=create_refresh_token(token_data, settings.jwt_secret_key, settings.jwt_algorithm, settings.jwt_refresh_token_expire_days),
        )
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from exc

@router.get("/me", response_model=UserRead)
async def me(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(User).where(User.id == current_user.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)

@router.post("/register", response_model=UserRead, status_code=201)
async def register(data: UserCreate, db: DbSession):
    existing = await db.execute(select(User).where((User.username == data.username) | (User.email == data.email)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        is_staff=data.is_staff,
        is_superuser=data.is_superuser,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return UserRead.model_validate(user)
