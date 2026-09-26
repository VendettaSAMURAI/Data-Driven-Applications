from __future__ import annotations
import argparse
from src.ingestion import (
    load_folder, validate_and_split, deduplicate_latest,
    build_run_report, save_outputs
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder", default="data/incoming")
    parser.add_argument("--output-folder", default="data/output")
    args = parser.parse_args()

    raw = load_folder(args.input_folder)
    valid, rejected = validate_and_split(raw)
    clean = deduplicate_latest(valid)

    report = build_run_report(
        input_rows=len(raw),
        valid_before_dedup=len(valid),
        rejected_rows=len(rejected),
        final_rows=len(clean),
    )
    save_outputs(clean, rejected, report, args.output_folder)

    print("Run report")
    for key, value in report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
