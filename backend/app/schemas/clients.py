from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    company: str = Field(min_length=1, max_length=160)


class ClientRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    company: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
