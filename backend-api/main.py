import os
from functools import lru_cache
from io import BytesIO
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BINARY_MODEL_PATH = PROJECT_ROOT / "models" / "pneumonia_binary.keras"
LEGACY_BINARY_MODEL_PATH = PROJECT_ROOT / "models" / "pneumonia_model.keras"
IMAGE_SIZE = 224
PNEUMONIA_THRESHOLD = 0.5


app = FastAPI(
    title="PneumoAI API",
    description="API binaire pour la detection Pneumonia / Normal sur radiographies thoraciques.",
    version="2.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def resolve_model_path() -> Path:
    if BINARY_MODEL_PATH.exists():
        return BINARY_MODEL_PATH
    if LEGACY_BINARY_MODEL_PATH.exists():
        return LEGACY_BINARY_MODEL_PATH
    raise FileNotFoundError(
        "Aucun modele binaire Pneumonia/Normal trouve. "
        f"Attendu: {BINARY_MODEL_PATH} ou {LEGACY_BINARY_MODEL_PATH}."
    )


@lru_cache(maxsize=1)
def get_model():
    return load_model(str(resolve_model_path()))


def preprocess_for_binary_model(image: Image.Image) -> np.ndarray:
    img_resized = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    img_array = np.array(img_resized).astype("float32") / 255.0
    return np.expand_dims(img_array, axis=0)


def predict_binary(image: Image.Image) -> dict:
    raw_prediction = get_model().predict(preprocess_for_binary_model(image), verbose=0)
    pneumonia_probability = float(np.ravel(raw_prediction)[0])
    normal_probability = 1.0 - pneumonia_probability

    if pneumonia_probability >= PNEUMONIA_THRESHOLD:
        prediction = "Pneumonia"
        confidence = pneumonia_probability
    else:
        prediction = "Normal"
        confidence = normal_probability

    return {
        "prediction": prediction,
        "confidence": int(round(confidence * 100)),
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    try:
        model_path = resolve_model_path()
        model_status = "ready"
    except FileNotFoundError:
        model_path = BINARY_MODEL_PATH
        model_status = "missing"

    return {
        "status": "ok",
        "version": "2.1.0",
        "task": "binary_pneumonia_detection",
        "classes": "Normal,Pneumonia",
        "model": str(model_path),
        "model_status": model_status,
    }


@app.post("/analyze")
async def analyze_image(image: UploadFile = File(...)) -> dict:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier envoye doit etre une image.")

    image_bytes = await image.read()
    await image.close()

    try:
        pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Image invalide ou illisible.") from exc

    try:
        return predict_binary(pil_image)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
