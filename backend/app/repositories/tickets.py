from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.tickets import TicketCreate, TicketStatus


class TicketRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: TicketCreate) -> Ticket:
        ticket = Ticket(
            client_id=str(payload.client_id),
            title=payload.title,
            description=payload.description,
            status=TicketStatus.pending.value,
        )
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket

    def list_all(self) -> list[Ticket]:
        statement = select(Ticket).order_by(Ticket.created_at.asc())
        return list(self.session.scalars(statement).all())

    def get(self, ticket_id: str) -> Ticket | None:
        return self.session.get(Ticket, ticket_id)

    def update_status(self, ticket: Ticket, status: TicketStatus) -> Ticket:
        ticket.status = status.value
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket
