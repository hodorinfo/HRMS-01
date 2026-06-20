from setuptools import find_packages, setup

setup(
    name="horilla-common",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.0",
        "sqlalchemy[asyncio]>=2.0.25",
        "pydantic>=2.5.0",
        "pydantic[email]",
        "email-validator>=2.0.0",
        "python-jose[cryptography]>=3.3.0",
        "httpx>=0.26.0",
        "celery[redis]>=5.3.0",
        "jinja2>=3.1.0",
        "asyncpg>=0.29.0",
    ],
)
