"""
Script 04: Test du module Quality avec images degradees
Objectif: Prouver que le module detecte bien les problemes de qualite
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quality_assessment import QualityAssessment
from PIL import Image, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np

# ===== CONFIGURATION =====
TEST_IMAGE = "data/chest_xray/test/NORMAL/IM-0001-0001.jpeg"

# Initialiser le module
qa = QualityAssessment()

# Charger l'image originale
print("Chargement de l'image originale...")
original = Image.open(TEST_IMAGE).convert('RGB')


# ===== CREER 4 VERSIONS DEGRADEES =====
print("\nCreation des versions degradees...")

# 1. Image originale (qualite maximale)
img_original = original

# 2. Image legerement floue
img_blur_light = original.filter(ImageFilter.GaussianBlur(radius=2))

# 3. Image tres floue
img_blur_heavy = original.filter(ImageFilter.GaussianBlur(radius=8))

# 4. Image trop sombre
enhancer = ImageEnhance.Brightness(original)
img_dark = enhancer.enhance(0.3)  # 30% de luminosite

# 5. Image trop claire
img_bright = enhancer.enhance(2.5)  # 250% de luminosite

# 6. Image faible contraste
contrast_enhancer = ImageEnhance.Contrast(original)
img_low_contrast = contrast_enhancer.enhance(0.3)

# Liste des images a tester
images_test = [
    ("Original", img_original),
    ("Flou leger", img_blur_light),
    ("Flou fort", img_blur_heavy),
    ("Trop sombre", img_dark),
    ("Trop clair", img_bright),
    ("Faible contraste", img_low_contrast)
]


# ===== EVALUER ET AFFICHER =====
print("\n" + "=" * 70)
print("EVALUATION DES IMAGES DEGRADEES")
print("=" * 70)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for i, (label, img) in enumerate(images_test):
    # Evaluer
    result = qa.evaluate(img)
    
    # Afficher resultats dans terminal
    print(f"\n--- {label} ---")
    print(f"Nettete:    {result['sharpness']['score']:6.1f}/100")
    print(f"Luminosite: {result['brightness']['score']:6.1f}/100")
    print(f"Contraste:  {result['contrast']['score']:6.1f}/100")
    print(f"GLOBAL:     {result['global_score']:6.1f}/100  ->  {result['decision']}")
    
    # Choisir couleur
    if result['decision'] == 'ACCEPTABLE':
        color = 'green'
    elif result['decision'] == 'MOYENNE':
        color = 'orange'
    else:
        color = 'red'
    
    # Afficher image avec scores
    axes[i].imshow(img, cmap='gray')
    
    title = f"{label}\n"
    title += f"{result['decision']} - Score: {result['global_score']:.1f}/100\n"
    title += f"Net: {result['sharpness']['score']:.0f} | "
    title += f"Lum: {result['brightness']['score']:.0f} | "
    title += f"Con: {result['contrast']['score']:.0f}"
    
    axes[i].set_title(title, color=color, fontweight='bold', fontsize=11)
    axes[i].axis('off')

plt.suptitle("Test du module Quality Assessment sur images degradees", 
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('models/quality_test_degraded.png', dpi=100, bbox_inches='tight')
plt.show()

print("\n" + "=" * 70)
print("Test termine! Image sauvegardee: models/quality_test_degraded.png")
print("=" * 70)