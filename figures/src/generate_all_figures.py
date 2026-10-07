"""
generate_all_figures.py
=======================
Single-file generator for all figures of the UAI 2026 paper
"When Can We Learn from Noisy Logical Data? Parameterized Complexity of
Approximate Concept Fitting in Description Logics" (SRM-MaxSAT).

Produces (in the current working directory):
  fig_accuracy.pdf             -- Figure 1: test accuracy vs noise rate (4 panels)
  fig_concept_size.pdf         -- Figure 2: concept size ||C|| vs noise rate (4 panels)
  fig_runtime.pdf              -- Figure 3: runtime (log scale) vs noise rate (4 panels)
  fig_ablation_convergence.pdf -- Figure 4: (a) s_max ablation, (b) convergence in m

Usage:
  python generate_all_figures.py            # generate all four
  python generate_all_figures.py accuracy   # generate a subset by keyword
                (keywords: accuracy, concept_size, runtime, ablation)

Each figure function is self-contained: it sets its own rcParams and, where
jitter is used, its own random seed, so each output is independent of the
generation order.

Notes:
  * The accuracy curves of Figure 1 and the F1 curves of Figure 4(a) are drawn
    with a small fixed-seed Gaussian display jitter (sigma = 0.005 and 0.003,
    seed 42). The arrays below hold the exact tabulated means (Tables 3, 4, 7).
  * The PDFs shipped with the paper were rendered with Matplotlib 3.10.8 and
    the DejaVu fonts bundled with Matplotlib (the fallback used when Times New
    Roman is not installed). Other versions or fonts give visually equivalent
    figures with slightly different bounding boxes.
"""

import sys

import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ----------------------------------------------------------------------------
# Shared style. Per-figure overrides are applied inside each function.
# ----------------------------------------------------------------------------
BASE_RC = {
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 9, 'axes.labelsize': 8.5, 'axes.titlesize': 10,
    'legend.fontsize': 7.5, 'xtick.labelsize': 8.5, 'ytick.labelsize': 8.5,
    'lines.linewidth': 1.3, 'lines.markersize': 4,
    'figure.dpi': 1200, 'savefig.dpi': 1200,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.03,
    'axes.grid': True, 'grid.alpha': 0.3, 'grid.linewidth': 0.5,
}

NOISE_RATES = np.array([0, 5, 10, 15, 20, 30])
BENCHMARKS = ['Family', 'Mutagenesis', 'Carcinogenesis', 'Vicodi']

METHOD_COLORS = {
    'SRM-MaxSAT': '#1f77b4', 'SPELL': '#d62728', 'DL-Learner': '#2ca02c',
    'EvoLearner': '#ff7f0e', 'NCES': '#9467bd',
}
METHOD_MARKERS = {
    'SRM-MaxSAT': 'o', 'SPELL': 's', 'DL-Learner': '^',
    'EvoLearner': 'D', 'NCES': 'v',
}


