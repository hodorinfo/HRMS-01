from fastapi import APIRouter
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import CurrentUser, DbSession
from app.models import Permission, Role, UserRole
from app.schemas import (
    PermissionCheckRequest,
    PermissionCheckResponse,
    PermissionRead,
    RoleCreate,
    RoleRead,
    UserRoleAssign,
)
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)


@api_router.get("/permissions", response_model=list[PermissionRead])
async def list_permissions(db: DbSession, _user: CurrentUser):
    result = await db.execute(
        select(Permission)
        .where(Permission.is_active.is_(True))
        .order_by(Permission.module, Permission.action)
    )
    return result.scalars().all()


@api_router.post("/permissions/check", response_model=PermissionCheckResponse)
async def check_permission_endpoint(data: PermissionCheckRequest, db: DbSession, current_user: CurrentUser):
    user_id = data.user_id or current_user.user_id
    if current_user.is_superuser:
        return PermissionCheckResponse(allowed=True, codename=data.codename)
    result = await db.execute(
        select(Permission)
        .join(Role.permissions)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id, Permission.codename == data.codename)
    )
    perm = result.scalar_one_or_none()
    return PermissionCheckResponse(allowed=perm is not None, codename=data.codename)


@api_router.get("/roles", response_model=list[RoleRead])
async def list_roles(db: DbSession, _user: CurrentUser):
    result = await db.execute(select(Role).options(selectinload(Role.permissions)))
    return result.scalars().all()


@api_router.post("/roles", response_model=RoleRead, status_code=201)
async def create_role(data: RoleCreate, db: DbSession, _user: CurrentUser):
    role = Role(name=data.name, description=data.description)
    if data.permission_ids:
        perms = await db.execute(select(Permission).where(Permission.id.in_(data.permission_ids)))
        found_perms = list(perms.scalars().all())
        if len(found_perms) != len(data.permission_ids):
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more permission IDs are invalid"
            )
        role.permissions = found_perms
    db.add(role)
    await db.flush()
    await db.refresh(role, ["permissions"])
    return role


@api_router.post("/user-roles", status_code=201)
async def assign_roles(data: UserRoleAssign, db: DbSession, _user: CurrentUser):
    await db.execute(delete(UserRole).where(UserRole.user_id == data.user_id))
    for rid in data.role_ids:
        db.add(UserRole(user_id=data.user_id, role_id=rid))
    return {"message": "Roles assigned"}
