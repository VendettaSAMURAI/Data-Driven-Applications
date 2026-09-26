import pandas as pd
import pytest

from src.pipeline import classify_issue, validate_input, process_cases


def test_classify_missing_value():
    result = classify_issue("The category field is missing from the record.", "category", "")
    assert result["issue_type"] == "missing_value"
    assert result["requires_review"] is True


def test_classify_invalid_numeric():
    result = classify_issue("The price field contains a negative value.", "price", "-12")
    assert result["issue_type"] == "invalid_numeric"
    assert result["computed_severity"] == "high"


def test_validate_input_detects_missing_column():
    df = pd.DataFrame({"case_id": ["DQ-1"]})
    with pytest.raises(ValueError):
        validate_input(df)


def test_process_cases_adds_columns():
    df = pd.DataFrame({
        "case_id": ["DQ-1"],
        "source_system": ["CRM"],
        "field_name": ["email"],
        "reported_value": [""],
        "issue_text": ["The email field is missing from the record."],
        "created_at": ["2026-09-01T10:00:00"],
        "reporter_team": ["DataOps"],
    })
    out = process_cases(df)
    assert {"issue_type", "computed_severity", "requires_review"}.issubset(out.columns)
