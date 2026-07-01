from typing import Optional
from pydantic import BaseModel, ConfigDict

class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    module: str
    action: str
    codename: str
    name: str
    description: Optional[str] = None
    is_active: bool = True

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permission_ids: list[int] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[list[int]] = None

class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str] = None
    is_system: bool = False
    is_active: bool = True
    permissions: list[PermissionRead] = []

class UserRoleAssign(BaseModel):
    user_id: int
    role_ids: list[int]

class RoleIdsBody(BaseModel):
    role_ids: list[int]

class PermissionCheckRequest(BaseModel):
    codename: str
    user_id: Optional[int] = None

class PermissionCheckResponse(BaseModel):
    allowed: bool
    codename: str
