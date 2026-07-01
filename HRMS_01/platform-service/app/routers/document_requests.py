from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import get_current_user
from app.models import DocumentRequest, DocumentRequestAssignment, Document
from app.schemas import (
    DocumentRequestCreate, DocumentRequestUpdate, DocumentRequestRead,
    DocumentRead,
)
from horilla_common.jwt import TokenPayload
from horilla_common.schemas import PaginatedResponse

router = APIRouter(prefix="/document-requests", tags=["base"])


@router.get("", response_model=PaginatedResponse[DocumentRequestRead])
async def list_document_requests(
    page: int = Query(1, ge=1),
    page_size: int = Query(200, ge=1, le=500),
    employee_id: Optional[int] = Query(None),
    q: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    _user: TokenPayload = Depends(get_current_user),
):
    base_query = select(DocumentRequest).options(
        selectinload(DocumentRequest.assignments)
    ).where(DocumentRequest.is_active == True)

    if employee_id is not None:
        assignment_subq = (
            select(DocumentRequestAssignment.document_request_id)
            .where(DocumentRequestAssignment.employee_id == employee_id)
            .subquery()
        )
        doc_subq = (
            select(Document.document_request_id)
            .where(
                Document.employee_id == employee_id,
                Document.document_request_id.isnot(None),
            )
            .subquery()
        )
        base_query = base_query.where(
            DocumentRequest.id.in_(select(assignment_subq))
            | DocumentRequest.id.in_(select(doc_subq))
        )

    if q:
        like = f"%{q}%"
        base_query = base_query.where(
            DocumentRequest.title.ilike(like) | DocumentRequest.description.ilike(like)
        )

    offset = (page - 1) * page_size
    total = await db.scalar(
        select(func.count()).select_from(DocumentRequest)
    )
    result = await db.execute(
        base_query.offset(offset).limit(page_size)
    )
    items = result.scalars().all()
    pages = (total + page_size - 1) // page_size if total else 0

    req_ids_missing = [item.id for item in items if not item.assignments]
    doc_emp_map: dict[int, set[int]] = {}
    if req_ids_missing:
        doc_rows = await db.execute(
            select(Document.document_request_id, Document.employee_id)
            .where(
                Document.document_request_id.in_(req_ids_missing),
                Document.employee_id.isnot(None),
            )
        )
        for row in doc_rows.all():
            doc_emp_map.setdefault(row.document_request_id, set()).add(row.employee_id)

    read_items = []
    for item in items:
        data = DocumentRequestRead.model_validate(item)
        if item.assignments:
            data.employee_ids = [a.employee_id for a in item.assignments]
        elif item.id in doc_emp_map:
            data.employee_ids = list(doc_emp_map[item.id])
        read_items.append(data)

    return PaginatedResponse(
        items=read_items,
        total=total or 0,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/{item_id}", response_model=DocumentRequestRead)
async def get_document_request(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(
        select(DocumentRequest)
        .options(selectinload(DocumentRequest.assignments))
        .where(DocumentRequest.id == item_id, DocumentRequest.is_active == True)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Document request not found")
    data = DocumentRequestRead.model_validate(item)
    if item.assignments:
        data.employee_ids = [a.employee_id for a in item.assignments]
    else:
        doc_rows = await db.execute(
            select(Document.employee_id)
            .where(
                Document.document_request_id == item.id,
                Document.employee_id.isnot(None),
            )
        )
        data.employee_ids = list({row[0] for row in doc_rows.all() if row[0]})
    return data


async def _sync_assignments_and_docs(
    item: DocumentRequest,
    employee_ids: list[int],
    user_id: int,
    db: AsyncSession,
):
    existing_ids = {a.employee_id for a in item.assignments}
    new_ids = set(employee_ids)

    for emp_id in new_ids - existing_ids:
        assignment = DocumentRequestAssignment(
            document_request_id=item.id,
            employee_id=emp_id,
            created_by_id=user_id,
        )
        db.add(assignment)
        doc = Document(
            title=f"Upload {item.title}",
            employee_id=emp_id,
            document_request_id=item.id,
            status="requested",
            created_by_id=user_id,
        )
        db.add(doc)

    for emp_id in existing_ids - new_ids:
        await db.execute(
            delete(DocumentRequestAssignment).where(
                DocumentRequestAssignment.document_request_id == item.id,
                DocumentRequestAssignment.employee_id == emp_id,
            )
        )

    await db.flush()
    await db.refresh(item, attribute_names=["assignments"])


@router.post("", response_model=DocumentRequestRead, status_code=201)
async def create_document_request(
    data: DocumentRequestCreate,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
):
    item = DocumentRequest(
        title=data.title,
        format=data.format,
        max_size=data.max_size,
        description=data.description,
        created_by_id=user.user_id,
    )
    db.add(item)
    await db.flush()

    await db.refresh(item, attribute_names=["assignments"])
    await _sync_assignments_and_docs(item, data.employee_ids, user.user_id, db)

    read_data = DocumentRequestRead.model_validate(item)
    read_data.employee_ids = [a.employee_id for a in item.assignments]
    return read_data


@router.put("/{item_id}", response_model=DocumentRequestRead)
async def update_document_request(
    item_id: int,
    data: DocumentRequestUpdate,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(
        select(DocumentRequest)
        .options(selectinload(DocumentRequest.assignments))
        .where(DocumentRequest.id == item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Document request not found")

    update_data = data.model_dump(exclude_unset=True)
    employee_ids = update_data.pop("employee_ids", None)

    for key, value in update_data.items():
        setattr(item, key, value)
    item.modified_by_id = user.user_id

    if employee_ids is not None:
        await _sync_assignments_and_docs(item, employee_ids, user.user_id, db)

    await db.flush()
    await db.refresh(item, attribute_names=["assignments"])
    read_data = DocumentRequestRead.model_validate(item)
    read_data.employee_ids = [a.employee_id for a in item.assignments]
    return read_data


@router.delete("/{item_id}", status_code=204)
async def delete_document_request(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(
        select(DocumentRequest).where(DocumentRequest.id == item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Document request not found")
    item.is_active = False
    item.modified_by_id = user.user_id
    await db.flush()


@router.get("/{item_id}/documents", response_model=PaginatedResponse[DocumentRead])
async def list_documents_for_request(
    item_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    _user: TokenPayload = Depends(get_current_user),
):
    result = await db.execute(
        select(DocumentRequest).where(DocumentRequest.id == item_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Document request not found")

    base_query = select(Document).where(
        Document.document_request_id == item_id, Document.is_active == True
    )
    offset = (page - 1) * page_size
    total = await db.scalar(
        select(func.count())
        .select_from(Document)
        .where(
            Document.document_request_id == item_id,
            Document.is_active == True,
        )
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
