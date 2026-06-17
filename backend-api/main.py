import os
import sys
from functools import lru_cache
from io import BytesIO
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from quality_assessment import QualityAssessment


MODEL_PATH = PROJECT_ROOT / "models" / "multilabel_mobilenetv2.keras"
LEGACY_MODEL_PATH = PROJECT_ROOT / "models" / "pneumonia_model.keras"
IMAGE_SIZE = 224
LABELS = [
    ("pneumonie", "Pneumonie"),
    ("consolidation", "Consolidation"),
    ("epanchement_pleural", "\u00c9panchement pleural"),
]


app = FastAPI(
    title="PneumoAI API V2",
    description="API multi-label pour l'analyse CheXpert-small de radiographies thoraciques.",
    version="2.0.0",
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


@lru_cache(maxsize=1)
def get_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Le modele V2 multi-label est introuvable. "
            f"Entrainez-le d'abord avec src/train_multilabel_chexpert.py pour creer {MODEL_PATH}."
        )
    return load_model(str(MODEL_PATH))


@lru_cache(maxsize=1)
def get_quality_assessor():
    return QualityAssessment()


def preprocess_for_mobilenet(image: Image.Image) -> np.ndarray:
    img_resized = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    img_array = np.array(img_resized).astype("float32")
    img_array = preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)


def predict_multilabel(image: Image.Image) -> dict[str, int]:
    prediction = get_model().predict(preprocess_for_mobilenet(image), verbose=0)[0]
    probabilities = {
        api_key: int(round(float(value) * 100))
        for (api_key, _display_name), value in zip(LABELS, prediction)
    }
    probabilities["normal"] = int(round((1 - max(prediction)) * 100))
    return probabilities


def assess_quality(image: Image.Image) -> dict:
    result = get_quality_assessor().evaluate(image)
    score = int(round(result["global_score"]))
    if score >= 85:
        label = "Excellente qualit\u00e9"
    elif score >= 70:
        label = "Bonne qualit\u00e9"
    elif score >= 40:
        label = "Qualit\u00e9 moyenne"
    else:
        label = "Qualit\u00e9 insuffisante"

    return {
        "score": score,
        "label": label,
        "criteres": [
            {"nom": "Nettet\u00e9", "score": int(round(result["sharpness"]["score"]))},
            {"nom": "Luminosit\u00e9", "score": int(round(result["brightness"]["score"]))},
            {"nom": "Contraste", "score": int(round(result["contrast"]["score"]))},
        ],
    }


def pathology_description(name: str, probability: int) -> str:
    if probability <= 0:
        return "Aucune analyse effectu\u00e9e"

    descriptions = {
        "Pneumonie": "Probabilit\u00e9 de signes compatibles avec une pneumonie.",
        "Consolidation": "Probabilit\u00e9 de zones de consolidation dans le parenchyme pulmonaire.",
        "\u00c9panchement pleural": "Probabilit\u00e9 d'un \u00e9panchement pleural visible sur la radiographie.",
        "Normal": "Score d\u00e9riv\u00e9: absence ou faible probabilit\u00e9 des trois pathologies cibl\u00e9es.",
    }
    return descriptions[name]


def build_pathologies(scores: dict[str, int]) -> list[dict]:
    items = [
        ("Pneumonie", scores["pneumonie"]),
        ("\u00c9panchement pleural", scores["epanchement_pleural"]),
        ("Consolidation", scores["consolidation"]),
        ("Normal", scores["normal"]),
    ]
    return [
        {
            "nom": name,
            "probabilite": probability,
            "description": pathology_description(name, probability),
        }
        for name, probability in items
    ]


@app.get("/health")
def health_check() -> dict[str, str]:
    model_status = "ready" if MODEL_PATH.exists() else "missing"
    return {
        "status": "ok",
        "version": "2.0.0",
        "model": str(MODEL_PATH),
        "model_status": model_status,
        "legacy_model_preserved": str(LEGACY_MODEL_PATH.exists()).lower(),
    }


@app.post("/analyze")
async def analyze_image(image: UploadFile = File(...)) -> dict:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier envoy\u00e9 doit \u00eatre une image.")

    image_bytes = await image.read()
    await image.close()

    try:
        pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Image invalide ou illisible.") from exc

    try:
        scores = predict_multilabel(pil_image)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "modele": {
            "version": "v2",
            "architecture": "MobileNetV2",
            "dataset": "CheXpert-small",
            "type": "multi-label",
            "labels": ["Pneumonia", "Consolidation", "Pleural Effusion"],
            "normal": "derive_absence_pathologies",
        },
        "qualite": assess_quality(pil_image),
        "predictions": {
            "pneumonie": scores["pneumonie"],
            "consolidation": scores["consolidation"],
            "epanchement_pleural": scores["epanchement_pleural"],
        },
        "pathologies": build_pathologies(scores),
    }
