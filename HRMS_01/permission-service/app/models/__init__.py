from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, Table, Column, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from horilla_common.base import Base, HorillaBaseMixin

role_permission = Table("permission_role_permissions", Base.metadata,
    Column("role_id", Integer, ForeignKey("permission_role.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission_permission.id", ondelete="CASCADE"), primary_key=True))

user_role = Table("permission_user_roles", Base.metadata,
    Column("user_id", Integer, primary_key=True),
    Column("role_id", Integer, ForeignKey("permission_role.id", ondelete="CASCADE"), primary_key=True))

class Permission(Base, HorillaBaseMixin):
    __tablename__ = "permission_permission"
    __table_args__ = (UniqueConstraint("module", "action", name="uq_module_action"),)
    module: Mapped[str] = mapped_column(String(50))
    action: Mapped[str] = mapped_column(String(20))
    codename: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

class Role(Base, HorillaBaseMixin):
    __tablename__ = "permission_role"
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    permissions: Mapped[list["Permission"]] = relationship("Permission", secondary=role_permission)

class UserRole(Base):
    __tablename__ = "permission_userrole"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("permission_role.id", ondelete="CASCADE"))
    role: Mapped["Role"] = relationship("Role")
