from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class RecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    title: str
    content: str
    view_count: int
