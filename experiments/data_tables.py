"""
Structured experimental data for the UAI 2026 paper
"When Can We Learn from Noisy Logical Data? Parameterized Complexity of
Approximate Concept Fitting in Description Logics" (SRM-MaxSAT).

Every value below is the number reported in the paper. Table and figure
numbers refer to the camera-ready version in paper/uai2026-main-id228.tex.
Run this file directly for a few internal sanity checks, and run
scripts/check_consistency.py to compare it against the LaTeX source, the
figure script and the README.
"""

# ── Experimental protocol (Section 6, Appendix E.2) ───────────────────────
NOISE_RATES = [0, 5, 10, 15, 20, 30]          # eta, in percent
BENCHMARKS = ['Family', 'Mutagenesis', 'Carcinogenesis', 'Vicodi']
METHODS = ['SRM-MaxSAT', 'SPELL', 'DL-Learner', 'EvoLearner', 'NCES']

NUM_TRAIN_EXAMPLES = 200                      # m
NUM_TEST_EXAMPLES = 100                       # clean, held out
NUM_SEEDS = 5                                 # seeds 0-4
S_MAX = 12                                    # maximum candidate size
DELTA = 0.05                                  # failure probability
SPELL_TIMEOUT_SECONDS = 300

# ── Table 2: Benchmark statistics ─────────────────────────────────────────
# Vicodi's axiom count is reported as approximate (~116,000) in the paper.
BENCHMARK_STATS = {
    'Family':         {'sig_c': 18,  'sig_r': 4,  'individuals': 202,    'axioms': 1_829,   'axioms_approximate': False},
    'Mutagenesis':    {'sig_c': 86,  'sig_r': 5,  'individuals': 14_145, 'axioms': 62_066,  'axioms_approximate': False},
    'Carcinogenesis': {'sig_c': 142, 'sig_r': 4,  'individuals': 22_372, 'axioms': 74_566,  'axioms_approximate': False},
    'Vicodi':         {'sig_c': 194, 'sig_r': 10, 'individuals': 33_238, 'axioms': 116_000, 'axioms_approximate': True},
}

# ── Figure 1, Table 3, Table 4: Test accuracy (mean over 5 seeds) ─────────
# Table 3 reports the columns eta in {0, 10, 20, 30}; Table 4 reports all six.
ACCURACY = {
    'SRM-MaxSAT': {
        'Family':         [0.97, 0.95, 0.93, 0.90, 0.87, 0.79],
        'Mutagenesis':    [0.95, 0.93, 0.90, 0.86, 0.82, 0.73],
        'Carcinogenesis': [0.94, 0.92, 0.89, 0.85, 0.80, 0.71],
        'Vicodi':         [0.91, 0.88, 0.85, 0.81, 0.76, 0.66],
    },
    'SPELL': {
        'Family':         [0.97, 0.88, 0.45, 0.31, 0.23, 0.16],
        'Mutagenesis':    [0.95, 0.82, 0.39, 0.27, 0.19, 0.12],
        'Carcinogenesis': [0.94, 0.79, 0.36, 0.25, 0.18, 0.11],
        'Vicodi':         [0.91, 0.74, 0.33, 0.22, 0.16, 0.09],
    },
    'DL-Learner': {
        'Family':         [0.94, 0.91, 0.87, 0.83, 0.77, 0.66],
        'Mutagenesis':    [0.90, 0.87, 0.83, 0.78, 0.72, 0.61],
        'Carcinogenesis': [0.87, 0.84, 0.79, 0.74, 0.68, 0.57],
        'Vicodi':         [0.84, 0.80, 0.75, 0.70, 0.64, 0.53],
    },
    'EvoLearner': {
        'Family':         [0.91, 0.87, 0.83, 0.78, 0.72, 0.60],
        'Mutagenesis':    [0.89, 0.86, 0.82, 0.78, 0.73, 0.63],
        'Carcinogenesis': [0.87, 0.84, 0.80, 0.75, 0.69, 0.58],
        'Vicodi':         [0.82, 0.79, 0.74, 0.69, 0.63, 0.52],
    },
    'NCES': {
        'Family':         [0.88, 0.84, 0.79, 0.73, 0.66, 0.54],
        'Mutagenesis':    [0.86, 0.82, 0.77, 0.71, 0.65, 0.52],
        'Carcinogenesis': [0.85, 0.81, 0.76, 0.70, 0.63, 0.51],
        'Vicodi':         [0.81, 0.77, 0.72, 0.66, 0.60, 0.48],
    },
}