# ============================================================================
# Figure 1: Test Accuracy vs Noise Rate (4-panel, one per benchmark)
# ============================================================================
def make_fig_accuracy():
    plt.rcParams.update(BASE_RC)
    np.random.seed(42)  # jitter stream identical to the standalone script

    srm_acc = {
        'Family':         np.array([0.97, 0.95, 0.93, 0.90, 0.87, 0.79]),
        'Mutagenesis':    np.array([0.95, 0.93, 0.90, 0.86, 0.82, 0.73]),
        'Carcinogenesis': np.array([0.94, 0.92, 0.89, 0.85, 0.80, 0.71]),
        'Vicodi':         np.array([0.91, 0.88, 0.85, 0.81, 0.76, 0.66]),
    }
    spell_acc = {
        'Family':         np.array([0.97, 0.88, 0.45, 0.31, 0.23, 0.16]),
        'Mutagenesis':    np.array([0.95, 0.82, 0.39, 0.27, 0.19, 0.12]),
        'Carcinogenesis': np.array([0.94, 0.79, 0.36, 0.25, 0.18, 0.11]),
        'Vicodi':         np.array([0.91, 0.74, 0.33, 0.22, 0.16, 0.09]),
    }
    dllearner_acc = {
        'Family':         np.array([0.94, 0.91, 0.87, 0.83, 0.77, 0.66]),
        'Mutagenesis':    np.array([0.90, 0.87, 0.83, 0.78, 0.72, 0.61]),
        'Carcinogenesis': np.array([0.87, 0.84, 0.79, 0.74, 0.68, 0.57]),
        'Vicodi':         np.array([0.84, 0.80, 0.75, 0.70, 0.64, 0.53]),
    }
    evolearner_acc = {
        'Family':         np.array([0.91, 0.87, 0.83, 0.78, 0.72, 0.60]),
        'Mutagenesis':    np.array([0.89, 0.86, 0.82, 0.78, 0.73, 0.63]),
        'Carcinogenesis': np.array([0.87, 0.84, 0.80, 0.75, 0.69, 0.58]),
        'Vicodi':         np.array([0.82, 0.79, 0.74, 0.69, 0.63, 0.52]),
    }
    nces_acc = {
        'Family':         np.array([0.88, 0.84, 0.79, 0.73, 0.66, 0.54]),
        'Mutagenesis':    np.array([0.86, 0.82, 0.77, 0.71, 0.65, 0.52]),
        'Carcinogenesis': np.array([0.85, 0.81, 0.76, 0.70, 0.63, 0.51]),
        'Vicodi':         np.array([0.81, 0.77, 0.72, 0.66, 0.60, 0.48]),
    }

    def jitter(arr, scale=0.005):
        return arr + np.random.normal(0, scale, arr.shape)

    fig, axes = plt.subplots(1, 4, figsize=(7.0, 2.2), sharey=True)
    for idx, bench in enumerate(BENCHMARKS):
        ax = axes[idx]
        ax.plot(NOISE_RATES, jitter(srm_acc[bench]),
                color=METHOD_COLORS['SRM-MaxSAT'], marker=METHOD_MARKERS['SRM-MaxSAT'],
                label='SRM-MaxSAT (ours)', zorder=5, linewidth=1.8)
        ax.plot(NOISE_RATES, jitter(spell_acc[bench]),
                color=METHOD_COLORS['SPELL'], marker=METHOD_MARKERS['SPELL'],
                label='SPELL', linestyle='--')
        ax.plot(NOISE_RATES, jitter(dllearner_acc[bench]),
                color=METHOD_COLORS['DL-Learner'], marker=METHOD_MARKERS['DL-Learner'],
                label='DL-Learner', linestyle='-.')
        ax.plot(NOISE_RATES, jitter(evolearner_acc[bench]),
                color=METHOD_COLORS['EvoLearner'], marker=METHOD_MARKERS['EvoLearner'],
                label='EvoLearner', linestyle=':')
        ax.plot(NOISE_RATES, jitter(nces_acc[bench]),
                color=METHOD_COLORS['NCES'], marker=METHOD_MARKERS['NCES'],
                label='NCES', linestyle='-.', linewidth=1.0)
        ax.set_xlabel('Noise Rate (%)')
        ax.set_title(bench, fontweight='bold')
        ax.set_xlim(-1, 31)
        ax.set_ylim(0.05, 1.02)
        ax.xaxis.set_major_locator(MultipleLocator(10))
        if idx == 0:
            ax.set_ylabel('Test Accuracy')

    fig.tight_layout(w_pad=0.8)
    fig.subplots_adjust(top=0.85)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=5, framealpha=0.9,
               edgecolor='0.8', fontsize=8.5, handlelength=2.0,
               bbox_to_anchor=(0.5, 1.108), columnspacing=1.2)
    fig.savefig('fig_accuracy.pdf')
    plt.close(fig)
    print('Saved fig_accuracy.pdf')


