#!/usr/bin/env python
"""Run the FR3 QA evaluation on a submission file.

Usage:
    python evaluation/run_eval.py \
        --gt data/annotations/val_qa.json \
        --pred path/to/submission.json \
        [--out scores.txt]

Submission format: a JSON list with the same ordering as the GT file, where
each entry has at least `question` and `answer` fields. See EVALUATION.md.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from metrics import load_qa, qa_accuracy


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gt", required=True, help="Path to ground-truth QA JSON")
    parser.add_argument("--pred", required=True, help="Path to prediction/submission JSON")
    parser.add_argument("--out", default=None, help="Optional scores output file")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.01,
        help="Relative tolerance for numeric answers (default 0.01 = 1%%)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print first 5 failure cases",
    )
    args = parser.parse_args()

    gt = load_qa(args.gt)
    pred = load_qa(args.pred)
    result = qa_accuracy(gt, pred, relative_tolerance=args.tolerance)

    print("=" * 60)
    print("FR3 QA Evaluation")
    print("=" * 60)
    print(f"Ground truth file : {args.gt}")
    print(f"Submission file   : {args.pred}")
    print(f"Total QA pairs    : {result['total']}")
    print(f"Correct answers   : {result['correct']}")
    print(f"Accuracy          : {result['accuracy']:.4f} ({result['accuracy'] * 100:.2f}%)")
    print("=" * 60)

    if args.verbose:
        wrong = [f for f in result["failures"] if f["type"] == "wrong_answer"][:5]
        for f in wrong:
            print(f"  [idx {f['idx']}] gt={f['gt']!r} pred={f['pred']!r}")

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w") as f:
            f.write(f"Accuracy:{result['accuracy']:.6f}\n")
            f.write(f"Total:{result['total']}\n")
            f.write(f"Correct:{result['correct']}\n")
        print(f"Scores written to: {args.out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
