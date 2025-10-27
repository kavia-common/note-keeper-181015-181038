from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_session
from .models import Note
from .schemas import NoteCreate, NoteUpdate, NoteOut

router = APIRouter(
    prefix="/api/notes",
    tags=["Notes"],
)


def _get_note_or_404(db: Session, note_id: int) -> Note:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
    return note


@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Create a new note with a required title and optional content.",
)
# PUBLIC_INTERFACE
def create_note(payload: NoteCreate, db: Session = Depends(get_session)) -> NoteOut:
    """
    Create a new note.

    Args:
        payload: NoteCreate schema with title (required) and content (optional).
        db: SQLAlchemy session.

    Returns:
        NoteOut: The created note.
    """
    now = datetime.utcnow()
    note = Note(
        title=payload.title,
        content=payload.content,
        created_at=now,
        updated_at=now,
    )
    db.add(note)
    db.flush()  # populate PK
    return NoteOut.model_validate(note)


@router.get(
    "",
    response_model=List[NoteOut],
    summary="List notes",
    description="List all notes. Optionally filter by search query applied to title and content.",
)
# PUBLIC_INTERFACE
def list_notes(
    q: Optional[str] = Query(None, description="Search substring for title/content"),
    db: Session = Depends(get_session),
) -> List[NoteOut]:
    """
    List notes with optional simple search.

    Args:
        q: Optional search query to match within title or content (case-insensitive).
        db: SQLAlchemy session.

    Returns:
        List[NoteOut]: All matching notes.
    """
    stmt = select(Note)
    if q:
        like = f"%{q}%"
        from sqlalchemy import or_
        stmt = stmt.where(or_(Note.title.ilike(like), Note.content.ilike(like)))
    stmt = stmt.order_by(Note.created_at.desc())
    notes = db.execute(stmt).scalars().all()
    return [NoteOut.model_validate(n) for n in notes]


@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get a note",
    description="Retrieve a single note by its ID.",
)
# PUBLIC_INTERFACE
def get_note(note_id: int, db: Session = Depends(get_session)) -> NoteOut:
    """
    Get a note by ID.

    Args:
        note_id: Note identifier.
        db: SQLAlchemy session.

    Returns:
        NoteOut: The requested note.

    Raises:
        404: If the note is not found.
    """
    note = _get_note_or_404(db, note_id)
    return NoteOut.model_validate(note)


@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update a note",
    description="Update a note's title/content. Partial updates supported via optional fields.",
)
# PUBLIC_INTERFACE
def update_note(
    note_id: int, payload: NoteUpdate, db: Session = Depends(get_session)
) -> NoteOut:
    """
    Update an existing note by ID.

    Args:
        note_id: Note identifier.
        payload: Fields to update (title/content).
        db: SQLAlchemy session.

    Returns:
        NoteOut: The updated note.

    Raises:
        404: If the note is not found.
    """
    note = _get_note_or_404(db, note_id)
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    note.updated_at = datetime.utcnow()
    db.add(note)
    return NoteOut.model_validate(note)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its ID.",
)
# PUBLIC_INTERFACE
def delete_note(note_id: int, db: Session = Depends(get_session)) -> None:
    """
    Delete an existing note by ID.

    Args:
        note_id: Note identifier.
        db: SQLAlchemy session.

    Returns:
        None

    Raises:
        404: If the note is not found.
    """
    note = _get_note_or_404(db, note_id)
    db.delete(note)
    # 204 No Content return
    return None