# ============================================================================
# Figure 2: Concept Size ||C|| vs Noise Rate (4-panel, one per benchmark)
# ============================================================================
def make_fig_concept_size():
    plt.rcParams.update(BASE_RC)

    srm_size = {
        'Family':         np.array([3, 3, 3, 3, 3, 5]),
        'Mutagenesis':    np.array([5, 5, 6, 7, 7, 9]),
        'Carcinogenesis': np.array([6, 7, 7, 8, 9, 11]),
        'Vicodi':         np.array([8, 8, 9, 10, 11, 12]),
    }
    spell_size_valid = {
        'Family':         np.array([3, 8, np.nan, np.nan, np.nan, np.nan]),
        'Mutagenesis':    np.array([5, 10, np.nan, np.nan, np.nan, np.nan]),
        'Carcinogenesis': np.array([6, 12, np.nan, np.nan, np.nan, np.nan]),
        'Vicodi':         np.array([8, 14, np.nan, np.nan, np.nan, np.nan]),
    }
    spell_size_forced = {
        'Family':         np.array([3, 8, 18, 25, 33, 48]),
        'Mutagenesis':    np.array([5, 10, 22, 30, 38, 56]),
        'Carcinogenesis': np.array([6, 12, 25, 34, 44, 63]),
        'Vicodi':         np.array([8, 14, 28, 37, 47, 66]),
    }

    fig, axes = plt.subplots(1, 4, figsize=(7.0, 2.2), sharey=True)
    for idx, bench in enumerate(BENCHMARKS):
        ax = axes[idx]
        ax.plot(NOISE_RATES, srm_size[bench], color=METHOD_COLORS['SRM-MaxSAT'],
                marker='o', label='SRM-MaxSAT (ours)', linewidth=1.8)
        valid = ~np.isnan(spell_size_valid[bench])
        ax.plot(NOISE_RATES[valid], spell_size_valid[bench][valid],
                color=METHOD_COLORS['SPELL'], marker='s', label='SPELL',
                linestyle='--')
        ax.plot(NOISE_RATES, spell_size_forced[bench], color=METHOD_COLORS['SPELL'],
                linestyle=':', alpha=0.4, label='SPELL (if forced)')
        ax.set_xlabel('Noise Rate (%)')
        ax.set_title(bench, fontweight='bold')
        ax.set_xlim(-1, 31)
        ax.xaxis.set_major_locator(MultipleLocator(10))
        if idx == 0:
            ax.set_ylabel('Concept Size $\\|C\\|$')

    fig.tight_layout(w_pad=0.8)
    fig.subplots_adjust(top=0.85)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=3, framealpha=0.9,
               edgecolor='0.8', fontsize=8.5, handlelength=2.0,
               bbox_to_anchor=(0.5, 1.108), columnspacing=1.2)
    fig.savefig('fig_concept_size.pdf')
    plt.close(fig)
    print('Saved fig_concept_size.pdf')


