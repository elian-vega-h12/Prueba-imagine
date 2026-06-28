from fastapi import HTTPException, status

from app.models.client import Client
from app.repositories.clients import ClientRepository
from app.schemas.clients import ClientCreate


class ClientService:
    def __init__(self, repository: ClientRepository) -> None:
        self.repository = repository

    def create_client(self, payload: ClientCreate) -> Client:
        return self.repository.create(payload)

    def list_clients(self) -> list[Client]:
        return self.repository.list_all()

    def get_client(self, client_id: str) -> Client:
        client = self.repository.get(client_id)
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found",
            )
        return client
