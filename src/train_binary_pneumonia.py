"""
Binary PneumoAI training pipeline.

Dataset expected:
data/chest_xray/
  train/NORMAL
  train/PNEUMONIA
  val/NORMAL
  val/PNEUMONIA
  test/NORMAL
  test/PNEUMONIA

Output:
models/pneumonia_binary.keras
models/binary_metrics.csv
"""

import argparse
import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def parse_args():
    parser = argparse.ArgumentParser(description="Train binary Pneumonia/Normal MobileNetV2 model.")
    parser.add_argument("--data-dir", default="data/chest_xray")
    parser.add_argument("--output-model", default="models/pneumonia_binary.keras")
    parser.add_argument("--metrics-output", default="models/binary_metrics.csv")
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--fine-tune-epochs", type=int, default=8)
    parser.add_argument("--fine-tune-learning-rate", type=float, default=1e-5)
    parser.add_argument("--fine-tune-from", type=int, default=100)
    return parser.parse_args()


def make_generators(args):
    data_dir = Path(args.data_dir)
    required = [
        data_dir / "train" / "NORMAL",
        data_dir / "train" / "PNEUMONIA",
        data_dir / "val" / "NORMAL",
        data_dir / "val" / "PNEUMONIA",
        data_dir / "test" / "NORMAL",
        data_dir / "test" / "PNEUMONIA",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing dataset folders:\n" + "\n".join(missing))

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=12,
        width_shift_range=0.08,
        height_shift_range=0.08,
        zoom_range=0.12,
        horizontal_flip=True,
        fill_mode="nearest",
    )
    eval_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    common = {
        "target_size": (args.image_size, args.image_size),
        "batch_size": args.batch_size,
        "class_mode": "binary",
    }
    train_gen = train_datagen.flow_from_directory(data_dir / "train", shuffle=True, **common)
    val_gen = eval_datagen.flow_from_directory(data_dir / "val", shuffle=False, **common)
    test_gen = eval_datagen.flow_from_directory(data_dir / "test", shuffle=False, **common)
    return train_gen, val_gen, test_gen


def build_model(args):
    base_model = MobileNetV2(
        input_shape=(args.image_size, args.image_size, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.45)(x)
    outputs = Dense(1, activation="sigmoid")(x)

    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=args.learning_rate),
        loss="binary_crossentropy",
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="accuracy"),
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
            tf.keras.metrics.AUC(name="auc"),
        ],
    )
    return model, base_model


def class_weights_from_generator(train_gen):
    labels = train_gen.classes
    total = len(labels)
    counts = np.bincount(labels)
    return {index: total / (len(counts) * count) for index, count in enumerate(counts)}


def evaluate(model, generator):
    generator.reset()
    y_true = generator.classes
    y_prob = model.predict(generator, verbose=1).ravel()
    y_pred = (y_prob >= 0.5).astype("int32")

    return pd.DataFrame(
        [
            {
                "accuracy": accuracy_score(y_true, y_pred),
                "precision": precision_score(y_true, y_pred, zero_division=0),
                "recall": recall_score(y_true, y_pred, zero_division=0),
                "f1": f1_score(y_true, y_pred, zero_division=0),
                "auc": roc_auc_score(y_true, y_prob),
                "threshold": 0.5,
            }
        ]
    )


def main():
    args = parse_args()
    Path(args.output_model).parent.mkdir(parents=True, exist_ok=True)
    Path(args.metrics_output).parent.mkdir(parents=True, exist_ok=True)

    train_gen, val_gen, test_gen = make_generators(args)
    print("Class indices:", train_gen.class_indices)

    model, base_model = build_model(args)
    callbacks = [
        EarlyStopping(monitor="val_auc", mode="max", patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=2, min_lr=1e-7),
        ModelCheckpoint(args.output_model, monitor="val_auc", mode="max", save_best_only=True),
    ]

    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.epochs,
        class_weight=class_weights_from_generator(train_gen),
        callbacks=callbacks,
    )

    for layer in base_model.layers[: args.fine_tune_from]:
        layer.trainable = False
    for layer in base_model.layers[args.fine_tune_from :]:
        layer.trainable = True

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=args.fine_tune_learning_rate),
        loss="binary_crossentropy",
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="accuracy"),
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
            tf.keras.metrics.AUC(name="auc"),
        ],
    )
    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.fine_tune_epochs,
        class_weight=class_weights_from_generator(train_gen),
        callbacks=callbacks,
    )

    best_model = tf.keras.models.load_model(args.output_model)
    metrics = evaluate(best_model, test_gen)
    metrics.to_csv(args.metrics_output, index=False)
    print(metrics.to_string(index=False))
    print(f"Saved model: {args.output_model}")
    print(f"Saved metrics: {args.metrics_output}")


if __name__ == "__main__":
    main()
