<div align="center">

# When Can We Learn from Noisy Logical Data?

### Parameterized Complexity of Approximate Concept Fitting in Description Logics

**Chang Lu** (Yale University) &nbsp;·&nbsp; **Yizheng Zhao** (Nanjing University) &nbsp;·&nbsp; **Renate A. Schmidt** (The University of Manchester)

**UAI 2026 &nbsp;·&nbsp; Paper ID 228**

[![LaTeX](https://img.shields.io/badge/Built%20with-LaTeX-008080?logo=latex&logoColor=white)](https://www.latex-project.org/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Figures: 1200 DPI](https://img.shields.io/badge/Figures-1200%20DPI-critical)](figures/)

</div>

---

## Overview

SAT-based bounded fitting (finding a smallest concept that correctly classifies all given examples) yields sample-efficient PAC learning for description logic (DL) concepts.
Yet the paradigm is **brittle**: it demands realizability, and a single mislabeled example can render the SAT formula unsatisfiable.
Learning without this assumption (agnostic learning) is statistically possible for bounded-size classes; the real barrier is **computational**: minimizing misclassifications over bounded-size concepts is NP-hard.

We introduce **ApxFit(_k_, _t_)**, asking whether a DL concept of size at most _k_ misclassifies at most _t_ examples, and chart the complexity landscape for fragments of 𝒜ℒ𝒞 whose operator sets contain conjunction and existential restriction ({⊓, ∃}) or, dually, {⊔, ∀}:

<div align="center">

| Parameter | Complexity | Reference |
|:----------|:-----------|:----------|
| _k_ (concept size) | **W[2]-hard**; in XP | Theorem 4.1 |
| _t_ (outlier count) | not in XP unless P = NP | Proposition 3.3 (_t_ = 0) |
| _t_ (outlier count), _k_ fixed | **in XP**; FPT open | Theorem 4.3 |
| (_k_, _t_) jointly | W[2]-hard | Theorem 4.1 (_t_ = 0) |

</div>

Hardness entries assume {⊓, ∃} ⊆ _O_ or {⊔, ∀} ⊆ _O_; membership entries hold for every operator set _O_ (Table 1 of the paper).

Algorithmically, we lift bounded fitting from SAT to **partial weighted MAX-SAT** and combine it with **structural risk minimization (SRM)**. The resulting algorithm, SRM-MaxSAT, satisfies an oracle inequality (Theorem 5.2) that adapts to the unknown optimal size and noise rate, yielding the first noise-tolerant DL concept learner with formal agnostic PAC guarantees.

---

## Experimental Highlights

We use four standard concept learning benchmarks with symmetric label noise injected at rates η ∈ {0, 5, 10, 15, 20, 30}% (_m_ = 200 training examples, 100 clean held-out test examples, 5 random seeds).
SRM-MaxSAT achieves the highest accuracy at every noise rate on every benchmark, leading the best heuristic baseline by 10–13 percentage points at η = 30%.

<div align="center">

**Test accuracy on the Family benchmark** (mean over 5 seeds; excerpt of Table 3)

| η | SRM-MaxSAT | SPELL | DL-Learner | EvoLearner | NCES |
|:-:|:----------:|:-----:|:----------:|:----------:|:----:|
| 0% | **.97** | **.97** | .94 | .91 | .88 |
| 10% | **.93** | .45 | .87 | .83 | .79 |
| 20% | **.87** | .23 | .77 | .72 | .66 |
| 30% | **.79** | .16 | .66 | .60 | .54 |

</div>

Key observations:
- At η = 0%, SRM-MaxSAT matches SPELL (the two return identical SAT solutions), so the MAX-SAT formulation introduces no penalty in the realizable setting.
- At η = 10%, SPELL's accuracy drops to 0.45 or below on all benchmarks, while SRM-MaxSAT retains accuracy of 0.85 or above.
- DL-Learner and EvoLearner degrade more gradually than SPELL but trail SRM-MaxSAT by 6–11 percentage points at η = 10%.
- SRM-MaxSAT selects compact concepts (‖_C_‖ ≤ 12 across all settings), whereas SPELL's attempted concept size exceeds 15 at η = 10% and 20 at η = 20% before timing out.
- SRM-MaxSAT's runtime stays under 300 seconds even at η = 30% on the largest benchmark (Vicodi, 33,238 individuals).

---

## Benchmarks

The four benchmarks span three domains (kinship, chemistry, European history), a 160× range in knowledge base size, and 𝒜ℒ𝒞 / 𝒜ℒ𝒞(𝒟) (with datatypes) expressiveness (Table 2 of the paper):

<div align="center">

| Benchmark | Domain | \|Σ\_C\| | \|Σ\_R\| | Individuals | Axioms |
|:---------:|:------:|:--------:|:--------:|:-----------:|:------:|
| **Family** | Kinship | 18 | 4 | 202 | 1,829 |
| **Mutagenesis** | Chemistry | 86 | 5 | 14,145 | 62,066 |
| **Carcinogenesis** | Chemistry | 142 | 4 | 22,372 | 74,566 |
| **Vicodi** | European history | 194 | 10 | 33,238 | ~116,000 |

</div>

All four are available from the Ontolearn framework: <https://files.dice-research.org/projects/Ontolearn/KGs.zip>.

---

## Repository Structure

```
uai2026-apxfit/
├── paper/                              # LaTeX source (camera-ready version)
│   ├── uai2026-main-id228.tex          # Main paper + appendix, single file
│   ├── uai2026.bib                     # Bibliography
│   ├── uai2026.cls                     # UAI 2026 document class
│   ├── fig_*.pdf                       # Figures included by the paper
│   └── README.md
│
├── figures/
│   ├── src/
│   │   └── generate_all_figures.py     # Single script producing Figures 1-4
│   └── fig_*.pdf                       # Generated figures (1200 DPI)
│
├── experiments/
│   └── data_tables.py                  # All reported numbers (Tables 2-8, Figures 1-4)
│
├── scripts/
│   ├── build_paper.sh                  # One-command paper compilation
│   ├── generate_figures.sh             # One-command figure generation
│   └── check_consistency.py            # Checks repository contents against the paper
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

This repository contains the paper source, the plotting code, and the reported numbers in structured form.

---

## Quick Start

### Prerequisites

- **LaTeX**: `pdflatex` and `bibtex` (tested with TeX Live 2023)
- **Python**: 3.10+ with the packages in `requirements.txt` (`numpy`, `matplotlib`)

```bash
pip install -r requirements.txt
```

### Generate Figures & Build Paper

```bash
# Generate all figures (saved as PDF in figures/ and copied to paper/)
bash scripts/generate_figures.sh

# Compile the paper (runs the pdflatex + bibtex cycle and reports errors)
bash scripts/build_paper.sh

# Check that data, figure script and README agree with the paper
python3 scripts/check_consistency.py
```

### Manual figure generation

```bash
cd figures
python3 src/generate_all_figures.py              # all four figures
python3 src/generate_all_figures.py accuracy     # Figure 1 -> fig_accuracy.pdf
python3 src/generate_all_figures.py concept_size # Figure 2 -> fig_concept_size.pdf
python3 src/generate_all_figures.py runtime      # Figure 3 -> fig_runtime.pdf
python3 src/generate_all_figures.py ablation     # Figure 4 -> fig_ablation_convergence.pdf
```

Notes on the figures:
- The accuracy curves of Figure 1 and the F1 curves of Figure 4(a) are drawn with a small fixed-seed Gaussian display jitter (σ = 0.005 and 0.003, seed 42), so a plotted point can differ from the tabulated mean by up to about 0.013. The exact values are those of Tables 3 and 4 and of `experiments/data_tables.py`.
- The PDFs in this repository were rendered with Matplotlib 3.10.8 (pinned in `requirements.txt`) and the DejaVu fonts bundled with Matplotlib, which the script falls back to when Times New Roman is not installed. In that setting the script reproduces them pixel for pixel; other versions or fonts give visually equivalent figures with slightly different bounding boxes.

---

## Key Theoretical Results

### Complexity Landscape

- **Statistical–computational separation** (Proposition 3.3): for every operator set _O_ containing ∃ or ∀, the class of concepts of size at most _k_ is agnostic PAC learnable with sample complexity _O_((_k_ log|Σ| + log(1/δ)) / ε²), yet ApxFit(_k_, _t_) is NP-complete, even for fixed _t_ = 0.
- **W[2]-hardness** (Theorem 4.1): ApxFit(_k_, _t_) is W[2]-hard parameterized by _k_, for every operator set _O_ with {⊓, ∃} ⊆ _O_ or {⊔, ∀} ⊆ _O_. Hardness holds even for _t_ = 0 and with Σ\_C = ∅.
- **XP membership** (Theorem 4.3): for any fixed _k_ and any operator set _O_ ⊆ {⊓, ⊔, ¬, ∃, ∀}, ApxFit(_k_, _t_) parameterized by _t_ is in XP. It can be solved in time _O_(_m_^_t_ · _p_(_N_)), where _m_ is the number of examples, _N_ the total input size, and _p_ a polynomial whose degree depends on _k_.

### SRM-MaxSAT Oracle Inequality

For each candidate size _s_ = 1, …, _s_\_max, SRM-MaxSAT (Algorithm 1) solves the partial weighted MAX-SAT instance Ψ(_s_, _E_) of Definition 5.1, which yields an empirical risk minimizer over concepts of size at most _s_, and returns the concept that minimizes empirical risk plus the penalty √(2(_s_ log|Σ| + log(2 _s_\_max / δ)) / _m_). Theorem 5.2 guarantees that, with probability at least 1 − δ,

> _R_(Ĉ) ≤ min\_{1 ≤ s ≤ s\_max} { R\*\_s + 2√(2(s log|Σ| + log(2 s\_max / δ)) / m) }

where R\*\_s is the optimal true risk achievable by concepts of size at most _s_.

---

## Citation

```bibtex
@inproceedings{lu2026apxfit,
  title     = {When Can We Learn from Noisy Logical Data?
               Parameterized Complexity of Approximate Concept
               Fitting in Description Logics},
  author    = {Lu, Chang and Zhao, Yizheng and Schmidt, Renate A.},
  booktitle = {Proceedings of the 42nd Conference on Uncertainty
               in Artificial Intelligence (UAI)},
  year      = {2026}
}
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
