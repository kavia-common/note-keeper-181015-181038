from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base fields shared by Note schemas."""
    title: str = Field(..., description="Title of the note")
    content: Optional[str] = Field(None, description="Optional note content/body")


# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Schema for creating a note."""
    pass


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Schema for updating a note."""
    title: Optional[str] = Field(None, description="Updated title of the note")
    content: Optional[str] = Field(None, description="Updated content/body of the note")


# PUBLIC_INTERFACE
class NoteOut(BaseModel):
    """Schema for reading a note back to clients."""
    id: int = Field(..., description="Unique identifier of the note")
    title: str = Field(..., description="Title of the note")
    content: Optional[str] = Field(None, description="Optional note content/body")
    created_at: datetime = Field(..., description="Creation timestamp (ISO 8601)")
    updated_at: datetime = Field(..., description="Last update timestamp (ISO 8601)")

    class Config:
        from_attributes = True
