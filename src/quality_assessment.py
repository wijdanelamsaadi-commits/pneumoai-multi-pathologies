"""
Module Quality Assessment
Evaluation de la qualite d'une radiographie thoracique
"""

import cv2
import numpy as np
from PIL import Image


class QualityAssessment:
    """
    Classe pour evaluer la qualite d'une radiographie thoracique.
    """
    
    def __init__(self):
        # Seuils empiriques ajustes apres tests
        self.SHARPNESS_THRESHOLD = 150
        self.BRIGHTNESS_MIN = 60
        self.BRIGHTNESS_MAX = 180
        self.CONTRAST_THRESHOLD = 50
    
    def assess_sharpness(self, image_array):
        """Mesurer la nettete via la variance du Laplacien."""
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array
        
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        score = min(100, (laplacian_var / self.SHARPNESS_THRESHOLD) * 100)
        
        return {
            'value': float(laplacian_var),
            'score': float(score),
            'is_acceptable': laplacian_var >= self.SHARPNESS_THRESHOLD
        }
    
    def assess_brightness(self, image_array):
        """Mesurer la luminosite moyenne."""
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array
        
        mean_brightness = np.mean(gray)
        
        optimal = (self.BRIGHTNESS_MIN + self.BRIGHTNESS_MAX) / 2
        max_deviation = (self.BRIGHTNESS_MAX - self.BRIGHTNESS_MIN) / 2
        deviation = abs(mean_brightness - optimal)
        score = max(0, 100 * (1 - deviation / max_deviation))
        
        is_acceptable = (self.BRIGHTNESS_MIN <= mean_brightness <= self.BRIGHTNESS_MAX)
        
        return {
            'value': float(mean_brightness),
            'score': float(score),
            'is_acceptable': bool(is_acceptable)
        }
    
    def assess_contrast(self, image_array):
        """Mesurer le contraste via l'ecart-type."""
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array
        
        contrast = np.std(gray)
        score = min(100, (contrast / self.CONTRAST_THRESHOLD) * 100)
        
        return {
            'value': float(contrast),
            'score': float(score),
            'is_acceptable': contrast >= self.CONTRAST_THRESHOLD
        }
    
    def evaluate(self, image):
        """Evaluation complete de la qualite."""
        if isinstance(image, Image.Image):
            image_array = np.array(image)
        else:
            image_array = image
        
        sharpness = self.assess_sharpness(image_array)
        brightness = self.assess_brightness(image_array)
        contrast = self.assess_contrast(image_array)
        
        # Score global (moyenne ponderee equilibree)
        global_score = (
            sharpness['score'] * 0.4 +
            brightness['score'] * 0.3 +
            contrast['score'] * 0.3
        )
        
        # Decision finale
        if global_score >= 70:
            decision = "ACCEPTABLE"
            recommendation = "Image de bonne qualite, prediction fiable."
        elif global_score >= 40:
            decision = "MOYENNE"
            recommendation = "Image de qualite moyenne, prediction avec prudence."
        else:
            decision = "REJET"
            recommendation = "Image de mauvaise qualite, refaire l'acquisition recommande."
        
        return {
            'sharpness': sharpness,
            'brightness': brightness,
            'contrast': contrast,
            'global_score': float(global_score),
            'decision': decision,
            'recommendation': recommendation
        }


# ===== TEST DU MODULE =====
if __name__ == "__main__":
    
    import os
    import matplotlib.pyplot as plt
    
    qa = QualityAssessment()
    
    test_path = "data/chest_xray/test/PNEUMONIA"
    test_files = os.listdir(test_path)[:4]
    
    print("=" * 70)
    print("TEST DU MODULE QUALITY ASSESSMENT")
    print("=" * 70)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()
    
    for i, filename in enumerate(test_files):
        image_path = os.path.join(test_path, filename)
        img = Image.open(image_path).convert('RGB')
        result = qa.evaluate(img)
        
        print(f"\n--- Image {i+1}: {filename} ---")
        print(f"Nettete:     {result['sharpness']['value']:.2f} "
              f"(score: {result['sharpness']['score']:.1f}/100)")
        print(f"Luminosite:  {result['brightness']['value']:.2f} "
              f"(score: {result['brightness']['score']:.1f}/100)")
        print(f"Contraste:   {result['contrast']['value']:.2f} "
              f"(score: {result['contrast']['score']:.1f}/100)")
        print(f"Score global: {result['global_score']:.1f}/100")
        print(f"Decision: {result['decision']}")
        
        if result['decision'] == 'ACCEPTABLE':
            color = 'green'
        elif result['decision'] == 'MOYENNE':
            color = 'orange'
        else:
            color = 'red'
        
        title = f"{result['decision']}\n"
        title += f"Score: {result['global_score']:.1f}/100\n"
        title += f"Net: {result['sharpness']['score']:.0f} | "
        title += f"Lum: {result['brightness']['score']:.0f} | "
        title += f"Con: {result['contrast']['score']:.0f}"
        
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(title, color=color, fontweight='bold', fontsize=11)
        axes[i].axis('off')
    
    plt.suptitle("Evaluation de qualite des radiographies",
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    print("\n" + "=" * 70)
    print("TEST TERMINE!")
    print("=" * 70)