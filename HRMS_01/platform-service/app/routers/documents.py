import mimetypes
import os
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Document, DocumentRequest
from app.schemas import DocumentBulkUpdate, DocumentCreate, DocumentUpdate, DocumentRead
from horilla_common.jwt import TokenPayload
from horilla_common.schemas import PaginatedResponse

router = APIRouter(prefix="/documents", tags=["base"])

ALLOWED_EXTENSIONS = {
    "pdf": {".pdf"},
    "txt": {".txt"},
    "docx": {".docx"},
    "xlsx": {".xlsx"},
    "jpg": {".jpg", ".jpeg"},
    "png": {".png"},
    "jpeg": {".jpg", ".jpeg"},
}

settings = get_settings()
UPLOAD_BASE = getattr(settings, "upload_base", "/media/documents")
DEFAULT_MAX_FILE_SIZE_MB = getattr(settings, "max_file_size_mb", 150)


@router.get("", response_model=PaginatedResponse[DocumentRead])
async def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(200, ge=1, le=500),
    employee_id: Optional[int] = Query(None),
    document_request_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    _user: TokenPayload = Depends(get_current_user),
):
    base_query = select(Document).where(Document.is_active == True)

    if employee_id is not None:
        base_query = base_query.where(Document.employee_id == employee_id)
    if document_request_id is not None:
        base_query = base_query.where(
            Document.document_request_id == document_request_id
        )
    if status is not None:
        base_query = base_query.where(Document.status == status)
    if q:
        base_query = base_query.where(Document.title.ilike(f"%{q}%"))

    offset = (page - 1) * page_size
    total = await db.scalar(
        select(func.count()).select_from(Document)
    )
    result = await db.execute(base_query.offset(offset).limit(page_size))
    items = result.scalars().all()
    pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        items=[DocumentRead.model_validate(i) for i in items],
        total=total or 0,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.post("/bulk-update", response_model=PaginatedResponse[DocumentRead])
async def bulk_update_documents(
    data: DocumentBulkUpdate,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(
        select(Document).where(Document.id.in_(data.ids), Document.is_active == True)
    )
    items = result.scalars().all()

    if not items:
        raise HTTPException(status_code=404, detail="No documents found")

    updated = []
    for item in items:
        item.status = data.status
        if data.reject_reason is not None:
            item.reject_reason = data.reject_reason
        item.modified_by_id = user.user_id
        updated.append(item)

    await db.flush()
    for item in updated:
        await db.refresh(item)

    return PaginatedResponse(
        items=[DocumentRead.model_validate(i) for i in updated],
        total=len(updated),
        page=1,
        page_size=len(updated),
        pages=1,
    )


@router.get("/{item_id}", response_model=DocumentRead)
async def get_document(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(
        select(Document).where(Document.id == item_id, Document.is_active == True)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentRead.model_validate(item)


@router.post("", response_model=DocumentRead, status_code=201)
async def create_document(
    data: DocumentCreate,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
):
    item = Document(**data.model_dump(exclude_unset=True))
    if hasattr(item, "created_by_id"):
        item.created_by_id = user.user_id
    db.add(item)
    try:
        await db.flush()
        await db.refresh(item)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return DocumentRead.model_validate(item)


@router.put("/{item_id}", response_model=DocumentRead)
async def update_document(
    item_id: int,
    data: DocumentUpdate,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Document not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    if hasattr(item, "modified_by_id"):
        item.modified_by_id = user.user_id
    try:
        await db.flush()
        await db.refresh(item)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return DocumentRead.model_validate(item)


@router.delete("/{item_id}", status_code=204)
async def delete_document(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Document not found")
    item.is_active = False
    item.modified_by_id = user.user_id
    await db.flush()


@router.get("/{item_id}/download")
async def download_document(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(
        select(Document).where(Document.id == item_id, Document.is_active == True)
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.document:
        raise HTTPException(status_code=400, detail="No file attached to this document")

    if not user.is_superuser and not user.is_staff:
        if document.employee_id != user.employee_id:
            raise HTTPException(status_code=403, detail="Not authorized to download this document")

    file_path = os.path.join(UPLOAD_BASE, str(document.employee_id), os.path.basename(document.document))

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    media_type, _ = mimetypes.guess_type(file_path)
    filename = os.path.basename(file_path)
    return FileResponse(
        path=file_path,
        media_type=media_type or "application/octet-stream",
        filename=filename,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.put("/{document_id}/attach", response_model=DocumentRead)
async def attach_document_file(
    document_id: int,
    file: UploadFile = File(...),
    issue_date: Optional[str] = Form(None),
    expiry_date: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    max_allowed_mb = DEFAULT_MAX_FILE_SIZE_MB

    if document.document_request_id:
        req_result = await db.execute(
            select(DocumentRequest).where(
                DocumentRequest.id == document.document_request_id
            )
        )
        doc_request = req_result.scalar_one_or_none()
        if doc_request:
            if doc_request.format != "any":
                ext = os.path.splitext(file.filename or "")[1].lower()
                allowed = ALLOWED_EXTENSIONS.get(doc_request.format)
                if allowed and ext not in allowed:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File type '{ext}' is not allowed. Expected: {doc_request.format}",
                    )
            max_allowed_mb = min(max_allowed_mb, doc_request.max_size)

    max_allowed_bytes = max_allowed_mb * 1024 * 1024
    contents = await file.read()
    if len(contents) > max_allowed_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the maximum allowed size of {max_allowed_mb} MB",
        )

    employee_dir = os.path.join(UPLOAD_BASE, str(document.employee_id))
    os.makedirs(employee_dir, exist_ok=True)

    ext = os.path.splitext(file.filename or "file")[1]
    safe_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(employee_dir, safe_name)

    with open(file_path, "wb") as f:
        f.write(contents)

    document.document = f"media/documents/{document.employee_id}/{safe_name}"
    if issue_date:
        document.issue_date = issue_date
    if expiry_date:
        document.expiry_date = expiry_date
    if hasattr(document, "modified_by_id"):
        document.modified_by_id = user.user_id

    await db.flush()
    await db.refresh(document)

    return DocumentRead.model_validate(document)
