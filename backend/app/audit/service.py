from datetime import UTC, datetime
from typing import Any, Protocol

from pymongo import MongoClient

from app.core.config import get_settings


class AuditWriter(Protocol):
    def write_event(self, event: dict[str, Any]) -> None:
        """Persist an audit event."""


class MongoAuditWriter:
    def __init__(self, mongo_url: str, database_name: str) -> None:
        self.client = MongoClient(mongo_url)
        self.collection = self.client[database_name]["audit_events"]

    def write_event(self, event: dict[str, Any]) -> None:
        self.collection.insert_one(event)


class AuditService:
    def __init__(self, writer: AuditWriter) -> None:
        self.writer = writer

    def record_ticket_created(self, *, ticket_id: str, user: str) -> None:
        self.writer.write_event(
            {
                "user": normalize_user(user),
                "action": "ticket_created",
                "ticket_id": ticket_id,
                "occurred_at": datetime.now(UTC),
            }
        )

    def record_ticket_status_updated(
        self,
        *,
        ticket_id: str,
        user: str,
        previous_status: str,
        new_status: str,
    ) -> None:
        self.writer.write_event(
            {
                "user": normalize_user(user),
                "action": "ticket_status_updated",
                "ticket_id": ticket_id,
                "previous_status": previous_status,
                "new_status": new_status,
                "occurred_at": datetime.now(UTC),
            }
        )


def normalize_user(user: str | None) -> str:
    if user is None or not user.strip():
        return "system"
    return user.strip()


def get_audit_service() -> AuditService:
    settings = get_settings()
    return AuditService(MongoAuditWriter(settings.mongo_url, settings.mongo_database))