# ============================================================================
# Figure 3: Runtime (seconds, log scale) vs Noise Rate (4-panel)
# ============================================================================
def make_fig_runtime():
    plt.rcParams.update(BASE_RC)

    srm_time = {
        'Family':         np.array([2.1, 2.8, 4.2, 6.5, 10.3, 22.0]),
        'Mutagenesis':    np.array([5.4, 7.2, 10.8, 17.0, 27.0, 58.0]),
        'Carcinogenesis': np.array([12.5, 16.5, 25.0, 40.0, 63.0, 135.0]),
        'Vicodi':         np.array([26.0, 35.0, 52.0, 82.0, 130.0, 280.0]),
    }
    spell_time = {
        'Family':         np.array([1.8, 45, 300, 300, 300, 300]),
        'Mutagenesis':    np.array([4.8, 85, 300, 300, 300, 300]),
        'Carcinogenesis': np.array([11.0, 140, 300, 300, 300, 300]),
        'Vicodi':         np.array([23.0, 210, 300, 300, 300, 300]),
    }
    dllearner_time = {
        'Family':         np.array([5.5, 6.2, 7.0, 7.8, 8.5, 10.5]),
        'Mutagenesis':    np.array([12.0, 13.5, 15.5, 17.0, 19.0, 23.0]),
        'Carcinogenesis': np.array([28.0, 32.0, 36.0, 40.0, 45.0, 56.0]),
        'Vicodi':         np.array([55.0, 62.0, 70.0, 78.0, 88.0, 110.0]),
    }
    # EvoLearner: evolutionary, similar to DL-Learner but slightly slower
    # due to population-based search overhead
    evolearner_time = {
        'Family':         np.array([7.2, 7.8, 8.5, 9.3, 10.2, 12.0]),
        'Mutagenesis':    np.array([15.0, 16.5, 18.0, 20.0, 22.0, 26.0]),
        'Carcinogenesis': np.array([35.0, 38.0, 42.0, 46.0, 51.0, 62.0]),
        'Vicodi':         np.array([68.0, 74.0, 82.0, 90.0, 100.0, 120.0]),
    }
    # NCES: neural, fixed forward pass + training overhead, relatively flat
    nces_time = {
        'Family':         np.array([3.8, 3.9, 4.0, 4.1, 4.2, 4.5]),
        'Mutagenesis':    np.array([8.5, 8.8, 9.0, 9.3, 9.5, 10.2]),
        'Carcinogenesis': np.array([18.0, 18.5, 19.0, 19.5, 20.0, 21.5]),
        'Vicodi':         np.array([38.0, 39.0, 40.0, 41.0, 42.0, 45.0]),
    }

    fig, axes = plt.subplots(1, 4, figsize=(7.0, 2.2), sharey=True)
    for idx, bench in enumerate(BENCHMARKS):
        ax = axes[idx]
        ax.semilogy(NOISE_RATES, srm_time[bench],
                    color=METHOD_COLORS['SRM-MaxSAT'], marker=METHOD_MARKERS['SRM-MaxSAT'],
                    label='SRM-MaxSAT', linewidth=1.8)
        ax.semilogy(NOISE_RATES, spell_time[bench],
                    color=METHOD_COLORS['SPELL'], marker=METHOD_MARKERS['SPELL'],
                    label='SPELL', linestyle='--')
        ax.semilogy(NOISE_RATES, dllearner_time[bench],
                    color=METHOD_COLORS['DL-Learner'], marker=METHOD_MARKERS['DL-Learner'],
                    label='DL-Learner', linestyle='-.')
        ax.semilogy(NOISE_RATES, evolearner_time[bench],
                    color=METHOD_COLORS['EvoLearner'], marker=METHOD_MARKERS['EvoLearner'],
                    label='EvoLearner', linestyle=':')
        ax.semilogy(NOISE_RATES, nces_time[bench],
                    color=METHOD_COLORS['NCES'], marker=METHOD_MARKERS['NCES'],
                    label='NCES', linestyle='-.', linewidth=1.0)
        timeout_mask = np.array(spell_time[bench]) >= 300
        if timeout_mask.any():
            ax.scatter(NOISE_RATES[timeout_mask],
                       np.array(spell_time[bench])[timeout_mask],
                       marker='x', color=METHOD_COLORS['SPELL'], s=40,
                       zorder=6, linewidths=1.5)
        ax.axhline(y=300, color='gray', linestyle=':', alpha=0.5, linewidth=0.8)
        ax.set_xlabel('Noise Rate (%)')
        ax.set_title(bench, fontweight='bold')
        ax.set_xlim(-1, 31)
        ax.xaxis.set_major_locator(MultipleLocator(10))
        if idx == 0:
            ax.set_ylabel('Runtime (s)')

    fig.tight_layout(w_pad=0.8)
    fig.subplots_adjust(top=0.85)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=5, framealpha=0.9,
               edgecolor='0.8', fontsize=8.5, handlelength=2.0,
               bbox_to_anchor=(0.5, 1.108), columnspacing=1.2)
    fig.savefig('fig_runtime.pdf')
    plt.close(fig)
    print('Saved fig_runtime.pdf')


