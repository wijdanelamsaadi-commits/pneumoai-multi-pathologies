"""
PIPELINE COMPLET: Quality Assessment + Diagnostic Pneumonie
Le systeme final qui combine les 2 modules
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from quality_assessment import QualityAssessment


class PneumoniaDetectionSystem:
    """Systeme complet: qualite + diagnostic."""
    
    def __init__(self, model_path="models/pneumonia_model.keras"):
        print("Initialisation du systeme...")
        print("  - Chargement du modele de pneumonie...")
        self.model = load_model(model_path)
        print("  - Chargement du module Quality Assessment...")
        self.quality_module = QualityAssessment()
        self.IMAGE_SIZE = 224
        print("Systeme pret!\n")
    
    def analyze(self, image_path):
        """Analyser une radiographie complete."""
        image = Image.open(image_path).convert('RGB')
        quality_result = self.quality_module.evaluate(image)
        
        result = {
            'image_path': image_path,
            'quality': quality_result,
            'diagnosis': None,
            'confidence': None,
            'final_decision': None,
            'message': None
        }
        
        # Si qualite insuffisante, on rejette
        if quality_result['decision'] == 'REJET':
            result['final_decision'] = 'REACQUISITION_REQUISE'
            result['message'] = ("Image de mauvaise qualite. "
                               "Refaire la radiographie est necessaire.")
            return result
        
        # Sinon, on fait le diagnostic
        img_resized = image.resize((self.IMAGE_SIZE, self.IMAGE_SIZE))
        img_array = np.array(img_resized) / 255.0
        img_batch = np.expand_dims(img_array, axis=0)
        
        prediction = self.model.predict(img_batch, verbose=0)
        probability = float(prediction[0][0])
        
        if probability >= 0.5:
            diagnosis = "PNEUMONIA"
            confidence = probability * 100
        else:
            diagnosis = "NORMAL"
            confidence = (1 - probability) * 100
        
        result['diagnosis'] = diagnosis
        result['confidence'] = confidence
        result['probability'] = probability
        
        # Decision finale selon qualite
        if quality_result['decision'] == 'ACCEPTABLE':
            result['final_decision'] = 'DIAGNOSTIC_FIABLE'
            result['message'] = f"Diagnostic: {diagnosis} ({confidence:.1f}% de confiance)"
        else:
            result['final_decision'] = 'DIAGNOSTIC_AVEC_PRUDENCE'
            result['message'] = (f"Diagnostic: {diagnosis} ({confidence:.1f}%) - "
                               "Qualite moyenne, validation par radiologue recommande.")
        
        return result
    
    def display_result(self, result):
        """Afficher le resultat dans le terminal."""
        print("=" * 70)
        print(f"ANALYSE: {os.path.basename(result['image_path'])}")
        print("=" * 70)
        
        print("\n[QUALITE D'IMAGE]")
        q = result['quality']
        print(f"  Nettete:    {q['sharpness']['score']:6.1f}/100")
        print(f"  Luminosite: {q['brightness']['score']:6.1f}/100")
        print(f"  Contraste:  {q['contrast']['score']:6.1f}/100")
        print(f"  GLOBAL:     {q['global_score']:6.1f}/100  ->  {q['decision']}")
        
        print("\n[DIAGNOSTIC]")
        if result['diagnosis']:
            print(f"  Resultat: {result['diagnosis']}")
            print(f"  Confiance: {result['confidence']:.2f}%")
        else:
            print("  Diagnostic non effectue (qualite insuffisante)")
        
        print("\n[DECISION FINALE]")
        print(f"  Status: {result['final_decision']}")
        print(f"  Message: {result['message']}")
        print()


# ===== TEST DU SYSTEME =====
if __name__ == "__main__":
    
    system = PneumoniaDetectionSystem()
    
    test_images = [
        "data/chest_xray/test/NORMAL/IM-0001-0001.jpeg",
        "data/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg",
        "data/chest_xray/test/NORMAL/NORMAL2-IM-0060-0001.jpeg",
        "data/chest_xray/test/PNEUMONIA/person1_virus_8.jpeg",
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()
    
    for i, img_path in enumerate(test_images):
        result = system.analyze(img_path)
        system.display_result(result)
        
        img = Image.open(img_path)
        axes[i].imshow(img, cmap='gray')
        
        decision = result['final_decision']
        if decision == 'DIAGNOSTIC_FIABLE':
            color = 'green'
        elif decision == 'DIAGNOSTIC_AVEC_PRUDENCE':
            color = 'orange'
        else:
            color = 'red'
        
        title = f"Qualite: {result['quality']['decision']} ({result['quality']['global_score']:.1f}/100)\n"
        if result['diagnosis']:
            title += f"Diagnostic: {result['diagnosis']} ({result['confidence']:.1f}%)\n"
        title += f"=> {decision}"
        
        axes[i].set_title(title, color=color, fontweight='bold', fontsize=10)
        axes[i].axis('off')
    
    plt.suptitle("SYSTEME COMPLET: Quality + Diagnostic Pneumonie",
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('models/pipeline_complet_test.png', dpi=100, bbox_inches='tight')
    plt.show()
    
    print("=" * 70)
    print("TEST DU PIPELINE COMPLET TERMINE!")
    print("=" * 70)