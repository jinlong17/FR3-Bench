"""QA correctness and restoration metric helpers for the FR3 benchmark.

QA evaluation follows the NTIRE 2026 FR3 challenge protocol:
- Numeric answers are compared with a 1% relative tolerance.
- Near-zero ground truth (|gt| < 1e-10) falls back to an absolute tolerance of 0.01.
- Non-numeric answers are compared by stripped string equality.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def is_correct(
    predicted: Any,
    ground_truth: Any,
    relative_tolerance: float = 0.01,
    absolute_tolerance: float = 0.01,
) -> bool:
    if predicted is None or predicted == "":
        return False
    try:
        pred_num = float(predicted)
        gt_num = float(ground_truth)
        if abs(gt_num) < 1e-10:
            return abs(pred_num - gt_num) < absolute_tolerance
        return abs(pred_num - gt_num) / abs(gt_num) < relative_tolerance
    except (ValueError, TypeError):
        return str(predicted).strip() == str(ground_truth).strip()


def load_qa(path: str | Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def qa_accuracy(
    gt_pairs: Iterable[dict],
    pred_pairs: Iterable[dict],
    relative_tolerance: float = 0.01,
) -> dict:
    gt = list(gt_pairs)
    pred = list(pred_pairs)
    if len(gt) != len(pred):
        raise ValueError(
            f"QA pair count mismatch: ground truth has {len(gt)}, prediction has {len(pred)}"
        )
    correct = 0
    failures: list[dict] = []
    for idx, (g, p) in enumerate(zip(gt, pred)):
        if g.get("question") != p.get("question"):
            failures.append({"idx": idx, "type": "question_mismatch"})
            continue
        if is_correct(p.get("answer"), g.get("answer"), relative_tolerance):
            correct += 1
        else:
            failures.append(
                {
                    "idx": idx,
                    "type": "wrong_answer",
                    "gt": g.get("answer"),
                    "pred": p.get("answer"),
                }
            )
    total = len(gt)
    return {
        "accuracy": correct / total if total else 0.0,
        "total": total,
        "correct": correct,
        "failures": failures,
    }


def psnr(pred, target, data_range: float = 1.0) -> float:
    """Mean PSNR across paired arrays. Expects numpy arrays in [0, data_range]."""
    import numpy as np

    pred = np.asarray(pred, dtype=np.float64)
    target = np.asarray(target, dtype=np.float64)
    mse = ((pred - target) ** 2).mean()
    if mse <= 0:
        return float("inf")
    return float(10.0 * np.log10((data_range**2) / mse))


def ssim(pred, target) -> float:
    """Wrapper around scikit-image SSIM (channel-last RGB float images)."""
    from skimage.metrics import structural_similarity

    return float(
        structural_similarity(
            pred, target, channel_axis=-1, data_range=1.0
        )
    )