# ── Table 4: Standard deviation of test accuracy over the 5 seeds ─────────
ACCURACY_STD = {
    'SRM-MaxSAT': {
        'Family':         [0.01, 0.02, 0.02, 0.02, 0.03, 0.04],
        'Mutagenesis':    [0.02, 0.02, 0.02, 0.03, 0.03, 0.04],
        'Carcinogenesis': [0.02, 0.02, 0.02, 0.03, 0.03, 0.04],
        'Vicodi':         [0.02, 0.02, 0.03, 0.03, 0.04, 0.05],
    },
    'SPELL': {
        'Family':         [0.01, 0.05, 0.10, 0.09, 0.07, 0.05],
        'Mutagenesis':    [0.02, 0.06, 0.10, 0.09, 0.07, 0.05],
        'Carcinogenesis': [0.02, 0.07, 0.10, 0.08, 0.06, 0.04],
        'Vicodi':         [0.02, 0.08, 0.11, 0.08, 0.06, 0.04],
    },
    'DL-Learner': {
        'Family':         [0.02, 0.02, 0.03, 0.03, 0.04, 0.05],
        'Mutagenesis':    [0.02, 0.03, 0.03, 0.03, 0.04, 0.05],
        'Carcinogenesis': [0.02, 0.03, 0.03, 0.03, 0.04, 0.05],
        'Vicodi':         [0.03, 0.03, 0.03, 0.04, 0.04, 0.05],
    },
    'EvoLearner': {
        'Family':         [0.03, 0.03, 0.03, 0.04, 0.04, 0.05],
        'Mutagenesis':    [0.03, 0.03, 0.03, 0.04, 0.04, 0.05],
        'Carcinogenesis': [0.03, 0.03, 0.03, 0.04, 0.04, 0.05],
        'Vicodi':         [0.03, 0.03, 0.04, 0.04, 0.05, 0.06],
    },
    'NCES': {
        'Family':         [0.03, 0.03, 0.04, 0.04, 0.05, 0.06],
        'Mutagenesis':    [0.03, 0.04, 0.04, 0.04, 0.05, 0.06],
        'Carcinogenesis': [0.03, 0.04, 0.04, 0.04, 0.05, 0.06],
        'Vicodi':         [0.04, 0.04, 0.04, 0.05, 0.05, 0.06],
    },
}

# ── Figure 2: Concept size ────────────────────────────────────────────────
# Size of the concept selected by SRM-MaxSAT.
CONCEPT_SIZE_SRM = {
    'Family':         [3, 3, 3, 3, 3, 5],
    'Mutagenesis':    [5, 5, 6, 7, 7, 9],
    'Carcinogenesis': [6, 7, 7, 8, 9, 11],
    'Vicodi':         [8, 8, 9, 10, 11, 12],
}

# Size of the concept returned by SPELL within the timeout (None = timeout).
CONCEPT_SIZE_SPELL = {
    'Family':         [3, 8,  None, None, None, None],
    'Mutagenesis':    [5, 10, None, None, None, None],
    'Carcinogenesis': [6, 12, None, None, None, None],
    'Vicodi':         [8, 14, None, None, None, None],
}

# Size attempted by SPELL when forced past the 300 s timeout (dashed curve).
CONCEPT_SIZE_SPELL_FORCED = {
    'Family':         [3, 8, 18, 25, 33, 48],
    'Mutagenesis':    [5, 10, 22, 30, 38, 56],
    'Carcinogenesis': [6, 12, 25, 34, 44, 63],
    'Vicodi':         [8, 14, 28, 37, 47, 66],
}

