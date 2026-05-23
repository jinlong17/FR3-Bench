#!/usr/bin/env python
"""Quick visual sanity check of FR3 examples.

Picks a QA pair from val_qa.json or test_qa.json, prints the question and
ground-truth answer (when available), and shows the first few referenced
receipt images side-by-side.

Usage:
    python tools/visualize.py --split val --index 0
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=["val", "test"], default="val")
    parser.add_argument("--index", type=int, default=0, help="QA pair index")
    parser.add_argument(
        "--images-root",
        default="data/images",
        help="Where images were downloaded (default: data/images)",
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=4,
        help="How many referenced images to display",
    )
    args = parser.parse_args()

    annot = Path("data/annotations") / f"{args.split}_qa.json"
    with open(annot) as f:
        pairs = json.load(f)
    if not 0 <= args.index < len(pairs):
        print(f"Index out of range: {args.index} (0..{len(pairs) - 1})", file=sys.stderr)
        return 1
    qa = pairs[args.index]

    print(f"[{args.split}] index {args.index} of {len(pairs)}")
    print(f"Q: {qa['question']}")
    if qa.get("answer") not in (None, ""):
        print(f"A: {qa['answer']}")
    if "metadata" in qa:
        print(f"Meta: {qa['metadata']}")
    print(f"image_list size: {len(qa['image_list'])}")
    print(f"Showing first {min(args.max_images, len(qa['image_list']))} images:")
    for name in qa["image_list"][: args.max_images]:
        print(f"  - {Path(args.images_root) / name}")

    try:
        import matplotlib.pyplot as plt
        from PIL import Image
    except ImportError:
        print("(matplotlib / PIL not installed — printing paths only)")
        return 0

    n = min(args.max_images, len(qa["image_list"]))
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 6))
    axes = [axes] if n == 1 else axes
    for ax, name in zip(axes, qa["image_list"][:n]):
        path = Path(args.images_root) / name
        if path.exists():
            ax.imshow(Image.open(path))
        ax.set_title(name, fontsize=9)
        ax.axis("off")
    fig.suptitle(qa["question"][:80], fontsize=10)
    plt.tight_layout()
    plt.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
