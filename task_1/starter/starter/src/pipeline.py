"""Week 1 starter file.

Goal: split the logic from prototype.py into reusable components.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "case_id",
    "source_system",
    "field_name",
    "reported_value",
    "issue_text",
    "created_at",
    "reporter_team",
}


def load_cases(path: str | Path) -> pd.DataFrame:
    """Load a CSV file and perform minimal schema validation."""
    df = pd.read_csv(path)
    validate_input(df)
    return df


def validate_input(df: pd.DataFrame) -> None:
    """Check whether all required columns are present."""
    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(missing)


def classify_issue(
    text: str,
    field_name: str = "",
    reported_value: str = ""
) -> dict:
    """Classify one data quality case with simple rule-based logic."""

    if "missing" in text:
        return {
            "issue_type": "missing_value",
            "computed_severity": "medium",
            "requires_review": True,
        }

    # Other classification rules need to come from
    # the lab tests/prototype.
    return {
        "issue_type": "unknown",
        "computed_severity": "low",
        "requires_review": False,
    }


def process_cases(df: pd.DataFrame) -> pd.DataFrame:
    """Process all cases and add new classification columns."""

    results = []

    for index, row in df.iterrows():
        result = classify_issue(
            row["issue_text"],
            row["field_name"],
            row["reported_value"]
        )

        results.append(result)

    classification_df = pd.DataFrame(results)

    df = df.copy()

    df["issue_type"] = classification_df["issue_type"].values
    df["computed_severity"] = classification_df["computed_severity"].values
    df["requires_review"] = classification_df["requires_review"].values

    return df


def summarize_cases(df: pd.DataFrame) -> pd.DataFrame:
    """Create a simple summary table by issue_type and severity."""

    summary = (
        df.groupby(["issue_type", "computed_severity"])
        .size()
        .reset_index(name="count")
    )

    return summary


def save_cases(df: pd.DataFrame, path: str | Path) -> None:
    """Save the result to a CSV file."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)