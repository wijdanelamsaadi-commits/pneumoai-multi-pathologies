"""
Training pipeline V2 for CheXpert-small multi-label chest X-ray detection.

Targets:
- Pneumonia
- Consolidation
- Pleural Effusion

The output layer is Dense(3, activation="sigmoid") and the model is saved to:
models/multilabel_mobilenetv2.keras
"""

import argparse
import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model


LABEL_COLUMNS = ["Pneumonia", "Consolidation", "Pleural Effusion"]
DEFAULT_MODEL_PATH = "models/multilabel_mobilenetv2.keras"


def parse_args():
    parser = argparse.ArgumentParser(description="Train MobileNetV2 on CheXpert-small multi-label targets.")
    parser.add_argument(
        "--data-dir",
        default="data/chexpert-small-reduced",
        help="Prepared reduced CheXpert-small directory containing train_reduced.csv and valid_reduced.csv.",
    )
    parser.add_argument("--output", default=DEFAULT_MODEL_PATH, help="Output .keras model path.")
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument(
        "--uncertain-policy",
        choices=["zero", "one"],
        default="zero",
        help="How CheXpert uncertain labels (-1) are mapped for the selected labels.",
    )
    parser.add_argument(
        "--fine-tune-at",
        type=int,
        default=120,
        help="Unfreeze MobileNetV2 layers from this index after the frozen warmup. Use -1 to skip fine-tuning.",
    )
    parser.add_argument("--fine-tune-epochs", type=int, default=3)
    return parser.parse_args()


def resolve_image_path(data_dir: Path, csv_path: str) -> str:
    raw_path = Path(str(csv_path).replace("/", os.sep))
    candidates = [
        data_dir / raw_path,
        data_dir.parent / raw_path,
        raw_path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(candidates[0])


def split_csv_path(data_dir: Path, csv_name: str) -> Path:
    prepared_names = {
        "train.csv": "train_reduced.csv",
        "valid.csv": "valid_reduced.csv",
    }
    prepared_path = data_dir / prepared_names.get(csv_name, csv_name)
    if prepared_path.exists():
        return prepared_path
    return data_dir / csv_name


def load_split(data_dir: Path, csv_name: str, uncertain_policy: str) -> pd.DataFrame:
    csv_path = split_csv_path(data_dir, csv_name)
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CheXpert CSV: {csv_path}")

    df = pd.read_csv(csv_path)
    path_column = "image_path" if "image_path" in df.columns else "Path"
    missing = [column for column in [path_column, *LABEL_COLUMNS] if column not in df.columns]
    if missing:
        raise ValueError(f"{csv_path} is missing required columns: {missing}")

    labels = df[LABEL_COLUMNS].copy()
    labels = labels.fillna(0)
    labels = labels.replace(-1, 1 if uncertain_policy == "one" else 0)
    labels = labels.clip(lower=0, upper=1).astype("float32")

    clean = pd.DataFrame(
        {
            "image_path": [
                str(Path(value)) if path_column == "image_path" else resolve_image_path(data_dir, value)
                for value in df[path_column]
            ],
        }
    )
    for column in LABEL_COLUMNS:
        clean[column] = labels[column].values

    existing = clean["image_path"].map(lambda value: Path(value).exists())
    missing_count = int((~existing).sum())
    if missing_count:
        print(f"Warning: {missing_count} image paths from {csv_name} do not exist and will be skipped.")
    return clean[existing].reset_index(drop=True)


def make_dataset(df: pd.DataFrame, image_size: int, batch_size: int, training: bool) -> tf.data.Dataset:
    paths = df["image_path"].values
    labels = df[LABEL_COLUMNS].values.astype("float32")
    dataset = tf.data.Dataset.from_tensor_slices((paths, labels))

    if training:
        dataset = dataset.shuffle(buffer_size=min(len(df), 4096), reshuffle_each_iteration=True)

    def load_image(path, label):
        image_bytes = tf.io.read_file(path)
        image = tf.io.decode_image(image_bytes, channels=3, expand_animations=False)
        image = tf.image.resize(image, (image_size, image_size))
        image = tf.cast(image, tf.float32)
        image = preprocess_input(image)
        return image, label

    dataset = dataset.map(load_image, num_parallel_calls=tf.data.AUTOTUNE)

    if training:
        augmentation = tf.keras.Sequential(
            [
                tf.keras.layers.RandomFlip("horizontal"),
                tf.keras.layers.RandomRotation(0.03),
                tf.keras.layers.RandomZoom(0.05),
            ],
            name="augmentation",
        )
        dataset = dataset.map(
            lambda image, label: (augmentation(image, training=True), label),
            num_parallel_calls=tf.data.AUTOTUNE,
        )

    return dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)


def build_model(image_size: int, learning_rate: float) -> Model:
    base_model = MobileNetV2(
        input_shape=(image_size, image_size, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(image_size, image_size, 3))
    x = base_model(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.4)(x)
    outputs = Dense(3, activation="sigmoid", name="pathology_probabilities")(x)

    model = Model(inputs=inputs, outputs=outputs, name="chexpert_multilabel_mobilenetv2")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="binary_accuracy", threshold=0.5),
            tf.keras.metrics.AUC(name="auc", multi_label=True, num_labels=3),
        ],
    )
    return model


def fine_tune(model: Model, fine_tune_at: int, learning_rate: float):
    if fine_tune_at < 0:
        return

    base_model = next((layer for layer in model.layers if isinstance(layer, tf.keras.Model)), None)
    if base_model is None:
        return

    base_model.trainable = True
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate / 10),
        loss="binary_crossentropy",
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="binary_accuracy", threshold=0.5),
            tf.keras.metrics.AUC(name="auc", multi_label=True, num_labels=3),
        ],
    )


def main():
    args = parse_args()
    data_dir = Path(args.data_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("PneumoAI V2 - CheXpert-small multi-label training")
    print("=" * 70)
    print(f"Dataset: {data_dir}")
    print(f"Labels: {', '.join(LABEL_COLUMNS)}")
    print(f"Output: {output_path}")

    train_df = load_split(data_dir, "train.csv", args.uncertain_policy)
    val_df = load_split(data_dir, "valid.csv", args.uncertain_policy)
    print(f"Train images: {len(train_df)}")
    print(f"Validation images: {len(val_df)}")
    print("Positive rates:")
    print(train_df[LABEL_COLUMNS].mean().round(4))

    train_ds = make_dataset(train_df, args.image_size, args.batch_size, training=True)
    val_ds = make_dataset(val_df, args.image_size, args.batch_size, training=False)

    model = build_model(args.image_size, args.learning_rate)
    model.summary()

    callbacks = [
        ModelCheckpoint(str(output_path), monitor="val_auc", mode="max", save_best_only=True, verbose=1),
        EarlyStopping(monitor="val_auc", mode="max", patience=4, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=2, min_lr=1e-7, verbose=1),
    ]

    model.fit(train_ds, validation_data=val_ds, epochs=args.epochs, callbacks=callbacks)

    if args.fine_tune_at >= 0 and args.fine_tune_epochs > 0:
        print("\nFine-tuning MobileNetV2...")
        fine_tune(model, args.fine_tune_at, args.learning_rate)
        model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=args.fine_tune_epochs,
            callbacks=callbacks,
        )

    model.save(str(output_path))
    print(f"\nV2 model saved: {output_path}")


if __name__ == "__main__":
    main()
