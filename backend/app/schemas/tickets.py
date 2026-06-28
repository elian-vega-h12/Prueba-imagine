from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TicketStatus(StrEnum):
    pending = "Pendiente"
    in_progress = "En progreso"
    done = "Finalizado"


class TicketCreate(BaseModel):
    client_id: UUID
    title: str = Field(min_length=1, max_length=180)
    description: str = Field(min_length=1)


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketRead(BaseModel):
    id: UUID
    client_id: UUID
    title: str
    description: str
    status: TicketStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
