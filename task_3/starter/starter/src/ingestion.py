from __future__ import annotations
from pathlib import Path
import json
import pandas as pd

ALLOWED_SENSORS = {"temp", "pressure", "humidity"}
REQUIRED_COLUMNS = {"record_id", "event_time", "sensor", "value"}

def load_folder(folder: str | Path) -> pd.DataFrame:
    """
    Load every CSV in a folder and add source_file.
    The pipeline should continue if there are multiple files.
    """
    # TODO
    raise NotImplementedError

def validate_and_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Return (valid_rows, rejected_rows).

    Reject rows when:
    - record_id is empty;
    - event_time is invalid;
    - sensor is unsupported;
    - value is not numeric.

    Add rejection_reason to rejected rows.
    """
    # TODO
    raise NotImplementedError

def deduplicate_latest(df: pd.DataFrame) -> pd.DataFrame:
    """
    For duplicate record_id values, keep the row with the latest event_time.
    """
    # TODO
    raise NotImplementedError

def build_run_report(
    input_rows: int,
    valid_before_dedup: int,
    rejected_rows: int,
    final_rows: int,
) -> dict:
    """Return a serializable run summary."""
    # TODO
    raise NotImplementedError

def save_outputs(
    clean: pd.DataFrame,
    rejected: pd.DataFrame,
    report: dict,
    output_folder: str | Path,
) -> None:
    # TODO
    raise NotImplementedError
