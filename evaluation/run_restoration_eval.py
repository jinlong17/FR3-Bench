#!/usr/bin/env python
"""Compute PSNR / SSIM / LPIPS between restored receipt images and ground-truth clean images.

Usage:
    python evaluation/run_restoration_eval.py \
        --pred-dir path/to/restored_images \
        --gt-dir path/to/clean_images \
        [--out restoration_scores.txt]

Both directories must contain matching filenames. Images are loaded as RGB and
normalized to [0, 1]. LPIPS is optional and only computed if the `lpips`
package and PyTorch are installed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from metrics import psnr, ssim


def _load_image(path: Path) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    return np.asarray(img, dtype=np.float32) / 255.0


def _try_lpips_loader():
    try:
        import torch  # noqa: F401
        import lpips  # noqa: F401
    except ImportError:
        return None
    import torch
    import lpips as _lpips

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = _lpips.LPIPS(net="alex").to(device).eval()

    def _lpips_fn(pred_np: np.ndarray, gt_np: np.ndarray) -> float:
        def _to_tensor(arr: np.ndarray):
            t = torch.from_numpy(arr).permute(2, 0, 1).unsqueeze(0).to(device)
            return t * 2.0 - 1.0  # LPIPS expects [-1, 1]
        with torch.no_grad():
            return float(model(_to_tensor(pred_np), _to_tensor(gt_np)).item())

    return _lpips_fn


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pred-dir", required=True, help="Directory of restored images")
    parser.add_argument("--gt-dir", required=True, help="Directory of ground-truth clean images")
    parser.add_argument("--out", default=None, help="Optional scores output file")
    parser.add_argument(
        "--ext",
        default=".jpg",
        help="Image extension to match (default .jpg)",
    )
    args = parser.parse_args()

    pred_dir = Path(args.pred_dir)
    gt_dir = Path(args.gt_dir)
    files = sorted(p.name for p in pred_dir.iterdir() if p.suffix.lower() == args.ext)
    if not files:
        print(f"No images with ext {args.ext} found in {pred_dir}")
        return 1

    lpips_fn = _try_lpips_loader()
    psnr_vals, ssim_vals, lpips_vals = [], [], []
    missing = []
    for name in files:
        gt_path = gt_dir / name
        if not gt_path.exists():
            missing.append(name)
            continue
        pred = _load_image(pred_dir / name)
        gt = _load_image(gt_path)
        if pred.shape != gt.shape:
            print(f"Skip {name}: shape mismatch {pred.shape} vs {gt.shape}")
            continue
        psnr_vals.append(psnr(pred, gt, data_range=1.0))
        ssim_vals.append(ssim(pred, gt))
        if lpips_fn:
            lpips_vals.append(lpips_fn(pred, gt))

    mean = lambda xs: float(np.mean(xs)) if xs else float("nan")
    result = {
        "PSNR": mean(psnr_vals),
        "SSIM": mean(ssim_vals),
        "LPIPS": mean(lpips_vals) if lpips_vals else None,
        "n_images": len(psnr_vals),
        "n_missing": len(missing),
    }

    print("=" * 60)
    print("FR3 Restoration Evaluation")
    print("=" * 60)
    print(f"PSNR  : {result['PSNR']:.4f} dB")
    print(f"SSIM  : {result['SSIM']:.4f}")
    if result["LPIPS"] is not None:
        print(f"LPIPS : {result['LPIPS']:.4f}")
    else:
        print("LPIPS : skipped (install `lpips` and `torch` to enable)")
    print(f"Images evaluated : {result['n_images']}")
    if missing:
        print(f"Missing GT pairs : {result['n_missing']} (first 5: {missing[:5]})")

    if args.out:
        with open(args.out, "w") as f:
            f.write(f"PSNR:{result['PSNR']:.6f}\n")
            f.write(f"SSIM:{result['SSIM']:.6f}\n")
            if result["LPIPS"] is not None:
                f.write(f"LPIPS:{result['LPIPS']:.6f}\n")
        print(f"Scores written to: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
