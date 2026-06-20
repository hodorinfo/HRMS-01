"""RBAC permission checking via permission service."""

from typing import Optional

import httpx


async def check_permission(
    permission_service_url: str,
    token: str,
    module: str,
    action: str,
    user_id: Optional[int] = None,
) -> bool:
    """Check if user has permission for module.action via permission service."""
    codename = f"{action}_{module.lower()}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{permission_service_url.rstrip('/')}/api/v1/permissions/check",
            json={"codename": codename, "user_id": user_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code == 200:
            return response.json().get("allowed", False)
        return False


def require_write_permission(method: str) -> bool:
    """Sensitive HTTP methods require permission check."""
    return method.upper() in {"POST", "PUT", "PATCH", "DELETE"}
