# Week 1 Starter – From analytical code to application component

## Goal
We turn notebook/prototype-style Python code into a reusable data-processing component and a minimal command-line application.

## Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Starting point
Open `src/prototype.py`. It can work as a quick analysis, but it is weak as an application component because it relies on hardcoded paths, global state, and print-based behavior.

## Task
Complete the functions in `src/pipeline.py`, then run:

```bash
python src/app.py --input data/issues_raw.csv --output data/issues_processed.csv
```

## Testing
```bash
pytest
```

## Using an AI assistant
You may use an AI assistant to brainstorm functions, tests, and debugging ideas, but you are responsible for understanding, running, and verifying the generated code.
