"""
Download/extract and prepare a reduced CheXpert-small dataset.

This script intentionally accepts only CheXpert-v1.0-small. It filters labels to:
- Pneumonia
- Consolidation
- Pleural Effusion

Output:
- data/chexpert-small-reduced/train_reduced.csv
- data/chexpert-small-reduced/valid_reduced.csv
"""

import argparse
import shutil
import subprocess
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd


LABEL_COLUMNS = ["Pneumonia", "Consolidation", "Pleural Effusion"]
DEFAULT_SOURCE_DIR = Path("data/CheXpert-v1.0-small")
DEFAULT_OUTPUT_DIR = Path("data/chexpert-small-reduced")


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare a reduced CheXpert-small dataset for PneumoAI V2.")
    parser.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR), help="Existing CheXpert-v1.0-small folder.")
    parser.add_argument("--archive", default="", help="Path to CheXpert-v1.0-small.zip if already downloaded.")
    parser.add_argument("--url", default="", help="Authorized direct download URL for CheXpert-v1.0-small.zip.")
    parser.add_argument(
        "--kaggle-slug",
        default="ashery/chexpert",
        help="Kaggle dataset slug for CheXpert-v1.0-small. Requires local Kaggle credentials.",
    )
    parser.add_argument("--download-dir", default="data", help="Where downloads/extractions are placed.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Prepared reduced dataset folder.")
    parser.add_argument("--max-train", type=int, default=12000, help="Maximum train rows in the reduced CSV.")
    parser.add_argument("--max-valid", type=int, default=1000, help="Maximum validation/evaluation rows.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--uncertain-policy",
        choices=["zero", "one"],
        default="zero",
        help="How uncertain labels (-1) are mapped.",
    )
    parser.add_argument(
        "--include-lateral",
        action="store_true",
        help="Include lateral views. Default keeps only frontal images when metadata is available.",
    )
    return parser.parse_args()


def assert_small_only(path: Path):
    normalized = path.name.lower()
    full_names = {"chexpert-v1.0", "chexpert-v1.0.zip"}
    if normalized in full_names or ("chexpert-v1.0" in normalized and "small" not in normalized):
        raise ValueError(
            "Refusing to use the full CheXpert dataset. Provide CheXpert-v1.0-small only."
        )


def download_with_url(url: str, download_dir: Path) -> Path:
    archive_path = download_dir / "CheXpert-v1.0-small.zip"
    print(f"Downloading CheXpert-small to {archive_path}...")
    urlretrieve(url, archive_path)
    return archive_path


def download_with_kaggle(slug: str, download_dir: Path) -> Path:
    kaggle_exe = shutil.which("kaggle")
    if not kaggle_exe:
        raise RuntimeError(
            "Kaggle CLI is not installed/configured. Provide --archive or --url after accepting the dataset terms."
        )

    print(f"Downloading Kaggle dataset {slug} into {download_dir}...")
    subprocess.run(
        [kaggle_exe, "datasets", "download", "-d", slug, "-p", str(download_dir)],
        check=True,
    )
    archives = sorted(download_dir.glob("*.zip"), key=lambda item: item.stat().st_mtime, reverse=True)
    if not archives:
        raise FileNotFoundError("Kaggle download completed but no zip archive was found.")
    return archives[0]


def extract_archive(archive_path: Path, download_dir: Path) -> Path:
    assert_small_only(archive_path)
    print(f"Extracting {archive_path}...")
    with zipfile.ZipFile(archive_path) as archive:
        small_members = [name for name in archive.namelist() if "CheXpert-v1.0-small/" in name]
        if not small_members:
            raise ValueError("Archive does not contain CheXpert-v1.0-small. Refusing to continue.")
        archive.extractall(download_dir)
    return find_small_dir(download_dir)


def find_small_dir(root: Path) -> Path:
    candidates = [root / "CheXpert-v1.0-small", *root.rglob("CheXpert-v1.0-small")]
    for candidate in candidates:
        if (candidate / "train.csv").exists() and (candidate / "valid.csv").exists():
            return candidate
    raise FileNotFoundError("Could not find CheXpert-v1.0-small with train.csv and valid.csv.")


