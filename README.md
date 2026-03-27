# ChakraView

A production-grade FastAPI backend — built checkpoint by checkpoint.

---

## Project Structure

```
ChakraView/
├── app/
│   ├── main.py               # FastAPI app factory + health endpoint
│   ├── api/
│   │   └── routes.py         # API route definitions
│   ├── core/
│   │   ├── config.py         # App settings (pydantic-settings)
│   │   └── middleware.py     # Request logging middleware
│   └── models/
│       └── schemas.py        # Pydantic request/response + StandardResponse
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

Returns app health status. Used by monitoring tools and load balancers.

**Response:**
```json
{
  "status": "ok"
}
```

---

## Interactive API Docs

Once the server is running, visit:

- **Swagger UI** → http://localhost:8000/docs
- **ReDoc**      → http://localhost:8000/redoc

---

## Logging Middleware

Every request is automatically logged to stdout in this format:

```
2024-01-01 00:00:00,000 | INFO | POST /api/v1/run-workflow - 200 (3.21ms)
```

Logs include: **timestamp | log level | HTTP method | path | status code | duration**

No setup required — active on all routes automatically.

---

## Standard Response Envelope (from Checkpoint 11)

The `StandardResponse` schema is defined and ready in `app/models/schemas.py`.
It will wrap all responses from Checkpoint 11 onward:

```json
{
  "status": "success",
  "data": { },
  "error": null
}
```

| Field   | Type            | Description                        |
|---------|-----------------|------------------------------------||
| `status`  | `str`         | `"success"` or `"error"`           |
| `data`    | `Any` / `null`| Response payload                   |
| `error`   | `str` / `null`| Error message if status is `error` |

---

## Checkpoint Progress

| Checkpoint | Description                        | Status     |
|------------|------------------------------------|------------|
| 1          | Project setup + foundation         | ✅ Done    |
| 1.1        | Health check, logging, envelope    | ✅ Done    |
