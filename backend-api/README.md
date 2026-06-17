# API FastAPI PneumoAI V2

API separee pour l'interface React. La V2 respecte le rapport final:

- dataset retenu: CheXpert-small
- probleme: multi-label
- architecture: MobileNetV2
- sortie modele: `Dense(3, activation="sigmoid")`
- loss: `binary_crossentropy`
- labels entraines: `Pneumonia`, `Consolidation`, `Pleural Effusion`

`Normal` n'est pas une classe entrainee. Le score Normal est derive cote API:
absence ou faible probabilite des trois pathologies ciblees.

## Modele attendu

Le backend charge:

```bash
models/multilabel_mobilenetv2.keras
```

L'ancien modele est conserve:

```bash
models/pneumonia_model.keras
```

## Preparation CheXpert-small uniquement

CheXpert requiert l'acceptation des conditions d'utilisation sur Stanford AIMI.
Apres obtention du lien ou de l'archive autorisee, preparer uniquement la version
small:

```bash
python src/prepare_chexpert_small.py --archive data/CheXpert-v1.0-small.zip
```

ou avec un lien direct autorise:

```bash
python src/prepare_chexpert_small.py --url "LIEN_AUTORISE_CHEXPERT_V1_SMALL"
```

Le script refuse explicitement `CheXpert-v1.0` complet et genere:

```bash
data/chexpert-small-reduced/train_reduced.csv
data/chexpert-small-reduced/valid_reduced.csv
```

Les CSV reduits contiennent uniquement:

- `Pneumonia`
- `Consolidation`
- `Pleural Effusion`

## Entrainement du modele V2

Depuis la racine du projet:

```bash
python src/train_multilabel_chexpert.py --data-dir data/chexpert-small-reduced
```

Le dossier prepare doit contenir `train_reduced.csv` et `valid_reduced.csv`.

## Lancement

```bash
cd backend-api
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## Endpoints

- `GET /health`: verifie l'API et indique si le modele V2 est present.
- `POST /analyze`: recoit une image dans le champ multipart `image`, calcule la
  qualite et retourne les probabilites reelles des 3 labels V2.

Exemple:

```bash
curl -X POST http://127.0.0.1:8000/analyze -F "image=@radio.png"
```

Reponse simplifiee:

```json
{
  "modele": {
    "version": "v2",
    "architecture": "MobileNetV2",
    "dataset": "CheXpert-small",
    "type": "multi-label"
  },
  "qualite": {
    "score": 92,
    "label": "Excellente qualite",
    "criteres": [
      { "nom": "Nettete", "score": 94 },
      { "nom": "Luminosite", "score": 90 },
      { "nom": "Contraste", "score": 92 }
    ]
  },
  "predictions": {
    "pneumonie": 0,
    "consolidation": 0,
    "epanchement_pleural": 0
  },
  "pathologies": [
    { "nom": "Pneumonie", "probabilite": 0 },
    { "nom": "Epanchement pleural", "probabilite": 0 },
    { "nom": "Consolidation", "probabilite": 0 },
    { "nom": "Normal", "probabilite": 0 }
  ]
}
```
