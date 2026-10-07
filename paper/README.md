# Paper Source

LaTeX source of the UAI 2026 paper (Paper ID 228), camera-ready version.

## Files

| File | Description |
|------|-------------|
| `uai2026-main-id228.tex` | Main paper and appendix in a single file (20 pages) |
| `uai2026.bib` | Bibliography |
| `uai2026.cls` | UAI 2026 document class |
| `fig_accuracy.pdf` | Figure 1: test accuracy versus label noise rate |
| `fig_concept_size.pdf` | Figure 2: concept size versus noise rate |
| `fig_runtime.pdf` | Figure 3: runtime (log scale) versus noise rate |
| `fig_ablation_convergence.pdf` | Figure 4: effect of s_max and convergence in the sample size |

The figure PDFs are copies of the files in `../figures/`. Regenerate them with `bash ../scripts/generate_figures.sh`.

## Building

```bash
pdflatex uai2026-main-id228
bibtex uai2026-main-id228
pdflatex uai2026-main-id228
pdflatex uai2026-main-id228
```

or, from the repository root, `bash scripts/build_paper.sh`.

## Structure

Page layout of the compiled PDF: main text on pages 1–9, references on pages 10–11, appendix table of contents on page 12, appendices on pages 13–20.

- **§1** Introduction
- **§2** Preliminaries (Description Logics, PAC Learning, Parameterized Complexity)
- **§3** The ApxFit Problem (Definitions 3.1 and 3.2, Proposition 3.3)
- **§4** Parameterized Complexity (Theorem 4.1: W[2]-hardness; Example 4.2; Theorem 4.3: XP membership; Table 1)
- **§5** MAX-SAT Algorithm with Structural Risk Minimization (Definition 5.1, Algorithm 1, Theorem 5.2: oracle inequality)
- **§6** Experiments (Tables 2 and 3, Figures 1–3; benchmarks: Family, Mutagenesis, Carcinogenesis, Vicodi)
- **§7** Conclusion and Future Work
- **App A** Proof of Theorem 4.1
- **App B** Proof of Theorem 5.2
- **App C** Concept Class Size and VC-Dimension Bounds (Lemma C.1, Corollary C.2, Proposition C.3, Remark C.4)
- **App D** Deferred Proofs (D.1 Proof of Proposition 3.3; D.2 Proof of Theorem 4.3; D.3 MAX-SAT Encoding Correctness; D.4 SRM Penalty Derivation; D.5 Sample Complexity from Finite Class Bound)
- **App E** Additional Experimental Results (E.1 Benchmark Details; E.2 Implementation and Hyperparameter Details; E.3 Full Numerical Results, Table 4; E.4 Statistical Significance Tests, Table 5; E.5 MAX-SAT Instance Statistics, Table 6; E.6 Ablation and Convergence Analysis, Figure 4 and Table 7; E.7 Qualitative Analysis of Learned Concepts, Table 8)
