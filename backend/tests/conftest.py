from collections.abc import Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.audit.service import AuditService
from app.controllers.tickets import get_audit_service
from app.db.base import Base
from app.db.session import get_session
from app.main import app
from app.models import Client, Ticket  # noqa: F401


class SpyAuditWriter:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def write_event(self, event: dict[str, Any]) -> None:
        self.events.append(event)


@pytest.fixture()
def audit_writer() -> SpyAuditWriter:
    return SpyAuditWriter()


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def api_client(
    db_session: Session,
    audit_writer: SpyAuditWriter,
) -> Generator[TestClient, None, None]:
    def override_session() -> Generator[Session, None, None]:
        yield db_session

    def override_audit_service() -> AuditService:
        return AuditService(audit_writer)

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_audit_service] = override_audit_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
