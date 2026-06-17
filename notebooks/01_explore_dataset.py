"""
Script 01: Exploration du dataset
Objectif: Comprendre nos donnees avant de faire l'IA
"""

import os
from PIL import Image
import matplotlib.pyplot as plt
import random

# ===== CONFIGURATION =====
# Chemin vers le dataset (depuis la racine du projet)
DATASET_PATH = "data/chest_xray"

# Les 3 dossiers principaux
SETS = ["train", "val", "test"]

# Les 2 categories
CATEGORIES = ["NORMAL", "PNEUMONIA"]


# ===== ETAPE 1: Compter les images =====
print("=" * 60)
print("ETAPE 1: Compter les images dans chaque dossier")
print("=" * 60)

total_images = 0

for set_name in SETS:
    print(f"\n--- Dossier: {set_name} ---")
    
    for category in CATEGORIES:
        folder_path = os.path.join(DATASET_PATH, set_name, category)
        
        # Lister tous les fichiers (.jpeg, .jpg, .png)
        if os.path.exists(folder_path):
            images = [f for f in os.listdir(folder_path) 
                     if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
            count = len(images)
            total_images += count
            print(f"  {category}: {count} images")
        else:
            print(f"  {category}: DOSSIER INTROUVABLE!")

print(f"\nTOTAL: {total_images} images dans tout le dataset")


# ===== ETAPE 2: Analyser une image =====
print("\n" + "=" * 60)
print("ETAPE 2: Analyser une image (proprietes)")
print("=" * 60)

# Prendre la 1ere image du dossier train/NORMAL
sample_folder = os.path.join(DATASET_PATH, "train", "NORMAL")
sample_files = os.listdir(sample_folder)
sample_image_path = os.path.join(sample_folder, sample_files[0])

print(f"\nImage analysee: {sample_files[0]}")

img = Image.open(sample_image_path)
print(f"Format: {img.format}")
print(f"Mode: {img.mode}")
print(f"Taille: {img.size} pixels (largeur x hauteur)")


# ===== ETAPE 3: Afficher des exemples =====
print("\n" + "=" * 60)
print("ETAPE 3: Afficher 4 radiographies")
print("=" * 60)

# Choisir aleatoirement 2 NORMAL et 2 PNEUMONIA
def get_random_images(category, n=2):
    folder = os.path.join(DATASET_PATH, "train", category)
    files = os.listdir(folder)
    selected = random.sample(files, n)
    return [os.path.join(folder, f) for f in selected]

normal_images = get_random_images("NORMAL", 2)
pneumonia_images = get_random_images("PNEUMONIA", 2)

# Creer une figure 2x2
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Exemples de radiographies thoraciques", fontsize=16, fontweight='bold')

# Ligne 1: NORMAL
for i, img_path in enumerate(normal_images):
    img = Image.open(img_path)
    axes[0, i].imshow(img, cmap='gray')
    axes[0, i].set_title("NORMAL (sain)", color='green', fontweight='bold')
    axes[0, i].axis('off')

# Ligne 2: PNEUMONIA
for i, img_path in enumerate(pneumonia_images):
    img = Image.open(img_path)
    axes[1, i].imshow(img, cmap='gray')
    axes[1, i].set_title("PNEUMONIA (malade)", color='red', fontweight='bold')
    axes[1, i].axis('off')

plt.tight_layout()
plt.show()

print("\nFin du script!")