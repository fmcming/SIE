# YOLO Defect Detection Starter

This is a minimal starter for a YOLO-based defect detection service with a simple FastAPI API.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

- `GET /health`: health check
- `POST /infer`: inference stub

Example payload:

```json
{
  "image_path": "/path/to/image.jpg",
  "model_version": "default"
}
```
