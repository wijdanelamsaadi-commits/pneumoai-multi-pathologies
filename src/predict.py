"""
Script de prediction
Utiliser le modele entraine pour predire sur de nouvelles images
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import random

# ===== CONFIGURATION =====
MODEL_PATH = "models/pneumonia_model.keras"
TEST_PATH = "data/chest_xray/test"
IMAGE_SIZE = 224

# ===== CHARGER LE MODELE =====
print("Chargement du modele...")
model = load_model(MODEL_PATH)
print("Modele charge avec succes!")


# ===== FONCTION DE PREDICTION =====
def predict_image(image_path):
    """Predire si une image est NORMAL ou PNEUMONIA"""
    
    # Charger et preprocesser
    img = Image.open(image_path).convert('RGB')
    img_resized = img.resize((IMAGE_SIZE, IMAGE_SIZE))
    img_array = np.array(img_resized) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)
    
    # Prediction
    prediction = model.predict(img_batch, verbose=0)
    probability = float(prediction[0][0])
    
    # Interpreter (0 = NORMAL, 1 = PNEUMONIA)
    if probability >= 0.5:
        diagnosis = "PNEUMONIA"
        confidence = probability * 100
    else:
        diagnosis = "NORMAL"
        confidence = (1 - probability) * 100
    
    return img, diagnosis, confidence, probability


# ===== TESTER SUR PLUSIEURS IMAGES =====
print("\n" + "=" * 60)
print("TEST: Prediction sur 6 images aleatoires")
print("=" * 60)

# Choisir 3 NORMAL et 3 PNEUMONIA
normal_files = os.listdir(os.path.join(TEST_PATH, "NORMAL"))
pneumonia_files = os.listdir(os.path.join(TEST_PATH, "PNEUMONIA"))

selected_images = []

# 3 images NORMAL aleatoires
for f in random.sample(normal_files, 3):
    selected_images.append({
        'path': os.path.join(TEST_PATH, "NORMAL", f),
        'true_label': 'NORMAL'
    })

# 3 images PNEUMONIA aleatoires
for f in random.sample(pneumonia_files, 3):
    selected_images.append({
        'path': os.path.join(TEST_PATH, "PNEUMONIA", f),
        'true_label': 'PNEUMONIA'
    })

# Afficher les predictions
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

correct = 0
for i, item in enumerate(selected_images):
    img, predicted, confidence, prob = predict_image(item['path'])
    
    is_correct = (predicted == item['true_label'])
    if is_correct:
        correct += 1
    
    color = 'green' if is_correct else 'red'
    symbol = '✓' if is_correct else '✗'
    
    title = f"Vrai: {item['true_label']}\n"
    title += f"Predit: {predicted} ({confidence:.1f}%) {symbol}"
    
    axes[i].imshow(img, cmap='gray')
    axes[i].set_title(title, color=color, fontweight='bold')
    axes[i].axis('off')
    
    print(f"\nImage {i+1}: {os.path.basename(item['path'])}")
    print(f"  Vrai diagnostic: {item['true_label']}")
    print(f"  Prediction: {predicted}")
    print(f"  Confiance: {confidence:.2f}%")
    print(f"  Probabilite brute: {prob:.4f}")
    print(f"  Resultat: {'CORRECT' if is_correct else 'INCORRECT'}")

print(f"\n{'=' * 60}")
print(f"BILAN: {correct}/6 predictions correctes ({correct/6*100:.0f}%)")
print(f"{'=' * 60}")

plt.suptitle("Predictions du modele sur des images de test", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()