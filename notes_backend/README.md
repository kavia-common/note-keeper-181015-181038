# Notes Backend (FastAPI)

A minimal FastAPI service providing CRUD endpoints for notes, backed by SQLite via SQLAlchemy.

- Runs in container: notes_backend
- Default port: 3001
- Database: SQLite file at `db/notes.db` (auto-created)
- OpenAPI docs: `/docs`
- Health: `/health`

## Endpoints

- GET `/health` — health check
- POST `/api/notes` — create a note
- GET `/api/notes` — list notes (optional search with `?q=...`)
- GET `/api/notes/{id}` — get a note by ID
- PUT `/api/notes/{id}` — update a note (title/content are optional)
- DELETE `/api/notes/{id}` — delete a note

## Schemas

- NoteCreate: `{ "title": "string", "content": "string|null" }`
- NoteUpdate: `{ "title": "string|null", "content": "string|null" }`
- NoteOut: `{ "id": number, "title": "string", "content": "string|null", "created_at": "ISO 8601", "updated_at": "ISO 8601" }`

## Quick start

The service is configured to start automatically on port 3001 in the provided environment.

If you need to run locally:

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

## Curl examples

Create a note:
```bash
curl -sS -X POST http://localhost:3001/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"My first note","content":"Hello world"}' | jq
```

List notes:
```bash
curl -sS http://localhost:3001/api/notes | jq
```

Search notes:
```bash
curl -sS "http://localhost:3001/api/notes?q=first" | jq
```

Get a note by ID:
```bash
curl -sS http://localhost:3001/api/notes/1 | jq
```

Update a note:
```bash
curl -sS -X PUT http://localhost:3001/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"content":"Updated text"}' | jq
```

Delete a note:
```bash
curl -sS -X DELETE -i http://localhost:3001/api/notes/1
```

## Environment

No environment variables are required by default.

## Notes

- CORS is enabled for all origins.
- Database tables are created automatically on startup via `Base.metadata.create_all`.
