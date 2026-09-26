from __future__ import annotations
from pathlib import Path
import json
import pandas as pd

REQUIRED_COLUMNS = {"case_id", "risk_probability", "segment", "amount"}

def load_policy(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _validate_thresholds(name: str, thresholds: dict) -> None:
    required = {"auto_accept_max", "manual_review_max"}
    missing = required - set(thresholds)
    if missing:
        raise ValueError(f"{name}: missing threshold(s): {sorted(missing)}")
    low = thresholds["auto_accept_max"]
    high = thresholds["manual_review_max"]
    if not (0 <= low <= 1 and 0 <= high <= 1):
        raise ValueError(f"{name}: thresholds must be between 0 and 1")
    if low > high:
        raise ValueError(f"{name}: auto_accept_max must be <= manual_review_max")

def validate_policy(policy: dict) -> None:
    if not policy.get("policy_version"):
        raise ValueError("policy_version is required")
    if "default" not in policy:
        raise ValueError("default thresholds are required")
    _validate_thresholds("default", policy["default"])
    for segment, thresholds in policy.get("segment_overrides", {}).items():
        _validate_thresholds(f"segment '{segment}'", thresholds)

def load_predictions(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)

def validate_predictions(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df["case_id"].isna().any() or df["case_id"].astype(str).str.strip().eq("").any():
        raise ValueError("case_id must not be empty")
    if df["risk_probability"].isna().any() or not df["risk_probability"].between(0, 1).all():
        raise ValueError("risk_probability must be between 0 and 1")
    if df["amount"].isna().any() or (df["amount"] < 0).any():
        raise ValueError("amount must be non-negative")

def decision_for_row(row: pd.Series, policy: dict) -> tuple[str, str]:
    thresholds = policy.get("segment_overrides", {}).get(
        row["segment"], policy["default"]
    )
    p = float(row["risk_probability"])
    accept_max = float(thresholds["auto_accept_max"])
    review_max = float(thresholds["manual_review_max"])

    if p <= accept_max:
        return "auto_accept", f"risk_probability <= {accept_max:.2f}"
    if p <= review_max:
        return "manual_review", f"{accept_max:.2f} < risk_probability <= {review_max:.2f}"
    return "reject", f"risk_probability > {review_max:.2f}"

def process_predictions(df: pd.DataFrame, policy: dict) -> pd.DataFrame:
    validate_predictions(df)
    validate_policy(policy)
    result = df.copy()
    decisions = result.apply(lambda row: decision_for_row(row, policy), axis=1)
    result["decision"] = [d for d, _ in decisions]
    result["decision_reason"] = [r for _, r in decisions]
    result["policy_version"] = policy["policy_version"]
    return result

def summarize_decisions(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("decision", dropna=False)
          .size()
          .reset_index(name="case_count")
          .sort_values("decision")
          .reset_index(drop=True)
    )

def save_results(df: pd.DataFrame, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
