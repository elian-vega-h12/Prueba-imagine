from fastapi import HTTPException, status

from app.audit.service import AuditService
from app.models.ticket import Ticket
from app.repositories.clients import ClientRepository
from app.repositories.tickets import TicketRepository
from app.schemas.tickets import TicketCreate, TicketStatus


class TicketService:
    def __init__(
        self,
        ticket_repository: TicketRepository,
        client_repository: ClientRepository,
        audit_service: AuditService,
    ) -> None:
        self.ticket_repository = ticket_repository
        self.client_repository = client_repository
        self.audit_service = audit_service

    def create_ticket(self, payload: TicketCreate, user: str) -> Ticket:
        if self.client_repository.get(str(payload.client_id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found",
            )

        ticket = self.ticket_repository.create(payload)
        self.audit_service.record_ticket_created(ticket_id=ticket.id, user=user)
        return ticket

    def list_tickets(self) -> list[Ticket]:
        return self.ticket_repository.list_all()

    def update_ticket_status(self, ticket_id: str, new_status: TicketStatus, user: str) -> Ticket:
        ticket = self.ticket_repository.get(ticket_id)
        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found",
            )

        previous_status = ticket.status
        updated_ticket = self.ticket_repository.update_status(ticket, new_status)
        self.audit_service.record_ticket_status_updated(
            ticket_id=updated_ticket.id,
            user=user,
            previous_status=previous_status,
            new_status=updated_ticket.status,
        )
        return updated_ticket
