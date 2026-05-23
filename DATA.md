# Dataset Documentation

## Overview

FR³ pairs degraded receipt images with clean references and structured
financial questions. The dataset is hosted on HuggingFace:
[`chickencaesar-yang/NTIRE_2026_Financial_Receipt`](https://huggingface.co/datasets/chickencaesar-yang/NTIRE_2026_Financial_Receipt)

| Split | Images | QA pairs | Answers public? |
|-------|--------|---------:|-----------------|
| Validation | 200 | 108 | ✅ Yes (`val_qa.json`) |
| Test       | 1,000 | 901 | ❌ Hidden (`test_qa.json` has `"answer": ""`) |
| **Total**  | **1,200** | **1,009** | — |

## How the data was built

1. **Privacy-preserving authoring.** Receipt templates were hand-designed
   (merchant, date, items, taxes, totals, payment method, location) — no real
   customer data was used.
2. **Real physical capture.** Receipts were printed on a real thermal printer
   and photographed handheld with an OPPO smartphone under varied lighting,
   yielding realistic paper texture, printer artifacts, and illumination
   noise in the "clean" set.
3. **Degradation synthesis.** Generative models (Gemini Pro and others) added
   blur, noise, compression artifacts, illumination changes, and partial
   occlusions, producing paired degraded/clean images.
4. **QA generation.** Multi-step computational questions were derived from
   structured per-receipt metadata (merchant, total, category, datetime, …).

## QA schema

```json
{
  "question": "What is the average tax amount per receipt in the 'food' category?",
  "answer": 4.51,
  "image_list": ["bill_0023.jpg", "bill_0118.jpg", "..."],
  "metadata": {
    "calculation_method": "average",
    "template": "MERCHANT_AVG_ALL",
    "categories": ["food"]
  }
}
```

- `answer` is a float rounded to 2 decimal places using
  `decimal.ROUND_HALF_UP`.
- `image_list` ranges from 10 to 1000 entries — many questions require
  reasoning across the entire test set.
- In `test_qa.json` the `answer` is `""` and `metadata` is absent.

## Calculation methods (16)

| Method | Test % | Val % |
|--------|-------:|------:|
| average | 30.2% | 17.6% |
| sum | 21.8% | 13.0% |
| percentage | 10.1% | 23.1% |
| range | 10.0% | 4.6% |
| maximum | 7.3% | 4.6% |
| median | 5.6% | 6.5% |
| minimum | 5.4% | 4.6% |
| difference | 2.7% | 2.8% |
| ratio | 2.0% | 6.5% |
| standard_deviation | 1.2% | 3.7% |
| harmonic_mean | 1.1% | 2.8% |
| coefficient_of_variation | 1.1% | 2.8% |
| aggregation | 1.1% | 3.7% |
| percentile | 0.2% | 1.9% |
| variance | 0.1% | 0.9% |
| interquartile_range | 0.1% | 0.9% |

## Download

```bash
pip install huggingface_hub
python data/download_data.py --out data/images               # full dataset
python data/download_data.py --out data/images --split val   # validation only
```

Alternatively, with the `datasets` library:

```python
from datasets import load_dataset
ds = load_dataset("chickencaesar-yang/NTIRE_2026_Financial_Receipt")
```

## Disk footprint

| Component | Size |
|-----------|-----:|
| Test images (1,000 degraded + 1,000 clean) | ~3.6 GB |
| Validation images (200 degraded + 200 clean) | ~789 MB |
| Annotation JSONs (in this repo) | ~6 MB |

## License

The dataset is released under **CC BY 4.0**. You are free to share and adapt
the data with appropriate credit. See [LICENSE](LICENSE).