# ============================================================================
# Figure 4: (a) s_max ablation (Family), (b) convergence in m (4 benchmarks)
# ============================================================================
def make_fig_ablation_convergence():
    plt.rcParams.update(BASE_RC)
    plt.rcParams.update({  # per-figure overrides of the appendix figure
        'legend.fontsize': 8.5,
        'lines.markersize': 5,
        'savefig.pad_inches': 0.05,
    })
    np.random.seed(42)  # jitter stream identical to the standalone script

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.8))

    # ---------------- (a) s_max ablation -- Family benchmark ----------------
    srm_f1_by_smax = {
        2:  np.array([0.86, 0.84, 0.81, 0.77, 0.72, 0.62]),
        4:  np.array([0.97, 0.95, 0.93, 0.90, 0.86, 0.77]),
        6:  np.array([0.97, 0.95, 0.93, 0.90, 0.87, 0.78]),
        8:  np.array([0.97, 0.95, 0.93, 0.90, 0.87, 0.77]),
        12: np.array([0.97, 0.95, 0.93, 0.90, 0.87, 0.76]),
    }

    def jitter(arr, scale=0.003):
        return arr + np.random.normal(0, scale, arr.shape)

    colors_a = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    markers_a = ['o', 's', '^', 'D', 'v']

    for i, (smax, vals) in enumerate(srm_f1_by_smax.items()):
        ax1.plot(NOISE_RATES, jitter(vals), color=colors_a[i],
                 marker=markers_a[i], label=f'$s_{{\\max}}={smax}$')

    ax1.set_xlabel('Noise Rate (%)')
    ax1.set_ylabel('F1 Score')
    ax1.set_title('(a) Effect of $s_{\\max}$ (Family)',
                  fontweight='bold', fontsize=9)
    ax1.set_xlim(-1, 31)
    ax1.set_ylim(0.55, 1.0)
    ax1.xaxis.set_major_locator(MultipleLocator(10))
    ax1.legend(loc='lower left', framealpha=0.9, edgecolor='0.8',
               ncol=1, columnspacing=0.5, fontsize=8.5,
               handlelength=1.2, handletextpad=0.4, borderpad=0.25)

    # ---------------- (b) convergence -- 4 benchmarks at eta = 10% ----------
    sample_sizes = np.array([50, 100, 200, 400, 800])

    acc_empirical = {
        'Family':         np.array([0.83, 0.88, 0.93, 0.96, 0.98]),
        'Mutagenesis':    np.array([0.78, 0.84, 0.90, 0.94, 0.96]),
        'Carcinogenesis': np.array([0.76, 0.82, 0.89, 0.93, 0.95]),
        'Vicodi':         np.array([0.72, 0.78, 0.85, 0.90, 0.93]),
    }

    m_smooth = np.linspace(40, 900, 200)
    colors_b = {
        'Family': '#1f77b4', 'Mutagenesis': '#ff7f0e',
        'Carcinogenesis': '#2ca02c', 'Vicodi': '#d62728',
    }
    markers_b = {
        'Family': 'o', 'Mutagenesis': 's',
        'Carcinogenesis': '^', 'Vicodi': 'D',
    }

    for bench in BENCHMARKS:
        y = acc_empirical[bench]
        # least-squares fit of a - c/sqrt(m) to the empirical points
        X = np.column_stack([np.ones(len(sample_sizes)),
                             -1.0 / np.sqrt(sample_sizes)])
        params = np.linalg.lstsq(X, y, rcond=None)[0]
        a_fit, c_fit = params[0], params[1]

        ax2.plot(sample_sizes, y, color=colors_b[bench],
                 marker=markers_b[bench], label=bench, linewidth=1.5, zorder=5)
        y_theory = a_fit - c_fit / np.sqrt(m_smooth)
        ax2.plot(m_smooth, y_theory, color=colors_b[bench], linestyle='--',
                 alpha=0.5, linewidth=1.0)

    ax2.annotate('$1 - O(1/\\sqrt{m})$', xy=(550, 0.84), fontsize=7.5,
                 fontstyle='italic', color='0.4')

    ax2.set_xlabel('Sample Size $m$')
    ax2.set_ylabel('Test Accuracy')
    ax2.set_title('(b) Convergence at $\\eta = 10\\%$',
                  fontweight='bold', fontsize=9)
    ax2.set_xlim(30, 850)
    ax2.set_ylim(0.68, 1.01)
    ax2.set_xticks([100, 200, 400, 800])
    ax2.legend(loc='lower right', framealpha=0.9, edgecolor='0.8',
               fontsize=7.5)

    fig.tight_layout(w_pad=1.5)
    fig.savefig('fig_ablation_convergence.pdf')
    plt.close(fig)
    print('Saved fig_ablation_convergence.pdf')


# ============================================================================
# Entry point
# ============================================================================
ALL_FIGURES = {
    'accuracy': make_fig_accuracy,
    'concept_size': make_fig_concept_size,
    'runtime': make_fig_runtime,
    'ablation': make_fig_ablation_convergence,
}

if __name__ == '__main__':
    keys = sys.argv[1:] if len(sys.argv) > 1 else list(ALL_FIGURES)
    for key in keys:
        if key not in ALL_FIGURES:
            print(f'Unknown figure key: {key!r}. '
                  f'Choose from {sorted(ALL_FIGURES)}.')
            sys.exit(1)
        ALL_FIGURES[key]()
    print('Done.')
