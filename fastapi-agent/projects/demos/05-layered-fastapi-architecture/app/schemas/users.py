from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    # TODO: define name validation.
    name: str = Field(..., min_length=2, max_length=100)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # TODO: define id and name response fields.
    id: int
    name: str
    pass
