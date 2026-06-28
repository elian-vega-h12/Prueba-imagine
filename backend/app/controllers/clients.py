from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.clients import ClientRepository
from app.schemas.clients import ClientCreate, ClientRead
from app.services.clients import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


def get_client_service(session: Annotated[Session, Depends(get_session)]) -> ClientService:
    return ClientService(ClientRepository(session))


@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreate,
    service: Annotated[ClientService, Depends(get_client_service)],
):
    return service.create_client(payload)


@router.get("", response_model=list[ClientRead])
def list_clients(service: Annotated[ClientService, Depends(get_client_service)]):
    return service.list_clients()


@router.get("/{client_id}", response_model=ClientRead)
def get_client(
    client_id: UUID,
    service: Annotated[ClientService, Depends(get_client_service)],
):
    return service.get_client(str(client_id))
