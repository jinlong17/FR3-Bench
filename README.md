<h1 align="center">
  FR<sup>3</sup>
</h1>

<p align="center">
  <strong>End-to-End Financial Receipt Restoration and Reasoning from Degraded Images</strong><br>
  <em>The NTIRE 2026 Challenge at CVPR 2026 — Public Evaluation Kit</em>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/XXXX.XXXXX"><img alt="Paper" src="https://img.shields.io/badge/Paper-CVPR%202026-c41e3a?style=flat-square&logo=arxiv&logoColor=white"></a>
  <a href="https://huggingface.co/datasets/chickencaesar-yang/NTIRE_2026_Financial_Receipt"><img alt="Dataset" src="https://img.shields.io/badge/🤗%20Dataset-HuggingFace-ffd200?style=flat-square"></a>
  <a href="https://www.codabench.org/competitions/13606/"><img alt="CodaBench" src="https://img.shields.io/badge/CodaBench-Leaderboard-2ea043?style=flat-square&logo=docusign&logoColor=white"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/Code-MIT-555?style=flat-square"></a>
  <a href="LICENSE"><img alt="Data License" src="https://img.shields.io/badge/Data-CC%20BY%204.0-d97706?style=flat-square"></a>
</p>

<p align="center">
  📄 <a href="https://arxiv.org/abs/XXXX.XXXXX"><strong>Paper</strong></a> &nbsp;·&nbsp;
  🌐 <a href="project_page/index.html"><strong>Project Page</strong></a> &nbsp;·&nbsp;
  🤗 <a href="https://huggingface.co/datasets/chickencaesar-yang/NTIRE_2026_Financial_Receipt"><strong>Dataset</strong></a> &nbsp;·&nbsp;
  🏆 <a href="https://www.codabench.org/competitions/13606/"><strong>Leaderboard</strong></a>
</p>

---

## ✨ Why FR³?

Existing document restoration benchmarks measure pixel fidelity (PSNR / SSIM / LPIPS) but
do **not** tell us whether a restored document is actually usable for downstream financial
reasoning. **FR³ closes that gap**: each degraded receipt image is paired with a clean
reference *and* multi-step financial questions (sums, averages, ratios, percentiles, …).
A method is only as good as the numbers it lets a downstream LLM compute.

<table>
<tr>
<td align="center" width="33%">
  <h3>1,200</h3>
  <sub>Paired degraded ↔ clean<br>receipt images</sub>
</td>
<td align="center" width="33%">
  <h3>1,009</h3>
  <sub>Structured financial<br>QA pairs (108 val + 901 test)</sub>
</td>
<td align="center" width="33%">
  <h3>16</h3>
  <sub>Calculation types<br>(sum → interquartile_range)</sub>
</td>
</tr>
</table>

- Real physical printing + smartphone photography → realistic degradations
- Privacy-preserving — receipts hand-designed, never derived from real customer data
- 60+ teams registered for the inaugural NTIRE 2026 challenge

---

## 🚀 Quick Start

```bash
git clone https://github.com/jinlong17/FR3-Bench.git
cd FR3-Bench
pip install -r requirements.txt

# Pull the images from HuggingFace (~4.4 GB)
python data/download_data.py --out data/images

# Run QA evaluation on a sample submission
python evaluation/run_eval.py \
    --gt data/annotations/val_qa.json \
    --pred path/to/your_submission.json
```

---

## 📁 Repository Layout

```
FR3-Bench/
├── evaluation/         # QA + restoration evaluators (PSNR / SSIM / LPIPS)
├── data/
│   ├── annotations/    # val_qa.json (108), test_qa.json (901)
│   ├── images/         # Receipt images (HF download or symlink; gitignored)
│   └── download_data.py
├── tools/              # Visualization, sample submission utilities
├── configs/default.yaml
├── project_page/       # GitHub Pages site (open index.html in a browser)
├── EVALUATION.md       # Submission format and protocol
├── DATA.md             # Detailed data documentation
└── requirements.txt
```

> Public users pull images into `data/images/` via `download_data.py`.
> Developers in the FR3 monorepo have `data/images` symlinked to the local
> `benchmark_source/` staging area — no download needed.

---

## 🎯 The Two Coupled Tasks

| | Task | Metric |
|--|--|--|
| **1** | **Image Restoration** — recover a clean receipt image from a degraded one. | PSNR ↑ · SSIM ↑ · LPIPS ↓ |
| **2** | **Financial Reasoning** — multi-step numerical reasoning over restored image(s). | QA accuracy with 1% tolerance |

Final ranking is **primarily by reasoning accuracy** and complemented by restoration
metrics — pixel quality without downstream usability gets you nothing.

---

## 🏆 NTIRE 2026 Leaderboard

| Rank | Team | Accuracy ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|:-:|:-:|-:|-:|-:|-:|
| 🥇 | **Maltlab** | **0.6404** | 15.61 | 0.7009 | 0.2252 |
| 🥈 | **Shelden** | 0.6238 | 17.54 | 0.7270 | 0.2902 |
| 🥉 | **gogogochufalou** | 0.6215 | 18.80 | 0.7361 | 0.2671 |
| 4 | yufans | 0.6215 | 17.40 | 0.6845 | 0.2530 |
| 5 | VEPG | 0.5794 | **20.31** | **0.7620** | **0.1786** |
| 6 | IMAG2006 | 0.5683 | 17.99 | 0.7475 | 0.2111 |
| 7 | weichow | 0.5150 | 17.40 | 0.6845 | 0.2530 |
| 8 | se7enxf | 0.3052 | 18.93 | 0.7136 | 0.2330 |
| 9 | navjot_singh | 0.2253 | 13.91 | 0.6291 | 0.3227 |

> The team with the best restoration (VEPG, rank 5) achieves the highest PSNR / SSIM and
> lowest LPIPS — yet places only **5th** on reasoning accuracy. **Pixel fidelity ≠ usefulness.**

---

## 📚 Citation

```bibtex
@inproceedings{fr3_2026,
  title     = {NTIRE 2026 Challenge on End-to-End Financial Receipt Restoration
               and Reasoning from Degraded Images: Datasets, Methods and Results},
  author    = {... authors ...},
  booktitle = {CVPR Workshops (NTIRE)},
  year      = {2026}
}
```

---

## ⚖️ License

- **Code**: [MIT](LICENSE)
- **Dataset**: [CC BY 4.0](LICENSE)

<p align="center">
  <sub>Made with ☕ by the FR³ team · OPPO AI Center · University of Würzburg</sub>
</p>
