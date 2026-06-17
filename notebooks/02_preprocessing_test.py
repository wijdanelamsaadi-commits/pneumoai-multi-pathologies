"""
Script 02: Test du preprocessing
Objectif: Apprendre comment preparer les images pour l'IA
"""

import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# ===== CONFIGURATION =====
IMAGE_SIZE = 224  # Taille standard pour l'IA (224x224 pixels)
SAMPLE_PATH = "data/chest_xray/train/PNEUMONIA"


# ===== ETAPE 1: Charger une image =====
print("=" * 60)
print("ETAPE 1: Charger une image")
print("=" * 60)

# Prendre la 1ere image
sample_files = os.listdir(SAMPLE_PATH)
image_path = os.path.join(SAMPLE_PATH, sample_files[0])

print(f"Image: {sample_files[0]}")

original_img = Image.open(image_path)
print(f"Taille originale: {original_img.size}")
print(f"Mode: {original_img.mode}")


# ===== ETAPE 2: Convertir en RGB =====
# Important: certaines images sont en niveaux de gris (mode 'L')
# L'IA prefere souvent du RGB (3 canaux)
print("\n" + "=" * 60)
print("ETAPE 2: Conversion en RGB")
print("=" * 60)

img_rgb = original_img.convert('RGB')
print(f"Mode apres conversion: {img_rgb.mode}")


# ===== ETAPE 3: Redimensionner =====
print("\n" + "=" * 60)
print("ETAPE 3: Redimensionner")
print("=" * 60)

img_resized = img_rgb.resize((IMAGE_SIZE, IMAGE_SIZE))
print(f"Nouvelle taille: {img_resized.size}")


# ===== ETAPE 4: Convertir en tableau NumPy =====
print("\n" + "=" * 60)
print("ETAPE 4: Conversion en tableau NumPy")
print("=" * 60)

img_array = np.array(img_resized)
print(f"Shape: {img_array.shape}")
print(f"Type: {img_array.dtype}")
print(f"Valeur min: {img_array.min()}")
print(f"Valeur max: {img_array.max()}")


# ===== ETAPE 5: Normalisation (0-255 -> 0-1) =====
print("\n" + "=" * 60)
print("ETAPE 5: Normalisation")
print("=" * 60)

img_normalized = img_array.astype('float32') / 255.0
print(f"Shape: {img_normalized.shape}")
print(f"Type: {img_normalized.dtype}")
print(f"Valeur min: {img_normalized.min():.4f}")
print(f"Valeur max: {img_normalized.max():.4f}")

print("\nL'image est prete pour l'IA!")


# ===== ETAPE 6: Visualiser les transformations =====
print("\n" + "=" * 60)
print("ETAPE 6: Visualisation")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Originale
axes[0].imshow(original_img, cmap='gray')
axes[0].set_title(f"Original\n{original_img.size}", fontweight='bold')
axes[0].axis('off')

# Redimensionnee
axes[1].imshow(img_resized)
axes[1].set_title(f"Redimensionnee\n{IMAGE_SIZE}x{IMAGE_SIZE}", fontweight='bold')
axes[1].axis('off')

# Normalisee
axes[2].imshow(img_normalized)
axes[2].set_title(f"Normalisee (0-1)\nPrete pour l'IA", fontweight='bold')
axes[2].axis('off')

plt.suptitle("Pipeline de preprocessing", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print("\nFin du script!")