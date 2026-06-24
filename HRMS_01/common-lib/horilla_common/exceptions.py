import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, DBAPIError

def add_global_exception_handlers(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        err_msg = str(exc.orig) if exc.orig else str(exc)
        err_msg_lower = err_msg.lower()
        
        # 1. Check specific known database constraints
        if "uq_employee_date" in err_msg:
            return JSONResponse(
                status_code=400,
                content={"detail": "Attendance has already been marked for this employee on this date."}
            )
            
        # 2. General duplicate key / unique constraint clashing
        if "unique constraint" in err_msg_lower or "duplicate key" in err_msg_lower:
            if "_pkey" in err_msg_lower:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "A record with this ID already exists."}
                )
            return JSONResponse(
                status_code=400,
                content={"detail": "This record already exists (duplicate entry)."}
            )
            
        # 3. Foreign key violation (invalid relations)
        if "foreign key constraint" in err_msg_lower:
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid reference: The referenced related record does not exist."}
            )
            
        # Default fallback for other IntegrityErrors (clean message)
        return JSONResponse(
            status_code=400,
            content={"detail": f"Database integrity violation: {err_msg}"}
        )

    @app.exception_handler(DBAPIError)
    async def dbapi_exception_handler(request: Request, exc: DBAPIError):
        # Handle DataErrors, ProgrammingErrors etc (like value too long)
        err_msg = str(exc.orig) if exc.orig else str(exc)
        clean_msg = err_msg.split('\n')[0] # Get only the first line of the DB error
        return JSONResponse(
            status_code=400,
            content={"detail": clean_msg}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # Send a clean error to the frontend, log traceback internally if needed
        clean_msg = str(exc).split('\n')[0]
        return JSONResponse(
            status_code=500,
            content={
                "detail": clean_msg,
                "error_type": exc.__class__.__name__
            }
        )
