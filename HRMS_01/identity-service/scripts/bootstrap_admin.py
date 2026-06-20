#!/usr/bin/env python3
"""Bootstrap admin user in identity service."""

import asyncio
import sys

import bcrypt
from sqlalchemy import select


async def create_admin(username: str = "admin", password: str = "admin", email: str = "admin@horilla.com"):
    from app.database import async_session, init_db
    from app.models import User

    await init_db()
    async with async_session() as db:
        existing = await db.execute(select(User).where(User.username == username))
        if existing.scalar_one_or_none():
            print(f"User '{username}' already exists")
            return
        user = User(
            username=username,
            email=email,
            password_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
            first_name="Admin",
            is_staff=True,
            is_superuser=True,
        )
        db.add(user)
        await db.commit()
        print(f"Created admin user: {username}")


if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else "admin"
    asyncio.run(create_admin(username, password))