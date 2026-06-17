# PneumoAI Multi-Pathologies

PneumoAI is a final-year project platform for chest X-ray analysis. The improved version provides a modern React interface, a FastAPI backend, image quality assessment, and a V2 training pipeline for multi-label lung pathology detection.

The target V2 model follows the report requirements:

- Dataset: CheXpert-small only
- Problem type: multi-label
- Architecture: MobileNetV2
- Outputs: `Dense(3, activation="sigmoid")`
- Loss: `binary_crossentropy`
- Labels: `Pneumonia`, `Consolidation`, `Pleural Effusion`

`Normal` is not trained as a class. It is derived as the absence or low probability of the three target pathologies.

## Project Structure

```text
backend-api/      FastAPI API for image analysis
frontend-react/   React + Vite + Tailwind web interface
frontend/         Original Streamlit interface, kept for reference
src/              Training, preparation, quality and prediction scripts
models/           Small model/assets kept when within GitHub limits
notebooks/        Exploration and validation notebooks
```

## Technologies

- React
- Vite
- Tailwind CSS
- lucide-react
- FastAPI
- TensorFlow / Keras
- MobileNetV2
- OpenCV
- Pillow
- CheXpert-small

## Dataset Note

CheXpert-small is not included in this repository.

You must download it separately after accepting the official dataset terms. Do not commit the dataset, downloaded archives, Kaggle credentials, or API tokens.

Expected local preparation flow:

```bash
python src/prepare_chexpert_small.py --archive data/CheXpert-v1.0-small.zip
```

or, if you have an authorized direct URL:

```bash
python src/prepare_chexpert_small.py --url "AUTHORIZED_CHEXPERT_SMALL_URL"
```

The preparation script creates:

```text
data/chexpert-small-reduced/train_reduced.csv
data/chexpert-small-reduced/valid_reduced.csv
```

Only these labels are retained:

- `Pneumonia`
- `Consolidation`
- `Pleural Effusion`

## Train the V2 Model

From the project root:

```bash
python src/train_multilabel_chexpert.py --data-dir data/chexpert-small-reduced
```

The trained V2 model is saved to:

```text
models/multilabel_mobilenetv2.keras
```

The older binary model `models/pneumonia_model.keras` is preserved.

## Backend Setup

```bash
cd backend-api
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Analyze an image:

```bash
curl -X POST http://127.0.0.1:8000/analyze -F "image=@radio.png"
```

## Frontend Setup

```bash
cd frontend-react
npm install
npm run dev
```

Default URL:

```text
http://127.0.0.1:5173
```

Production build:

```bash
npm run build
```

## Security and Repository Hygiene

This repository must not include:

- CheXpert data or any dataset images
- `kaggle.json`
- `.env` files
- API keys or tokens
- downloaded archives such as `.zip`
- large model files rejected by GitHub
- local virtual environments
- `node_modules`

## Medical Disclaimer

PneumoAI is a decision-support prototype. It does not replace the opinion, diagnosis, or supervision of a qualified healthcare professional.
