import copy
import pandas as pd
import pytest
from src.policy_engine import validate_policy, validate_predictions, decision_for_row

BASE_POLICY = {
    "policy_version": "test",
    "default": {"auto_accept_max": 0.25, "manual_review_max": 0.70},
    "segment_overrides": {
        "high_value": {"auto_accept_max": 0.15, "manual_review_max": 0.50}
    },
}

def test_invalid_policy_order_is_rejected():
    policy = copy.deepcopy(BASE_POLICY)
    policy["default"]["auto_accept_max"] = 0.8
    policy["default"]["manual_review_max"] = 0.4
    with pytest.raises(ValueError):
        validate_policy(policy)

def test_probability_outside_range_is_rejected():
    df = pd.DataFrame([{
        "case_id": "X1",
        "risk_probability": 1.2,
        "segment": "standard",
        "amount": 10,
    }])
    with pytest.raises(ValueError):
        validate_predictions(df)

def test_segment_override_changes_decision():
    row = pd.Series({
        "case_id": "X2",
        "risk_probability": 0.20,
        "segment": "high_value",
        "amount": 8000,
    })
    decision, _ = decision_for_row(row, BASE_POLICY)
    assert decision == "manual_review"

def test_standard_case_can_be_auto_accepted():
    row = pd.Series({
        "case_id": "X3",
        "risk_probability": 0.20,
        "segment": "standard",
        "amount": 100,
    })
    decision, _ = decision_for_row(row, BASE_POLICY)
    assert decision == "auto_accept"
