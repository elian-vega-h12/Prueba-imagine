from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from app.audit.service import AuditService, get_audit_service, normalize_user
from app.db.session import get_session
from app.repositories.clients import ClientRepository
from app.repositories.tickets import TicketRepository
from app.schemas.tickets import TicketCreate, TicketRead, TicketStatusUpdate
from app.services.tickets import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_ticket_service(
    session: Annotated[Session, Depends(get_session)],
    audit_service: Annotated[AuditService, Depends(get_audit_service)],
) -> TicketService:
    return TicketService(
        ticket_repository=TicketRepository(session),
        client_repository=ClientRepository(session),
        audit_service=audit_service,
    )


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(
    payload: TicketCreate,
    service: Annotated[TicketService, Depends(get_ticket_service)],
    x_user: Annotated[str | None, Header(alias="X-User")] = None,
):
    return service.create_ticket(payload, normalize_user(x_user))


@router.get("", response_model=list[TicketRead])
def list_tickets(service: Annotated[TicketService, Depends(get_ticket_service)]):
    return service.list_tickets()


@router.patch("/{ticket_id}/status", response_model=TicketRead)
def update_ticket_status(
    ticket_id: UUID,
    payload: TicketStatusUpdate,
    service: Annotated[TicketService, Depends(get_ticket_service)],
    x_user: Annotated[str | None, Header(alias="X-User")] = None,
):
    return service.update_ticket_status(str(ticket_id), payload.status, normalize_user(x_user))