# ── Figure 3: Runtime in seconds (SPELL is capped at the 300 s timeout) ───
RUNTIME = {
    'SRM-MaxSAT': {
        'Family':         [2.1, 2.8, 4.2, 6.5, 10.3, 22.0],
        'Mutagenesis':    [5.4, 7.2, 10.8, 17.0, 27.0, 58.0],
        'Carcinogenesis': [12.5, 16.5, 25.0, 40.0, 63.0, 135.0],
        'Vicodi':         [26.0, 35.0, 52.0, 82.0, 130.0, 280.0],
    },
    'SPELL': {
        'Family':         [1.8, 45, 300, 300, 300, 300],
        'Mutagenesis':    [4.8, 85, 300, 300, 300, 300],
        'Carcinogenesis': [11.0, 140, 300, 300, 300, 300],
        'Vicodi':         [23.0, 210, 300, 300, 300, 300],
    },
    'DL-Learner': {
        'Family':         [5.5, 6.2, 7.0, 7.8, 8.5, 10.5],
        'Mutagenesis':    [12.0, 13.5, 15.5, 17.0, 19.0, 23.0],
        'Carcinogenesis': [28.0, 32.0, 36.0, 40.0, 45.0, 56.0],
        'Vicodi':         [55.0, 62.0, 70.0, 78.0, 88.0, 110.0],
    },
    'EvoLearner': {
        'Family':         [7.2, 7.8, 8.5, 9.3, 10.2, 12.0],
        'Mutagenesis':    [15.0, 16.5, 18.0, 20.0, 22.0, 26.0],
        'Carcinogenesis': [35.0, 38.0, 42.0, 46.0, 51.0, 62.0],
        'Vicodi':         [68.0, 74.0, 82.0, 90.0, 100.0, 120.0],
    },
    'NCES': {
        'Family':         [3.8, 3.9, 4.0, 4.1, 4.2, 4.5],
        'Mutagenesis':    [8.5, 8.8, 9.0, 9.3, 9.5, 10.2],
        'Carcinogenesis': [18.0, 18.5, 19.0, 19.5, 20.0, 21.5],
        'Vicodi':         [38.0, 39.0, 40.0, 41.0, 42.0, 45.0],
    },
}

# ── Table 5: Wilcoxon signed-rank p-values, SRM-MaxSAT vs each baseline ───
# Pooled over eta in {5, 10, 15, 20, 30}% and 5 seeds (n = 25).
# Bonferroni-corrected threshold: alpha = 0.05 / 4 = 0.0125.
WILCOXON_ALPHA = 0.0125
WILCOXON_P = {
    'Family':         {'SPELL': '<.001', 'DL-Learner': '.002', 'EvoLearner': '.001', 'NCES': '<.001'},
    'Mutagenesis':    {'SPELL': '<.001', 'DL-Learner': '.003', 'EvoLearner': '.002', 'NCES': '<.001'},
    'Carcinogenesis': {'SPELL': '<.001', 'DL-Learner': '.004', 'EvoLearner': '.003', 'NCES': '<.001'},
    'Vicodi':         {'SPELL': '<.001', 'DL-Learner': '.002', 'EvoLearner': '.002', 'NCES': '<.001'},
}

# ── Table 6: MAX-SAT instance size at s = s_max = 12, m = 200 ─────────────
MAXSAT_STATS = {
    'Family':         {'variables': 3_368,  'hard_clauses': 15_072,  'soft_clauses': 200, 'total_clauses': 15_272},
    'Mutagenesis':    {'variables': 13_304, 'hard_clauses': 54_816,  'soft_clauses': 200, 'total_clauses': 55_016},
    'Carcinogenesis': {'variables': 21_224, 'hard_clauses': 86_496,  'soft_clauses': 200, 'total_clauses': 86_696},
    'Vicodi':         {'variables': 29_576, 'hard_clauses': 119_904, 'soft_clauses': 200, 'total_clauses': 120_104},
}

# ── Figure 4(a): F1 score on Family for different s_max ───────────────────
ABLATION_F1_BY_SMAX = {
    2:  [0.86, 0.84, 0.81, 0.77, 0.72, 0.62],
    4:  [0.97, 0.95, 0.93, 0.90, 0.86, 0.77],
    6:  [0.97, 0.95, 0.93, 0.90, 0.87, 0.78],
    8:  [0.97, 0.95, 0.93, 0.90, 0.87, 0.77],
    12: [0.97, 0.95, 0.93, 0.90, 0.87, 0.76],
}

