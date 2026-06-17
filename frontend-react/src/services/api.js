const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "");

export const emptyAnalysisResult = {
  fileName: "",
  qualite: {
    score: 0,
    label: "Aucune analyse effectu\u00e9e",
    criteres: [
      { nom: "Nettet\u00e9", score: 0 },
      { nom: "Luminosit\u00e9", score: 0 },
      { nom: "Contraste", score: 0 }
    ]
  },
  predictions: {
    pneumonie: { probabilite: 0, statut: "" },
    normal: { probabilite: 0, statut: "" }
  },
  pathologies: [
    { nom: "Pneumonie", probabilite: 0, statut: "", positive: false, seuil: null, description: "Aucune analyse effectu\u00e9e" },
    { nom: "Normal", probabilite: 0, statut: "", positive: false, seuil: null, description: "Aucune analyse effectu\u00e9e" }
  ]
};

export async function analyzeImage(file) {
  if (!file) {
    return emptyAnalysisResult;
  }
  if (!API_BASE_URL) {
    throw new Error("Configuration API manquante: VITE_API_BASE_URL doit pointer vers le backend Render.");
  }

  const formData = new FormData();
  formData.append("image", file);

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    let message = "Erreur lors de l'analyse de l'image.";
    try {
      const payload = await response.json();
      message = payload.detail || message;
    } catch {
      message = await response.text() || message;
    }
    throw new Error(message);
  }

  const data = await response.json();
  return {
    fileName: file.name,
    ...toBinaryAnalysisResult(data)
  };
}

function toBinaryAnalysisResult(data) {
  const prediction = data.prediction === "Pneumonia" ? "Pneumonia" : "Normal";
  const confidence = Number(data.confidence) || 0;
  const pneumoniaScore = prediction === "Pneumonia" ? confidence : Math.max(0, 100 - confidence);
  const normalScore = prediction === "Normal" ? confidence : Math.max(0, 100 - confidence);

  return {
    prediction,
    confidence,
    qualite: {
      score: 0,
      label: "Analyse binaire Pneumonia / Normal",
      criteres: [
        { nom: "Nettet\u00e9", score: 0 },
        { nom: "Luminosit\u00e9", score: 0 },
        { nom: "Contraste", score: 0 }
      ]
    },
    predictions: {
      pneumonie: {
        probabilite: pneumoniaScore,
        statut: prediction === "Pneumonia" ? "Positive" : "Negative"
      },
      normal: {
        probabilite: normalScore,
        statut: prediction === "Normal" ? "Positive" : "Negative"
      }
    },
    pathologies: [
      {
        nom: "Pneumonie",
        probabilite: pneumoniaScore,
        statut: prediction === "Pneumonia" ? "Positive" : "Negative",
        positive: prediction === "Pneumonia",
        seuil: 50,
        description: prediction === "Pneumonia"
          ? "Radiographie class\u00e9e comme Pneumonia par le mod\u00e8le binaire."
          : "Probabilit\u00e9 faible de pneumonie selon le mod\u00e8le binaire."
      },
      {
        nom: "Normal",
        probabilite: normalScore,
        statut: prediction === "Normal" ? "Positive" : "Negative",
        positive: prediction === "Normal",
        seuil: 50,
        description: prediction === "Normal"
          ? "Radiographie class\u00e9e comme Normal par le mod\u00e8le binaire."
          : "La radiographie n'est pas class\u00e9e comme Normal par le mod\u00e8le binaire."
      }
    ]
  };
}
