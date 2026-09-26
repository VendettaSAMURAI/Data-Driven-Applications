# Week 1 – Python: From analytical code to application component

## Starting situation
A DataOps team receives data quality cases from several systems. The goal is to turn notebook/prototype-style Python code into a reusable component that can later be called from an application, workflow, or API.

## Learning goals
By the end of the session, you will be able to:

1. distinguish an analytical prototype from an application component;
2. split Python code into functions with clear input/output steps;
3. add simple data validation and error handling;
4. build a minimal command-line data-processing application;
5. use an AI assistant for coding, while verifying the result with execution and tests.

## In-class task
The `src/prototype.py` file is a quickly assembled, notebook-like prototype. Your task is to move the logic into the functions in `src/pipeline.py`, then run the minimal application.

## Setup
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Tasks

### Task 1 – Understand the prototype
Open `src/prototype.py`. Identify at least three reasons why it is not suitable as a long-term application component.

### Task 2 – Loading and validation
Complete:

- `load_cases(path)`
- `validate_input(df)`

Validation should at least check whether all required columns are present.

### Task 3 – Case classification
Complete the `classify_issue(...)` function.

The return value should be a dictionary:

```python
{
    "issue_type": "missing_value",
    "computed_severity": "medium",
    "requires_review": True,
}
```

### Task 4 – Batch processing
Complete:

- `process_cases(df)`
- `summarize_cases(df)`
- `save_cases(df, path)`

### Task 5 – Run the application
Run:

```bash
python src/app.py --input data/issues_raw.csv --output data/issues_processed.csv
```

If successful, the file `data/issues_processed.csv` should be created and a short summary should appear in the terminal.

### Task 6 – Verify
Run:

```bash
pytest
```

The goal is not necessarily to make everything green on the first attempt. Use the failures to improve the component.

## Using an AI assistant
You may use ChatGPT, Copilot, or another AI assistant for example to:

- complete function skeletons;
- write pandas code;
- explain errors;
- brainstorm test cases.

Required verification:

- run the code;
- inspect the output CSV;
- run the tests;
- explain what your solution does.

## Minimum deliverable
By the end of the session, you should have:

- a working `src/pipeline.py`;
- a runnable `src/app.py`;
- a generated `data/issues_processed.csv`;
- at least a partially successful or interpretable test run.

## Advanced tasks
1. Add a `--min-severity` command-line argument.
2. Add a new test for an `outlier` or `format_error` case.
3. Save a separate `summary.csv` file with the summary table.
4. Replace `print` with `logging`.
