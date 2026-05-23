# Data

## Layout

```
data/
├── annotations/
│   ├── val_qa.json     # 108 validation QA pairs (with answers)
│   └── test_qa.json    # 901 test QA pairs (answers hidden)
├── images/             # Receipt images (downloaded from HuggingFace; gitignored)
└── download_data.py    # Pulls images from HuggingFace
```

Only the small annotation JSONs are shipped in this repository. The full image
dataset (≈ 4.4 GB) is hosted on HuggingFace and pulled on demand.

> **Dev note**: when this repo is checked out as part of the FR3 monorepo
> alongside `benchmark_source/`, `data/images` is a symlink to
> `../../benchmark_source/` instead of a downloaded directory. The
> evaluation scripts work either way; `download_data.py` is only needed for
> standalone (public) clones.

## Get the images

```bash
# Full dataset (validation + test)
python data/download_data.py --out data/images

# Only validation (smaller, for development)
python data/download_data.py --out data/images --split val
```

The download requires the `huggingface_hub` Python package (in
`requirements.txt`). Anonymous access is sufficient.

## Annotation format

Each entry in the QA JSON files looks like:

```json
{
  "question": "From 2023-01-01 to 2023-12-31, what is the total amount spent (sum of receipt totals)?",
  "answer": 62195.25,
  "image_list": ["bill_0001.jpg", "bill_0002.jpg", ...],
  "metadata": {
    "calculation_method": "sum",
    "template": "T001",
    "categories": ["all"]
  }
}
```

In `test_qa.json` the `answer` field is an empty string and `metadata` is
omitted. Models must fill in `answer` and keep the same ordering and
`image_list` as the GT file when submitting.

The 16 calculation methods used: `sum`, `average`, `percentage`, `range`,
`maximum`, `median`, `minimum`, `difference`, `ratio`, `standard_deviation`,
`harmonic_mean`, `coefficient_of_variation`, `aggregation`, `percentile`,
`variance`, `interquartile_range`.
