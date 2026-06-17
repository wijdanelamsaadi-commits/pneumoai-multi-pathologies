const API_URL = "http://127.0.0.1:8000/analyze";

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
    pneumonie: 0,
    consolidation: 0,
    epanchement_pleural: 0
  },
  pathologies: [
    { nom: "Pneumonie", probabilite: 0, description: "Aucune analyse effectu\u00e9e" },
    { nom: "\u00c9panchement pleural", probabilite: 0, description: "Aucune analyse effectu\u00e9e" },
    { nom: "Consolidation", probabilite: 0, description: "Aucune analyse effectu\u00e9e" },
    { nom: "Normal", probabilite: 0, description: "Aucune analyse effectu\u00e9e" }
  ]
};

export async function analyzeImage(file) {
  if (!file) {
    return emptyAnalysisResult;
  }

  const formData = new FormData();
  formData.append("image", file);

  const response = await fetch(API_URL, {
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
    ...data
  };
}
