FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV PORT=7860

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend-api/requirements.txt backend-api/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r backend-api/requirements.txt

COPY backend-api backend-api
COPY models models

CMD ["sh", "-c", "uvicorn main:app --app-dir backend-api --host 0.0.0.0 --port ${PORT:-7860}"]
