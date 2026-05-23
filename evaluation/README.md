# Evaluation

Two evaluators, matching the NTIRE 2026 FR3 challenge protocol.

## 1. QA Accuracy (primary metric)

```bash
python evaluation/run_eval.py \
    --gt data/annotations/val_qa.json \
    --pred submission.json \
    --out scores.txt
```

- `submission.json` must be a JSON list, same length and ordering as the GT file,
  with `question` and `answer` fields per entry.
- Numeric answers use a 1% relative tolerance (or 0.01 absolute when GT ≈ 0).
- Answers should be rounded to 2 decimal places using Python `decimal.ROUND_HALF_UP`.

## 2. Image Restoration Quality

```bash
python evaluation/run_restoration_eval.py \
    --pred-dir path/to/restored \
    --gt-dir   path/to/clean \
    --out      restoration_scores.txt
```

PSNR and SSIM are computed via `scikit-image`. LPIPS requires installing
`lpips` and `torch` (skipped automatically if unavailable).

## Final ranking

Final ranking is primarily by QA accuracy and complemented by PSNR / SSIM / LPIPS.
See [EVALUATION.md](../EVALUATION.md) for the full submission protocol.
