# Evaluation Protocol

The challenge has **two evaluation phases**, mirroring the NTIRE 2026 setup.

## Phase 1 — Development

You get `data/annotations/val_qa.json` (108 QA pairs with answers) and the
matching 200 validation images (degraded + clean) on HuggingFace. Iterate
locally:

```bash
python evaluation/run_eval.py \
    --gt data/annotations/val_qa.json \
    --pred submission_val.json

python evaluation/run_restoration_eval.py \
    --pred-dir restored_val/ \
    --gt-dir   data/images/val/clean/
```

## Phase 2 — Test

`data/annotations/test_qa.json` has 901 questions with hidden answers (`""`).
The 1,000 test images are released as **degraded only** — clean references
are kept on the evaluation server.

You submit:

1. **Restored images** — one file per degraded test image, same filename.
2. **A QA prediction JSON** — same length and ordering as `test_qa.json`, with
   the `answer` field filled in.

Submissions are scored on the [CodaBench leaderboard](https://www.codabench.org/competitions/13606/).

## Submission format

```json
[
  {
    "question": "From 2023-01-01 to 2023-12-31, what is the total amount spent?",
    "answer": 62195.25,
    "image_list": ["bill_0001.jpg", "..."]
  },
  ...
]
```

- The list **must** have the same length as `test_qa.json` (901 entries).
- `question` and `image_list` should be copied verbatim from `test_qa.json`.
- `answer` should be a numeric value rounded to 2 decimal places using
  `decimal.ROUND_HALF_UP`.

## Scoring

### QA accuracy (primary)

Each predicted answer is compared with the ground truth:

- If both are numeric: correct iff `|pred - gt| / |gt| < 0.01` (1% relative
  tolerance). When `|gt| < 1e-10`, use absolute tolerance 0.01 instead.
- Otherwise: case-sensitive stripped string equality.

The reported accuracy is `correct / total`.

### Restoration quality (secondary)

- **PSNR** (peak signal-to-noise ratio, dB ↑) — pixel fidelity.
- **SSIM** (structural similarity, ↑) — structural consistency.
- **LPIPS** (learned perceptual similarity, ↓) — perceptual distance.

### Final ranking

Primarily by QA accuracy; PSNR/SSIM/LPIPS are used as tie-breakers and
secondary indicators. A method with great restoration metrics but poor
reasoning accuracy will not place highly — see VEPG in the leaderboard (best
restoration, 5th on accuracy).

## Rules

1. All methods must be reproducible. Submit your code and a fact sheet
   describing the pipeline.
2. One team submission per participant. One algorithm per team for the final
   ranking.
3. Pre-trained models / external data are allowed but must be disclosed.
4. No use of the held-out test answers in any form during training.
