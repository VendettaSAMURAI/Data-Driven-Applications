from __future__ import annotations
import argparse
from src.policy_engine import (
    load_policy, load_predictions, process_predictions,
    summarize_decisions, save_results
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/predictions.csv")
    parser.add_argument("--policy", default="data/policy.json")
    parser.add_argument("--output", default="data/decisions.csv")
    args = parser.parse_args()

    policy = load_policy(args.policy)
    df = load_predictions(args.input)
    result = process_predictions(df, policy)
    save_results(result, args.output)

    print("\nDecision summary")
    print(summarize_decisions(result).to_string(index=False))

if __name__ == "__main__":
    main()
