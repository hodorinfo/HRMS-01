from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.database import get_db
from app.dependencies import CurrentUser, DbSession, require_permission
from app.models import Permission, Role, UserRole
from app.schemas import (
    PermissionCheckRequest,
    PermissionCheckResponse,
    PermissionRead,
    RoleCreate,
    RoleRead,
    RoleIdsBody,
    RoleUpdate,
    UserRoleAssign,
)
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)


@api_router.get("/permissions", response_model=list[PermissionRead])
async def list_permissions(
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("permission.view_user_permissions")),
):
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
async def list_roles(
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("permission.view_user_permissions")),
):
    result = await db.execute(select(Role).options(selectinload(Role.permissions)))
    return result.scalars().all()


@api_router.post("/roles", response_model=RoleRead, status_code=201)
async def create_role(
    data: RoleCreate,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("permission.add_group")),
):
    role = Role(name=data.name, description=data.description)
    if data.permission_ids:
        perms = await db.execute(select(Permission).where(Permission.id.in_(data.permission_ids)))
        found_perms = list(perms.scalars().all())
        if len(found_perms) != len(data.permission_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more permission IDs are invalid"
            )
        role.permissions = found_perms
    db.add(role)
    await db.flush()
    await db.refresh(role, ["permissions"])
    return role


@api_router.post("/user-roles", status_code=201)
async def assign_roles(
    data: UserRoleAssign,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("permission.assign_role")),
):
    await db.execute(delete(UserRole).where(UserRole.user_id == data.user_id))
    for rid in data.role_ids:
        db.add(UserRole(user_id=data.user_id, role_id=rid))
    return {"message": "Roles assigned"}


@api_router.get("/users/{user_id}/permissions", response_model=list[str])
async def get_user_permissions(
    user_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    if user_id != current_user.user_id and not current_user.is_superuser:
        if "permission.view_user_permissions" not in current_user.permissions:
            raise HTTPException(status_code=403, detail="Permission denied: permission.view_user_permissions")
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions))
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
    )
    seen = set()
    for role in result.scalars().all():
        for perm in role.permissions:
            seen.add(perm.codename)
    return sorted(seen)


@api_router.get("/roles/{role_id}", response_model=RoleRead)
async def get_role(
    role_id: int,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("permission.view_user_permissions")),
):
    result = await db.execute(
        select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@api_router.put("/roles/{role_id}", response_model=RoleRead)
async def update_role(
    role_id: int,
    data: RoleUpdate,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("permission.add_group")),
):
    result = await db.execute(
        select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if data.name is not None:
        role.name = data.name
    if data.description is not None:
        role.description = data.description
    if data.permission_ids is not None:
        perms = await db.execute(select(Permission).where(Permission.id.in_(data.permission_ids)))
        found_perms = list(perms.scalars().all())
        if len(found_perms) != len(data.permission_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more permission IDs are invalid"
            )
        role.permissions = found_perms
    await db.flush()
    await db.refresh(role, ["permissions"])
    return role


@api_router.delete("/roles/{role_id}", status_code=204)
async def delete_role(
    role_id: int,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("permission.add_group")),
):
    result = await db.execute(
        select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if role.is_system:
        raise HTTPException(status_code=400, detail="Cannot delete a system role")
    assigned = await db.execute(select(UserRole).where(UserRole.role_id == role_id))
    if assigned.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Role is assigned to one or more users. Remove assignments before deleting."
        )
    await db.delete(role)
    await db.flush()
    return None


@api_router.get("/users/{user_id}/roles", response_model=list[RoleRead])
async def get_user_roles(
    user_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    if user_id != current_user.user_id and not current_user.is_superuser:
        if "permission.view_user_permissions" not in current_user.permissions:
            raise HTTPException(status_code=403, detail="Permission denied: permission.view_user_permissions")
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions))
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
    )
    return result.scalars().all()


@api_router.put("/users/{user_id}/roles", response_model=list[RoleRead])
async def set_user_roles(
    user_id: int,
    data: RoleIdsBody,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("permission.assign_role")),
):
    roles = await db.execute(select(Role).where(Role.id.in_(data.role_ids)))
    found_roles = list(roles.scalars().all())
    if len(found_roles) != len(data.role_ids):
        raise HTTPException(status_code=400, detail="One or more role IDs are invalid")
    await db.execute(delete(UserRole).where(UserRole.user_id == user_id))
    for rid in data.role_ids:
        db.add(UserRole(user_id=user_id, role_id=rid))
    await db.flush()
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions))
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
    )
    return result.scalars().all()


@api_router.get("/internal/users/{user_id}/permissions", response_model=list[str])
async def get_user_permissions_internal(
    user_id: int,
    request: Request,
    db: DbSession,
):
    token = request.headers.get("X-Service-Token")
    settings = get_settings()
    if not token or token != settings.internal_service_token:
        raise HTTPException(status_code=403, detail="Invalid or missing service token")
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions))
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
    )
    seen = set()
    for role in result.scalars().all():
        for perm in role.permissions:
            seen.add(perm.codename)
    return sorted(seen)
