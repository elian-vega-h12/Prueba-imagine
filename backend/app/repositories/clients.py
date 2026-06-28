from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.clients import ClientCreate


class ClientRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: ClientCreate) -> Client:
        client = Client(**payload.model_dump())
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def list_all(self) -> list[Client]:
        statement = select(Client).order_by(Client.created_at.asc())
        return list(self.session.scalars(statement).all())

    def get(self, client_id: str) -> Client | None:
        return self.session.get(Client, client_id)
