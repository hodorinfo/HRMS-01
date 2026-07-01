from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from horilla_common.base import Base, HorillaBaseMixin

class MailAutomation(Base, HorillaBaseMixin):
    __tablename__ = "horilla_automations_mailautomation"
    title: Mapped[str] = mapped_column(String(100), unique=True)
    method_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model: Mapped[str] = mapped_column(String(100))
    mail_to: Mapped[str] = mapped_column(Text)
    mail_details: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    trigger: Mapped[str] = mapped_column(String(20))
    mail_template_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    delivery_channel: Mapped[str] = mapped_column(String(20), default="email")
    condition: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class Notification(Base):
    __tablename__ = "notifications_notification"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recipient_id: Mapped[int] = mapped_column(Integer)
    unread: Mapped[bool] = mapped_column(Boolean, default=True)
    actor_content_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    actor_object_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    verb: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    public: Mapped[bool] = mapped_column(Boolean, default=True)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    level: Mapped[str] = mapped_column(String(20), default="info")

class AuditTag(Base, HorillaBaseMixin):
    __tablename__ = "horilla_audit_audittag"
    title: Mapped[str] = mapped_column(String(20))
    highlight: Mapped[bool] = mapped_column(Boolean, default=False)

class HistoryTrackingFields(Base, HorillaBaseMixin):
    __tablename__ = "horilla_audit_historytrackingfields"
    tracking_fields: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    work_info_track: Mapped[bool] = mapped_column(Boolean, default=False)

class DocumentRequestAssignment(Base, HorillaBaseMixin):
    __tablename__ = "horilla_documents_documentrequestassignment"
    document_request_id: Mapped[int] = mapped_column(Integer, ForeignKey("horilla_documents_documentrequest.id", ondelete="CASCADE"))
    employee_id: Mapped[int] = mapped_column(Integer)

class DocumentRequest(Base, HorillaBaseMixin):
    __tablename__ = "horilla_documents_documentrequest"
    title: Mapped[str] = mapped_column(String(100))
    format: Mapped[str] = mapped_column(String(20), default="any")
    max_size: Mapped[int] = mapped_column(Integer, default=150)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    assignments: Mapped[list[DocumentRequestAssignment]] = relationship(
        "DocumentRequestAssignment", backref="document_request",
        cascade="all, delete-orphan",
        foreign_keys=[DocumentRequestAssignment.document_request_id],
    )

class Document(Base, HorillaBaseMixin):
    __tablename__ = "horilla_documents_document"
    title: Mapped[str] = mapped_column(String(100))
    employee_id: Mapped[int] = mapped_column(Integer)
    document_request_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("horilla_documents_documentrequest.id", ondelete="SET NULL"), nullable=True)
    document: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="requested")
    reject_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    issue_date: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    expiry_date: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    notify_before: Mapped[int] = mapped_column(Integer, default=1)
    is_digital_asset: Mapped[bool] = mapped_column(Boolean, default=False)