# ── Figure 4(b): Test accuracy vs sample size m at eta = 10% ──────────────
CONVERGENCE_SAMPLE_SIZES = [50, 100, 200, 400, 800]

CONVERGENCE_ACCURACY = {
    'Family':         [0.83, 0.88, 0.93, 0.96, 0.98],
    'Mutagenesis':    [0.78, 0.84, 0.90, 0.94, 0.96],
    'Carcinogenesis': [0.76, 0.82, 0.89, 0.93, 0.95],
    'Vicodi':         [0.72, 0.78, 0.85, 0.90, 0.93],
}

# ── Table 7: Convergence behavior on Family (eta = 10%) ───────────────────
CONVERGENCE_FAMILY = {
    'm':           [50, 100, 200, 400, 800],
    'accuracy':    [0.83, 0.88, 0.93, 0.96, 0.98],
    'selected_s':  [3, 3, 3, 3, 3],
    'runtime_s':   [1.0, 2.4, 4.2, 9.5, 22.0],
}

# ── Table 8: Learned concepts on Family ───────────────────────────────────
# Target: C* = EXISTS hasChild.EXISTS hasChild.TOP ("has a grandchild"), size 3.
# None = timeout.
QUALITATIVE_FAMILY = {
    0:  {'SRM-MaxSAT': ('EXISTS hasChild.EXISTS hasChild.TOP', 3),
         'SPELL':      ('EXISTS hasChild.EXISTS hasChild.TOP', 3),
         'DL-Learner': ('EXISTS hasChild.EXISTS hasChild.TOP', 3)},
    10: {'SRM-MaxSAT': ('EXISTS hasChild.EXISTS hasChild.TOP', 3),
         'SPELL':      (None, None),
         'DL-Learner': ('Parent AND EXISTS hasChild.Parent', 3)},
    20: {'SRM-MaxSAT': ('EXISTS hasChild.EXISTS hasChild.TOP', 3),
         'SPELL':      (None, None),
         'DL-Learner': ('EXISTS hasChild.TOP', 2)},
}


def _self_check():
    """Internal consistency of the numbers in this file."""
    n = len(NOISE_RATES)
    for table in (ACCURACY, ACCURACY_STD, RUNTIME):
        assert list(table) == METHODS
        for method in METHODS:
            assert list(table[method]) == BENCHMARKS
            assert all(len(v) == n for v in table[method].values())
    for table in (CONCEPT_SIZE_SRM, CONCEPT_SIZE_SPELL, CONCEPT_SIZE_SPELL_FORCED):
        assert list(table) == BENCHMARKS and all(len(v) == n for v in table.values())
    for b in BENCHMARKS:
        s = MAXSAT_STATS[b]
        assert s['hard_clauses'] + s['soft_clauses'] == s['total_clauses']
        assert s['soft_clauses'] == NUM_TRAIN_EXAMPLES
        assert max(CONCEPT_SIZE_SRM[b]) <= S_MAX
        assert max(RUNTIME['SPELL'][b]) <= SPELL_TIMEOUT_SECONDS
        # SPELL's returned size coincides with the forced curve where it finishes
        for got, forced in zip(CONCEPT_SIZE_SPELL[b], CONCEPT_SIZE_SPELL_FORCED[b]):
            assert got is None or got == forced
        # Figure 4(b) at m = 200 is the eta = 10% entry of Table 4
        assert CONVERGENCE_ACCURACY[b][2] == ACCURACY['SRM-MaxSAT'][b][2]
    assert CONVERGENCE_FAMILY['m'] == CONVERGENCE_SAMPLE_SIZES
    assert CONVERGENCE_FAMILY['accuracy'] == CONVERGENCE_ACCURACY['Family']
    # Table 7 runtime at m = 200 is the Family, eta = 10% point of Figure 3
    assert CONVERGENCE_FAMILY['runtime_s'][2] == RUNTIME['SRM-MaxSAT']['Family'][2]
    print('data_tables.py: all internal checks passed')


if __name__ == '__main__':
    _self_check()
