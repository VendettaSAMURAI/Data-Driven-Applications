"""Week 1 - intentionally notebook-like prototype.

Task: refactor this logic into reusable components.
"""

import pandas as pd

# Intentionally hardcoded paths and print-based behavior.
df = pd.read_csv("data/issues_raw.csv")

categories = []
severity = []
review = []

for text in df["issue_text"]:
    text_l = str(text).lower()
    if "missing" in text_l:
        categories.append("missing_value")
        severity.append("medium")
        review.append(True)
    elif "negative" in text_l or "non-numeric" in text_l:
        categories.append("invalid_numeric")
        severity.append("high")
        review.append(True)
    elif "date" in text_l:
        categories.append("invalid_date")
        severity.append("medium")
        review.append(True)
    elif "duplicate" in text_l:
        categories.append("duplicate")
        severity.append("medium")
        review.append(True)
    elif "extremely high" in text_l:
        categories.append("outlier")
        severity.append("high")
        review.append(True)
    elif "format" in text_l:
        categories.append("format_error")
        severity.append("low")
        review.append(False)
    else:
        categories.append("unknown")
        severity.append("low")
        review.append(True)


df["issue_type"] = categories
df["computed_severity"] = severity
df["requires_review"] = review

print(df.head())
print(df["issue_type"].value_counts())

df.to_csv("data/issues_processed.csv", index=False)
