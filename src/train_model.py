"""
Script principal: Entrainement du modele de detection de pneumonie
Architecture: Transfer Learning avec MobileNetV2 (rapide sur CPU)
"""

import os
# Reduire les warnings TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt

# ===== CONFIGURATION =====
DATASET_PATH = "data/chest_xray"
IMAGE_SIZE = 224           # Taille des images en entree
BATCH_SIZE = 32            # Nombre d'images par lot
EPOCHS = 5                # Nombre de passages sur le dataset
LEARNING_RATE = 0.0001     # Vitesse d'apprentissage

print("=" * 60)
print("ENTRAINEMENT DU MODELE DE DETECTION DE PNEUMONIE")
print("=" * 60)
print(f"\nConfiguration:")
print(f"  - Taille images: {IMAGE_SIZE}x{IMAGE_SIZE}")
print(f"  - Batch size: {BATCH_SIZE}")
print(f"  - Epochs: {EPOCHS}")
print(f"  - Learning rate: {LEARNING_RATE}")


# ===== ETAPE 1: Charger les donnees =====
print("\n" + "=" * 60)
print("ETAPE 1: Chargement des donnees")
print("=" * 60)

# Generateur pour les donnees d'entrainement (avec augmentation)
train_datagen = ImageDataGenerator(
    rescale=1./255,              # Normalisation 0-1
    rotation_range=10,           # Rotation aleatoire
    width_shift_range=0.1,       # Decalage horizontal
    height_shift_range=0.1,      # Decalage vertical
    horizontal_flip=True,        # Retournement horizontal
    zoom_range=0.1               # Zoom aleatoire
)

# Generateur pour test/val (sans augmentation, juste normalisation)
val_test_datagen = ImageDataGenerator(rescale=1./255)

# Charger train
train_generator = train_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'train'),
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=True
)

# Charger validation
val_generator = val_test_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'val'),
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

# Charger test
test_generator = val_test_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'test'),
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

print(f"\nClasses detectees: {train_generator.class_indices}")


# ===== ETAPE 2: Construire le modele =====
print("\n" + "=" * 60)
print("ETAPE 2: Construction du modele (Transfer Learning)")
print("=" * 60)

# Charger MobileNetV2 pre-entraine sur ImageNet
base_model = MobileNetV2(
    input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
    include_top=False,           # Sans la couche finale d'ImageNet
    weights='imagenet'           # Poids pre-entraines
)

# Geler les couches du modele de base (ne pas re-entrainer)
base_model.trainable = False

# Ajouter nos propres couches
inputs = base_model.input
x = base_model.output
x = GlobalAveragePooling2D()(x)              # Reduire les dimensions
x = Dense(128, activation='relu')(x)          # Couche cachee
x = Dropout(0.5)(x)                           # Regularisation (anti-overfitting)
outputs = Dense(1, activation='sigmoid')(x)   # Sortie binaire (0 ou 1)

model = Model(inputs=inputs, outputs=outputs)

# Compiler le modele
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("\nModele cree avec succes!")
print(f"Nombre total de parametres: {model.count_params():,}")
print(f"Parametres entrainables: {sum([tf.size(v).numpy() for v in model.trainable_variables]):,}")


# ===== ETAPE 3: Entrainement =====
print("\n" + "=" * 60)
print("ETAPE 3: Entrainement du modele")
print("=" * 60)
print("\nC'est parti! Cela peut prendre 30-60 minutes sur CPU...")
print("(prends un cafe!)\n")

# Callbacks
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True,
    verbose=1
)

checkpoint = ModelCheckpoint(
    'models/best_model.keras',
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

# Lancer l'entrainement!
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    callbacks=[early_stopping, checkpoint],
    verbose=1
)


# ===== ETAPE 4: Evaluation =====
print("\n" + "=" * 60)
print("ETAPE 4: Evaluation sur les donnees de test")
print("=" * 60)

test_loss, test_accuracy = model.evaluate(test_generator, verbose=1)
print(f"\nResultats sur le test set:")
print(f"  - Loss: {test_loss:.4f}")
print(f"  - Accuracy: {test_accuracy*100:.2f}%")


# ===== ETAPE 5: Sauvegarder le modele =====
print("\n" + "=" * 60)
print("ETAPE 5: Sauvegarde du modele")
print("=" * 60)

model.save('models/pneumonia_model.keras')
print("Modele sauvegarde dans: models/pneumonia_model.keras")


# ===== ETAPE 6: Visualiser les resultats =====
print("\n" + "=" * 60)
print("ETAPE 6: Visualisation de l'entrainement")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Graphique de l'accuracy
axes[0].plot(history.history['accuracy'], label='Train', color='blue')
axes[0].plot(history.history['val_accuracy'], label='Validation', color='orange')
axes[0].set_title('Accuracy au fil des epochs')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

# Graphique de la loss
axes[1].plot(history.history['loss'], label='Train', color='blue')
axes[1].plot(history.history['val_loss'], label='Validation', color='orange')
axes[1].set_title('Loss au fil des epochs')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig('models/training_history.png')
plt.show()

print("\nGraphique sauvegarde: models/training_history.png")
print("\n" + "=" * 60)
print("ENTRAINEMENT TERMINE!")
print("=" * 60)