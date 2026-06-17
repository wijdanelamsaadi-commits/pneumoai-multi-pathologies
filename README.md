# PneumoAI - Binary Pneumonia Detection

PneumoAI is a PFE project for chest X-ray analysis. This version intentionally returns to a reliable binary workflow:

- `Normal`
- `Pneumonia`

This version keeps the scope intentionally binary because the Pneumonia/Normal workflow is preferred for reliability.

## Technologies

- Frontend: React, Vite, Tailwind CSS, lucide-react
- Backend: FastAPI
- Model: TensorFlow / Keras, MobileNetV2 transfer learning
- Dataset: Kaggle Chest X-Ray Pneumonia, not included in this repository

## Project Structure

```text
backend-api/                  FastAPI binary inference API
frontend-react/               React interface
frontend/                     Original Streamlit app, preserved
models/pneumonia_binary.keras Binary Pneumonia/Normal model
models/pneumonia_model.keras  Legacy binary model, preserved
src/train_binary_pneumonia.py Binary training pipeline
notebooks/                    Colab notebooks
```

## Backend

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --app-dir backend-api --host 127.0.0.1 --port 8000
```

Analyze an image:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "image=@path/to/chest-xray.jpeg"
```

Expected response:

```json
{
  "prediction": "Pneumonia",
  "confidence": 97
}
```

## Frontend React

```bash
cd frontend-react
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

## Training

Dataset expected locally:

```text
data/chest_xray/
  train/NORMAL
  train/PNEUMONIA
  val/NORMAL
  val/PNEUMONIA
  test/NORMAL
  test/PNEUMONIA
```

Run:

```bash
python src/train_binary_pneumonia.py
```

Outputs:

- `models/pneumonia_binary.keras`
- `models/binary_metrics.csv`

## Colab

Use:

```text
notebooks/PneumoAI_Binary_Pneumonia_Colab.ipynb
```

It downloads Kaggle `paultimothymooney/chest-xray-pneumonia`, trains the binary model, exports metrics, and saves the model to Google Drive.

## Data Policy

The dataset is not included. Do not commit:

- `data/`
- Kaggle tokens
- zip archives
- virtual environments
- `node_modules/`
