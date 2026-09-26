import pandas as pd
from src.ingestion import validate_and_split, deduplicate_latest, build_run_report

def test_invalid_rows_are_quarantined():
    df = pd.DataFrame([
        {"record_id":"A","event_time":"2026-09-01T10:00:00","sensor":"temp","value":"21.5","source_file":"x.csv"},
        {"record_id":"B","event_time":"bad","sensor":"temp","value":"20.0","source_file":"x.csv"},
        {"record_id":"C","event_time":"2026-09-01T10:00:00","sensor":"wind","value":"5.0","source_file":"x.csv"},
    ])
    valid, rejected = validate_and_split(df)
    assert len(valid) == 1
    assert len(rejected) == 2
    assert rejected["rejection_reason"].str.len().gt(0).all()

def test_latest_duplicate_is_kept():
    df = pd.DataFrame([
        {"record_id":"A","event_time":pd.Timestamp("2026-09-01T10:00:00"),"sensor":"temp","value":20.0,"source_file":"a.csv"},
        {"record_id":"A","event_time":pd.Timestamp("2026-09-02T10:00:00"),"sensor":"temp","value":21.0,"source_file":"b.csv"},
    ])
    result = deduplicate_latest(df)
    assert len(result) == 1
    assert result.iloc[0]["value"] == 21.0
    assert result.iloc[0]["source_file"] == "b.csv"

def test_report_counts_duplicates():
    report = build_run_report(
        input_rows=12,
        valid_before_dedup=8,
        rejected_rows=4,
        final_rows=6,
    )
    assert report["duplicates_removed"] == 2
    assert report["final_rows"] == 6
