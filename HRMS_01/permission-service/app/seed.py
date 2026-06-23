"""Seed default permissions and roles on startup."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Permission, Role

MODULES = ["Base", "Employee", "Attendance", "Leave", "Payroll", "Recruitment", "PMS", "Onboarding", "Offboarding", "Asset", "Project", "Helpdesk"]
ACTIONS = ["view", "add", "change", "delete"]
DEFAULT_ROLES = {
    "Admin": ACTIONS,
    "Manager": ["view", "add", "change"],
    "Employee": ["view"],
}

async def seed_permissions(db: AsyncSession):
    for module in MODULES:
        for action in ACTIONS:
            codename = f"{action}_{module.lower()}"
            existing = await db.execute(select(Permission).where(Permission.codename == codename))
            if not existing.scalar_one_or_none():
                db.add(Permission(module=module, action=action, codename=codename, name=f"Can {action} {module}"))
    await db.flush()
    for role_name, actions in DEFAULT_ROLES.items():
        existing = await db.execute(select(Role).where(Role.name == role_name))
        if not existing.scalar_one_or_none():
            role = Role(name=role_name, description=f"Default {role_name} role", is_system=True)
            perms = await db.execute(select(Permission))
            if role_name == "Admin":
                role.permissions = list(perms.scalars().all())
            else:
                role.permissions = [p for p in perms.scalars().all() if p.action in actions]
            db.add(role)
    await db.commit()
