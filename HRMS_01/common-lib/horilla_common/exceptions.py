import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

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

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc),
                "error_type": exc.__class__.__name__,
                "traceback": tb
            }
        )