def ensure_source(args) -> Path:
    source_dir = Path(args.source_dir)
    download_dir = Path(args.download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)

    if source_dir.exists():
        assert_small_only(source_dir)
        return source_dir

    archive = Path(args.archive) if args.archive else None
    if archive and archive.exists():
        return extract_archive(archive, download_dir)

    if args.url:
        archive = download_with_url(args.url, download_dir)
        return extract_archive(archive, download_dir)

    archive = download_with_kaggle(args.kaggle_slug, download_dir)
    return extract_archive(archive, download_dir)


def resolve_image_path(source_dir: Path, value: str) -> str:
    raw = Path(str(value).replace("/", "\\"))
    candidates = [
        source_dir / raw,
        source_dir.parent / raw,
        raw,
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate.resolve())
    return str((source_dir / raw).resolve())


def reduce_split(source_dir: Path, csv_name: str, max_rows: int, args) -> pd.DataFrame:
    csv_path = source_dir / csv_name
    df = pd.read_csv(csv_path)
    required = ["Path", *LABEL_COLUMNS]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"{csv_path} is missing required columns: {missing}")

    if not args.include_lateral and "Frontal/Lateral" in df.columns:
        df = df[df["Frontal/Lateral"].astype(str).str.lower() == "frontal"].copy()

    labels = df[LABEL_COLUMNS].fillna(0).replace(-1, 1 if args.uncertain_policy == "one" else 0)
    labels = labels.clip(lower=0, upper=1).astype("int8")

    reduced = pd.DataFrame(
        {
            "image_path": [resolve_image_path(source_dir, value) for value in df["Path"]],
            "source_path": df["Path"].astype(str).values,
        }
    )
    for column in LABEL_COLUMNS:
        reduced[column] = labels[column].values

    existing = reduced["image_path"].map(lambda value: Path(value).exists())
    skipped = int((~existing).sum())
    if skipped:
        print(f"Warning: skipped {skipped} rows with missing images from {csv_name}.")
    reduced = reduced[existing].reset_index(drop=True)

    if max_rows and len(reduced) > max_rows:
        positives = []
        quota = max(1, max_rows // (len(LABEL_COLUMNS) + 1))
        for column in LABEL_COLUMNS:
            positives.append(reduced[reduced[column] == 1].sample(min(quota, int((reduced[column] == 1).sum())), random_state=args.seed))
        normal_like = reduced[reduced[LABEL_COLUMNS].sum(axis=1) == 0]
        if not normal_like.empty:
            positives.append(normal_like.sample(min(quota, len(normal_like)), random_state=args.seed))
        sampled = pd.concat(positives, ignore_index=False).drop_duplicates()
        remaining = max_rows - len(sampled)
        if remaining > 0:
            pool = reduced.drop(index=sampled.index, errors="ignore")
            sampled = pd.concat(
                [sampled, pool.sample(min(remaining, len(pool)), random_state=args.seed)],
                ignore_index=False,
            )
        reduced = sampled.sample(frac=1, random_state=args.seed).reset_index(drop=True)

    return reduced


def write_split(df: pd.DataFrame, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Wrote {len(df)} rows: {output_path}")
    print(df[LABEL_COLUMNS].mean().round(4).to_string())


def main():
    args = parse_args()
    source_dir = ensure_source(args)
    assert_small_only(source_dir)
    output_dir = Path(args.output_dir)

    print("=" * 70)
    print("Preparing reduced CheXpert-small dataset")
    print("=" * 70)
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    print(f"Labels: {', '.join(LABEL_COLUMNS)}")

    train_df = reduce_split(source_dir, "train.csv", args.max_train, args)
    valid_df = reduce_split(source_dir, "valid.csv", args.max_valid, args)

    write_split(train_df, output_dir / "train_reduced.csv")
    write_split(valid_df, output_dir / "valid_reduced.csv")

    metadata = output_dir / "README.md"
    metadata.write_text(
        "\n".join(
            [
                "# Reduced CheXpert-small dataset",
                "",
                "Source dataset: CheXpert-v1.0-small only.",
                "Labels: Pneumonia, Consolidation, Pleural Effusion.",
                "Problem type: multi-label.",
                "Normal is not a trained label; it is derived from low probabilities.",
                f"Train rows: {len(train_df)}",
                f"Validation/evaluation rows: {len(valid_df)}",
                f"Uncertain policy: {args.uncertain_policy}",
                f"Frontal only: {not args.include_lateral}",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote metadata: {metadata}")


if __name__ == "__main__":
    main()
