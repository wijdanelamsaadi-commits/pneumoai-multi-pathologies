# Free Deployment Plan

This project should be deployed without Render and without a credit card.

## Recommended Architecture

- Frontend: Vercel
- Backend: Hugging Face Spaces with Docker
- Model: `models/pneumonia_binary.keras`

## Why Not Streamlit Cloud?

Streamlit Cloud runs `frontend/app.py`, so it shows the old Streamlit UI.
The new app is React + FastAPI and must be deployed as two services.

## Why Not Render?

Render may request a credit card for web services. Use Hugging Face Spaces instead.

## Backend on Hugging Face Spaces

Create a Space:

```text
Name: pneumoai-api
SDK: Docker
Visibility: Public
```

Connect/import this GitHub repository:

```text
https://github.com/wijdanelamsaadi-commits/pneumoai-multi-pathologies
```

The Space should use the root `Dockerfile`.

Runtime:

```text
Python: 3.11-slim Docker image
Port: 7860
Start command: uvicorn main:app --app-dir backend-api --host 0.0.0.0 --port 7860
```

Environment variables:

```text
PORT=7860
FRONTEND_ORIGINS=https://pneumoai-pneumonia-detection.vercel.app
```

Expected backend URL:

```text
https://YOUR-HF-USERNAME-pneumoai-api.hf.space
```

Health check:

```text
https://YOUR-HF-USERNAME-pneumoai-api.hf.space/health
```

Analyze endpoint:

```text
POST https://YOUR-HF-USERNAME-pneumoai-api.hf.space/analyze
FormData field: image
```

## Frontend on Vercel

Create a Vercel project:

```text
Repository: wijdanelamsaadi-commits/pneumoai-multi-pathologies
Root Directory: frontend-react
Framework Preset: Vite
Install Command: npm install
Build Command: npm run build
Output Directory: dist
```

Environment variable:

```text
VITE_API_BASE_URL=https://YOUR-HF-USERNAME-pneumoai-api.hf.space
```

Suggested frontend URL:

```text
https://pneumoai-pneumonia-detection.vercel.app
```

## After Vercel Deploys

Copy the final Vercel URL and update Hugging Face Spaces:

```text
FRONTEND_ORIGINS=<FINAL_VERCEL_URL>
```

Then restart the Space.

## Fallback If Hugging Face Spaces Is Too Slow

If TensorFlow cold start is too slow on the free CPU:

1. Keep Vercel frontend as a demo without API by disabling uploads temporarily.
2. Or deploy the old Streamlit app only, accepting that it is not the new React UI.
3. Or convert the new React UI into a Streamlit-only interface, but this loses the current React design.
