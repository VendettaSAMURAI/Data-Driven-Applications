# Task 3 – Robust file ingestion with quarantine

## Scenario
A partner system drops several CSV files into a folder every day. In real systems, you cannot assume that every row is valid, and one bad record should not necessarily stop the complete batch.

Build an ingestion component that:

1. loads all CSV files from a folder;
2. keeps the source filename for traceability;
3. separates valid and invalid rows;
4. quarantines invalid rows with an explicit reason;
5. removes duplicate records by keeping the latest version;
6. writes a small machine-readable run report.

This task introduces concepts that the main Week 1 exercise does not cover:

> **partial failure, quarantine, lineage, deduplication, and operational run reporting.**

## Suggested use
- **40–60 minutes** as a longer extra task;
- suitable as homework if there is not enough class time.

## Your tasks

Complete the functions in `src/ingestion.py`:

- `load_folder()`
- `validate_and_split()`
- `deduplicate_latest()`
- `build_run_report()`
- `save_outputs()`

Run:

```bash
python app.py
pytest
```

Expected outputs:

```text
data/output/clean.csv
data/output/rejected.csv
data/output/run_report.json
```

## Validation rules
A row must be rejected if:

- `record_id` is missing;
- `event_time` cannot be parsed;
- `sensor` is not one of `temp`, `pressure`, `humidity`;
- `value` is not numeric.

A rejected row should contain a useful `rejection_reason`.

## Deduplication rule
If several valid rows have the same `record_id`, keep the row with the **latest `event_time`**.

## AI-assisted working pattern
Use AI for **one design problem**, then solve the paired problem yourself.

Suggested sequence:

1. Ask AI to propose a clean way to represent multiple validation errors in `rejection_reason`.
2. Implement the validation/quarantine logic.
3. **Without AI**, implement `deduplicate_latest()` and `build_run_report()`.
4. Run the tests and inspect the actual output files.

## Design questions
Be prepared to answer:

- Why is quarantine often better than stopping the whole batch?
- Why do we preserve `source_file`?
- Why is deduplication a business rule rather than just a pandas trick?
- What would make this pipeline safe to run repeatedly?

## Minimum result
A run should produce:
- a clean dataset;
- a rejected dataset with reasons;
- a JSON run report.

## Extension
Make the pipeline idempotent by adding a simple processed-file manifest, so already processed input files are skipped on the next run.
