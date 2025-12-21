"""Data ingestion script for the Watt About It project.

Loads a CSV sample, validates its structure, and uploads it to the configured
cloud data lake (AWS S3 by default) while emitting structured logs.
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd
from botocore.exceptions import ClientError

try:
    import boto3
except ImportError as exc:  # pragma: no cover - boto3 should be installed in runtime
    raise RuntimeError("boto3 is required to run the ingestion script.") from exc

try:  # Optional quality-of-life feature; falls back silently if package is absent.
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

EXPECTED_SCHEMA: Dict[str, str] = {
    "record_id": "string",
    "customer_id": "string",
    "meter_id": "string",
    "reading_ts": "datetime",
    "consumption_kwh": "float",
    "tariff_eur_kwh": "float",
    "is_peak": "bool",
}

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT_ROOT / "data" / "samples" / "sample_energy_consumption.csv"
LOG_DIR = PROJECT_ROOT / "logs"


@dataclass(frozen=True)
class ValidationResult:
    missing_columns: List[str]
    extra_columns: List[str]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest CSV data into the cloud data lake.")
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Path to the CSV file to ingest (default: data/samples/sample_energy_consumption.csv)",
    )
    parser.add_argument(
        "--bucket",
        type=str,
        default=os.getenv("DATA_LAKE_BUCKET"),
        help="Target S3 bucket. Falls back to DATA_LAKE_BUCKET env variable.",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=os.getenv("DATA_LAKE_PREFIX", "watt-about-it/raw"),
        help="Key prefix inside the bucket (default: watt-about-it/raw or DATA_LAKE_PREFIX env variable).",
    )
    parser.add_argument(
        "--region",
        type=str,
        default=os.getenv("AWS_REGION"),
        help="AWS region (optional, boto3 falls back to default chain).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run validation and logging without uploading to the cloud.",
    )
    return parser


def configure_logging(run_id: str) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"ingestion_{run_id}.log"
    handlers = [logging.StreamHandler(sys.stdout), logging.FileHandler(log_path, mode="w", encoding="utf-8")]
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers)
    return log_path


def ensure_env_loaded() -> None:
    if load_dotenv is not None:
        load_dotenv()


def read_csv(source: Path) -> pd.DataFrame:
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    df = pd.read_csv(source)
    if "reading_ts" in df.columns:
        df["reading_ts"] = pd.to_datetime(df["reading_ts"], utc=True, errors="raise")
    if "is_peak" in df.columns:
        df["is_peak"] = (
            df["is_peak"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({"true": True, "false": False})
        )
        if df["is_peak"].isna().any():
            raise ValueError("Invalid boolean values detected in 'is_peak' column.")
        df["is_peak"] = df["is_peak"].astype(bool)
    return df


def validate_structure(df: pd.DataFrame) -> ValidationResult:
    missing = [col for col in EXPECTED_SCHEMA if col not in df.columns]
    extra = [col for col in df.columns if col not in EXPECTED_SCHEMA]
    if missing:
        raise ValueError(f"Missing mandatory columns: {missing}")

    if extra:
        logging.warning("Extra columns detected and will be preserved: %s", extra)

    type_errors: List[str] = []
    for column, expected_type in EXPECTED_SCHEMA.items():
        if not _is_dtype(df[column], expected_type):
            type_errors.append(f"{column} expected {expected_type}")

    if type_errors:
        raise ValueError(f"Column type mismatches: {type_errors}")

    return ValidationResult(missing_columns=missing, extra_columns=extra)


def _is_dtype(series: pd.Series, expected: str) -> bool:
    from pandas.api import types as ptypes

    if expected == "string":
        return ptypes.is_string_dtype(series.dtype) or ptypes.is_object_dtype(series.dtype)
    if expected == "float":
        return ptypes.is_float_dtype(series.dtype)
    if expected == "datetime":
        return ptypes.is_datetime64_any_dtype(series.dtype)
    if expected == "bool":
        return ptypes.is_bool_dtype(series.dtype)
    return False


def upload_to_s3(source: Path, bucket: str, prefix: str, region: str | None, run_id: str) -> str:
    session_kwargs = {"region_name": region} if region else {}
    s3_client = boto3.client("s3", **session_kwargs)

    date_part = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    version_tag = datetime.now(timezone.utc).strftime("%H%M%S")
    prefix = prefix.strip("/")
    object_key = f"{prefix}/{date_part}/{source.stem}_{run_id}_{version_tag}.csv"

    logging.info("Uploading %s to s3://%s/%s", source, bucket, object_key)
    try:
        s3_client.upload_file(str(source), bucket, object_key)
    except ClientError as exc:
        raise RuntimeError(f"Upload to s3://{bucket}/{object_key} failed") from exc

    return object_key


def main() -> None:
    ensure_env_loaded()
    parser = build_arg_parser()
    args = parser.parse_args()

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = configure_logging(run_id)
    logging.info("Starting ingestion run %s", run_id)

    source_path = args.source.expanduser().resolve()
    logging.info("Loading source file: %s", source_path)
    df = read_csv(source_path)
    logging.info("Dataset shape: %s rows x %s columns", df.shape[0], df.shape[1])

    validate_structure(df)
    logging.info("Schema validation successful for columns: %s", list(df.columns))

    bucket = args.bucket or os.getenv("DATA_LAKE_BUCKET")
    if not bucket:
        raise RuntimeError("S3 bucket must be provided via --bucket or DATA_LAKE_BUCKET env variable.")
    prefix = args.prefix or os.getenv("DATA_LAKE_PREFIX", "watt-about-it/raw")

    if args.dry_run:
        logging.info("Dry-run enabled: skipping upload while keeping validation and logs.")
        final_path = f"s3://{bucket}/{prefix.strip('/')}/<dry-run>"
    else:
        object_key = upload_to_s3(source_path, bucket, prefix, args.region, run_id)
        final_path = f"s3://{bucket}/{object_key}"

    logging.info("Ingestion successful. Cloud destination: %s", final_path)
    logging.info("Log file written to %s", log_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # Catch-all to ensure failure is logged and non-zero exit is propagated.
        logging.exception("Ingestion failed: %s", exc)
        sys.exit(1)
