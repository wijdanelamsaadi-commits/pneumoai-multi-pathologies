"""
Script 03: Tester TensorFlow
Objectif: Verifier que tout fonctionne avant d'entrainer l'IA
"""

import tensorflow as tf
import numpy as np

print("=" * 60)
print("TEST DE TENSORFLOW")
print("=" * 60)

# ===== Version =====
print(f"\nVersion TensorFlow: {tf.__version__}")
print(f"Version Keras: {tf.keras.__version__}")

# ===== GPU disponible? =====
print("\n--- Verification du GPU ---")
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"GPU detecte: {len(gpus)} GPU(s)")
    for gpu in gpus:
        print(f"  - {gpu}")
else:
    print("Pas de GPU detecte - on utilisera le CPU")
    print("(plus lent mais ca marche tres bien pour apprendre)")

# ===== Test simple: addition de tenseurs =====
print("\n--- Test 1: Operations mathematiques ---")
a = tf.constant([1, 2, 3])
b = tf.constant([4, 5, 6])
c = a + b
print(f"a = {a.numpy()}")
print(f"b = {b.numpy()}")
print(f"a + b = {c.numpy()}")

# ===== Test: creer un mini reseau de neurones =====
print("\n--- Test 2: Creation d'un mini reseau de neurones ---")
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(5,)),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

print("Mini reseau cree avec succes!")
print(f"Nombre de couches: {len(model.layers)}")
print(f"Nombre de parametres: {model.count_params()}")

# Afficher la structure
print("\n--- Structure du reseau ---")
model.summary()

# ===== Test: faire une prediction =====
print("\n--- Test 3: Prediction sur donnees fictives ---")
donnees_test = np.random.random((1, 5))
print(f"Donnees d'entree: {donnees_test[0]}")

prediction = model.predict(donnees_test, verbose=0)
print(f"Prediction (avant entrainement): {prediction[0][0]:.4f}")
print("(la prediction est aleatoire car le modele n'est pas entraine)")

print("\n" + "=" * 60)
print("TENSORFLOW FONCTIONNE PARFAITEMENT!")
print("ON EST PRET A ENTRAINER NOTRE IA!")
print("=" * 60)