# ChakraView

A production-grade FastAPI backend — built checkpoint by checkpoint.

---

## Project Structure

```
ChakraView/
├── app/
│   ├── main.py           # FastAPI app factory
│   ├── api/
│   │   └── routes.py     # API route definitions
│   ├── core/
│   │   └── config.py     # App settings (pydantic-settings)
│   └── models/
│       └── schemas.py    # Pydantic request/response schemas
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Server

From inside the `ChakraView/` directory:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

| Flag       | Purpose                                      |
|------------|----------------------------------------------|
| `--reload` | Auto-restart on file changes (development)   |
| `--host`   | Bind to all interfaces                       |
| `--port`   | Listen on port 8000                          |

---

## API Endpoints

### `POST /api/v1/run-workflow`

Accepts a workflow query and acknowledges receipt.

**Request body:**
```json
{
  "query": "your query string here"
}
```

**Response:**
```json
{
  "status": "received",
  "query": "your query string here"
}
```

**Validation rules:**
- `query` is required
- `query` must be a non-empty string

---

### `GET /health`

Returns app health status.

**Response:**
```json
{
  "status": "ok",
  "app": "ChakraView"
}
```

---

## Interactive API Docs

Once the server is running, visit:

- **Swagger UI** → http://localhost:8000/docs
- **ReDoc**      → http://localhost:8000/redoc

---

## Checkpoint Progress

| Checkpoint | Description              | Status |
|------------|--------------------------|--------|
| 1          | Project setup + foundation | ✅ Done |
