# Task 2 – Config-driven model decision service

## Scenario
A predictive model returns a risk probability for each case. The model itself does **not** decide the business action. A separate policy determines whether a case is automatically accepted, sent to manual review, or rejected.

This task introduces a different application-design idea from the main Week 1 exercise:

> **Keep business policy outside the Python code whenever practical.**

The policy is stored in `data/policy.json`, so threshold changes do not require rewriting the processing logic.

## Suggested use
- **25–40 minutes** as a second in-class task, or
- homework if the first task takes longer.

## Your tasks

1. Implement `load_policy()`.
2. Implement `validate_policy()`.
3. Implement `validate_predictions()`.
4. Implement `decision_for_row()`.
5. Implement `process_predictions()`.
6. Implement `summarize_decisions()`.
7. Run:

```bash
python app.py
pytest
```

## Important design questions
Be prepared to answer:

- Why should the model probability and the business decision be separate?
- What is gained by storing thresholds in a configuration file?
- What could go wrong if the configuration is invalid?
- Why should the output include `policy_version` and `decision_reason`?

## AI-assisted working pattern
Use an AI assistant deliberately, but not for every step.

**AI-assisted step:** ask the assistant to propose validation rules for `policy.json`.

Then, **without asking the AI**, implement the validation of the prediction DataFrame yourself.

Afterwards compare the two kinds of validation:
- configuration validation;
- input-data validation.

For testing, you may ask AI to suggest **one** edge case. Write at least **one additional edge-case test yourself**.

## Minimum result
A working program that produces `data/decisions.csv` with:
- a decision;
- an explanation;
- the policy version.

## Extension
Add a second configuration file representing a new policy version and demonstrate that the same Python code produces different decisions without code changes.
