from fastapi import APIRouter, Depends, HTTPException, status, Request
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from horilla_common.jwt import create_access_token, create_refresh_token, decode_token
from app.config import get_settings
from app.database import get_db
from app.dependencies import CurrentUser, DbSession
from app.models import Employee, User
from app.schemas import (
    LoginRequest, TokenResponse, UserCreate, UserRead, UserUpdate,
    ChangePasswordRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from app.tasks import send_password_reset_email_task

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=TokenResponse)
async def login(db: DbSession, form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    from datetime import datetime, timezone
    user.last_login = datetime.now(timezone.utc)
    await db.flush()
    
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

@router.put("/me", response_model=UserRead)
async def update_me(data: UserUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(User).where(User.id == current_user.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    await db.flush()
    await db.refresh(user)
    return UserRead.model_validate(user)

@router.post("/change-password")
async def change_password(data: ChangePasswordRequest, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(User).where(User.id == current_user.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
        
    user.password_hash = hash_password(data.new_password)
    await db.flush()
    return {"message": "Password changed successfully"}

@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, db: DbSession):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user:
        # Prevent user enumeration by always returning success
        return {"message": "If that email is registered, a password reset link has been sent"}
        
    # Generate token
    token_data = {"sub": user.email, "type": "reset_password"}
    # Token valid for 1 hour
    token = create_access_token(token_data, settings.jwt_secret_key, settings.jwt_algorithm, 60)
    
    # Trigger celery task
    send_password_reset_email_task.delay(user.email, token)
    
    return {"message": "If that email is registered, a password reset link has been sent"}

@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest, db: DbSession):
    try:
        payload = decode_token(data.token, settings.jwt_secret_key, settings.jwt_algorithm)
        if payload.type != "reset_password":
            raise HTTPException(status_code=400, detail="Invalid token type")
        email = payload.sub
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
        
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.password_hash = hash_password(data.new_password)
    await db.flush()
    return {"message": "Password reset successfully"}
