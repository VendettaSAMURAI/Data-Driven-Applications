"""Minimal command-line application for the Week 1 lab.

Example:
python src/app.py --input data/issues_raw.csv --output data/issues_processed.csv
"""

from __future__ import annotations

import argparse
from pipeline import load_cases, process_cases, summarize_cases, save_cases


def main() -> None:
    parser = argparse.ArgumentParser(description="Data quality case processor")
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--output", required=True, help="Output CSV file")
    args = parser.parse_args()

    df = load_cases(args.input)
    processed = process_cases(df)
    save_cases(processed, args.output)

    print("Processed:", len(processed), "records")
    print(summarize_cases(processed).to_string(index=False))


if __name__ == "__main__":
    main()
