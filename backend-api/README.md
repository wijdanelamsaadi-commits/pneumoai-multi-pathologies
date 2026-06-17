# PneumoAI Backend API

FastAPI backend for binary chest X-ray classification:

- `Normal`
- `Pneumonia`

## Run

From the project root:

```bash
python -m uvicorn main:app --app-dir backend-api --host 127.0.0.1 --port 8000
```

## Model Loading

The API loads:

```text
models/pneumonia_binary.keras
```

If this file is missing, it falls back to:

```text
models/pneumonia_model.keras
```

## Endpoint

```http
POST /analyze
```

Multipart form field:

```text
image
```

Response:

```json
{
  "prediction": "Pneumonia",
  "confidence": 97
}
```

`confidence` is the confidence of the returned class.
