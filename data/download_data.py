#!/usr/bin/env python
"""Download the FR3 Financial Receipt dataset from HuggingFace.

The full image dataset (paired degraded / clean receipts) lives on HuggingFace:
    https://huggingface.co/datasets/chickencaesar-yang/NTIRE_2026_Financial_Receipt

This script pulls everything into `data/images/` by default and leaves the
small annotation JSONs (already in this repo at `data/annotations/`) untouched.

Note for project developers: `data/images` may be a symlink to the local
`benchmark_source/` staging area. In that case you do **not** need to run
this script — the data is already on disk. The script aborts with a clear
message if the target is a symlink, to avoid writing HF downloads into the
upstream staging dir.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HF_REPO_ID = "chickencaesar-yang/NTIRE_2026_Financial_Receipt"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default="data/images",
        help="Where to download the dataset (default: data/images)",
    )
    parser.add_argument(
        "--split",
        choices=["all", "val", "test"],
        default="all",
        help="Which split to download",
    )
    args = parser.parse_args()

    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("ERROR: huggingface_hub not installed. Run: pip install huggingface_hub", file=sys.stderr)
        return 1

    out_dir = Path(args.out)
    if out_dir.is_symlink():
        print(
            f"ERROR: {out_dir} is a symlink (pointing to {out_dir.resolve()}).\n"
            f"This is the developer setup where data is already on disk via the\n"
            f"benchmark_source/ staging area. Skip this script, or pass --out\n"
            f"to a different path if you actually need a fresh HuggingFace pull.",
            file=sys.stderr,
        )
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)

    allow_patterns = None
    if args.split == "val":
        allow_patterns = ["val/*", "validation/*", "*val*"]
    elif args.split == "test":
        allow_patterns = ["test/*", "*test*"]

    print(f"Downloading {HF_REPO_ID} -> {out_dir}")
    snapshot_download(
        repo_id=HF_REPO_ID,
        repo_type="dataset",
        local_dir=str(out_dir),
        allow_patterns=allow_patterns,
    )
    print(f"Done. Files are in: {out_dir.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
