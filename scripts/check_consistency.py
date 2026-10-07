#!/usr/bin/env python3
"""
Check that everything in this repository agrees with the paper.

The LaTeX source (paper/uai2026-main-id228.tex) is the reference. This script
compares against it, value by value:

  * experiments/data_tables.py            (all tabulated numbers)
  * figures/src/generate_all_figures.py   (the arrays plotted in Figures 1-4)
  * README.md                             (the two numeric tables)

and then re-derives the quantitative statements made in the paper's text from
the data (for example "accuracy of 0.85 or above at 10% noise").

Usage:  python3 scripts/check_consistency.py
Needs only the Python standard library. Exit status is 0 if all checks pass.
"""

import ast
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / 'paper' / 'uai2026-main-id228.tex'
BIB = ROOT / 'paper' / 'uai2026.bib'
FIG_SCRIPT = ROOT / 'figures' / 'src' / 'generate_all_figures.py'
DATA = ROOT / 'experiments' / 'data_tables.py'
README = ROOT / 'README.md'

FIGURE_FILES = ['fig_accuracy.pdf', 'fig_concept_size.pdf',
                'fig_runtime.pdf', 'fig_ablation_convergence.pdf']

passed, failed = [], []


def check(name, condition, detail=''):
    (passed if condition else failed).append(name)
    print(('  [ok]   ' if condition else '  [FAIL] ') + name
          + ('' if condition or not detail else '\n         ' + str(detail)))


def same(a, b):
    """Equality of numbers / nested lists, tolerant to float representation."""
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) < 1e-9
    return a == b


# ── LaTeX parsing ─────────────────────────────────────────────────────────
tex = TEX.read_text(encoding='utf-8')
tex_nc = re.sub(r'(?<!\\)%.*', '', tex)          # comments removed


def tabular(label):
    i = tex_nc.index('\\label{%s}' % label)
    a = tex_nc.index('\\begin{tabular}', i)
    a = tex_nc.index('\n', a)                    # skip the column specification
    b = tex_nc.index('\\end{tabular}', a)
    return tex_nc[a:b]


def rows(label):
    body = tabular(label)
    body = re.sub(r'\\(toprule|midrule|bottomrule)', '', body)
    return [r.strip() for r in body.split('\\\\') if r.strip()]


def number(cell):
    cell = cell.replace('{,}', '').replace('${\\sim}$', '')
    return float(re.search(r'-?\d*\.?\d+', cell).group(0))


METHODS = ['SRM-MaxSAT', 'SPELL', 'DL-Learner', 'EvoLearner', 'NCES']
BENCHMARKS = ['Family', 'Mutagenesis', 'Carcinogenesis', 'Vicodi']


def accuracy_table(label):
    """Rows of Table 3 / Table 4 in order: 4 benchmarks x 5 methods."""
    pattern = r'&\s*(%s)\s*&(.*?)\\\\' % '|'.join(re.escape(m) for m in METHODS)
    found = re.findall(pattern, tabular(label) + '\\\\', flags=re.S)
    assert len(found) == 20, 'expected 20 method rows in %s, got %d' % (label, len(found))
    table = {}
    for idx, (method, cells) in enumerate(found):
        bench = BENCHMARKS[idx // 5]
        assert method == METHODS[idx % 5]
        table[(method, bench)] = [float('0' + v) for v in re.findall(r'\.\d+', cells)]
    return table


def labelled_rows(label, names):
    out = {}
    for row in rows(label):
        cells = [c.strip() for c in row.split('&')]
        for key, name in names.items():
            if cells[0].replace(' ', '').startswith(name.replace(' ', '')):
                out[key] = [number(c) for c in cells[1:]]
    return out


# ── Load the Python sources ───────────────────────────────────────────────
spec = importlib.util.spec_from_file_location('data_tables', DATA)
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)


class _NumpyStub:
    """Just enough of numpy to evaluate the literal arrays in the figure script."""
    nan = None
    array = staticmethod(list)


def figure_script_literals():
    """All `name = {...}` / `name = np.array([...])` assignments in the script."""
    tree = ast.parse(FIG_SCRIPT.read_text(encoding='utf-8'))
    values = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and isinstance(node.value, (ast.Dict, ast.Call, ast.List)):
            try:
                code = compile(ast.Expression(node.value), str(FIG_SCRIPT), 'eval')
                values[node.targets[0].id] = eval(code, {'np': _NumpyStub, '__builtins__': {}})
            except Exception:
                pass                              # not a data literal
    return values


F = figure_script_literals()

print('1. data_tables.py  vs  LaTeX tables')
t3, t4 = accuracy_table('tab:results'), accuracy_table('tab:full-results')
cols3 = [D.NOISE_RATES.index(e) for e in (0, 10, 20, 30)]
check('Table 3 (accuracy at 0/10/20/30%) = data_tables.ACCURACY',
      all(same(t3[(m, b)], [D.ACCURACY[m][b][i] for i in cols3])
          for m in METHODS for b in BENCHMARKS))
check('Table 4 means = data_tables.ACCURACY',
      all(same(t4[(m, b)][0::2], D.ACCURACY[m][b]) for m in METHODS for b in BENCHMARKS))
check('Table 4 standard deviations = data_tables.ACCURACY_STD',
      all(same(t4[(m, b)][1::2], D.ACCURACY_STD[m][b]) for m in METHODS for b in BENCHMARKS))

t2 = labelled_rows('tab:benchmarks', {'sig_c': '$|\\Sigma_C|$', 'sig_r': '$|\\Sigma_R|$',
                                      'individuals': 'Individuals', 'axioms': 'Axioms'})
check('Table 2 (benchmark statistics) = data_tables.BENCHMARK_STATS',
      all(same(t2[k], [D.BENCHMARK_STATS[b][k] for b in BENCHMARKS]) for k in t2) and len(t2) == 4)

t6 = labelled_rows('tab:maxsat-stats', {'variables': 'Variables', 'hard_clauses': 'Hard clauses',
                                        'soft_clauses': 'Soft clauses', 'total_clauses': 'Total clauses'})
check('Table 6 (MAX-SAT instance size) = data_tables.MAXSAT_STATS',
      all(same(t6[k], [D.MAXSAT_STATS[b][k] for b in BENCHMARKS]) for k in t6) and len(t6) == 4)

t7 = labelled_rows('tab:convergence', {'m': '$m$', 'accuracy': 'Accuracy',
                                       'selected_s': 'Selected', 'runtime_s': 'Runtime'})
check('Table 7 (convergence on Family) = data_tables.CONVERGENCE_FAMILY',
      all(same(t7[k], D.CONVERGENCE_FAMILY[k]) for k in t7) and len(t7) == 4)

t5 = {}
for row in rows('tab:significance'):
    cells = [c.strip() for c in row.split('&')]
    if cells[0] in BENCHMARKS:
        t5[cells[0]] = [re.sub(r'[\$\^\*\s]', '', c) for c in cells[1:]]
check('Table 5 (Wilcoxon p-values) = data_tables.WILCOXON_P',
      all(t5[b] == [D.WILCOXON_P[b][m] for m in METHODS[1:]] for b in BENCHMARKS))

t8 = re.findall(r'&\s*(SRM-MaxSAT|SPELL|DL-Learner)\s*&.*?&\s*(\d+|---)\s*\\\\',
                tabular('tab:qualitative') + '\\\\', flags=re.S)
expected8 = [(m, '---' if D.QUALITATIVE_FAMILY[eta][m][1] is None else str(D.QUALITATIVE_FAMILY[eta][m][1]))
             for eta in (0, 10, 20) for m in ('SRM-MaxSAT', 'SPELL', 'DL-Learner')]
check('Table 8 (learned concept sizes) = data_tables.QUALITATIVE_FAMILY', t8 == expected8, t8)

print('2. generate_all_figures.py  vs  data_tables.py')
check('noise rates and benchmark order', same(F['NOISE_RATES'], D.NOISE_RATES) and F['BENCHMARKS'] == D.BENCHMARKS)
fig1 = {'SRM-MaxSAT': 'srm_acc', 'SPELL': 'spell_acc', 'DL-Learner': 'dllearner_acc',
        'EvoLearner': 'evolearner_acc', 'NCES': 'nces_acc'}
check('Figure 1 arrays = ACCURACY (hence Tables 3 and 4)',
      all(same(F[v][b], D.ACCURACY[m][b]) for m, v in fig1.items() for b in BENCHMARKS))
check('Figure 2 arrays = CONCEPT_SIZE_*',
      all(same(F['srm_size'][b], D.CONCEPT_SIZE_SRM[b])
          and same(F['spell_size_valid'][b], D.CONCEPT_SIZE_SPELL[b])
          and same(F['spell_size_forced'][b], D.CONCEPT_SIZE_SPELL_FORCED[b]) for b in BENCHMARKS))
fig3 = {'SRM-MaxSAT': 'srm_time', 'SPELL': 'spell_time', 'DL-Learner': 'dllearner_time',
        'EvoLearner': 'evolearner_time', 'NCES': 'nces_time'}
check('Figure 3 arrays = RUNTIME',
      all(same(F[v][b], D.RUNTIME[m][b]) for m, v in fig3.items() for b in BENCHMARKS))
check('Figure 4(a) arrays = ABLATION_F1_BY_SMAX',
      all(same(F['srm_f1_by_smax'][k], D.ABLATION_F1_BY_SMAX[k]) for k in D.ABLATION_F1_BY_SMAX)
      and set(F['srm_f1_by_smax']) == set(D.ABLATION_F1_BY_SMAX))
check('Figure 4(b) arrays = CONVERGENCE_ACCURACY',
      same(F['sample_sizes'], D.CONVERGENCE_SAMPLE_SIZES)
      and all(same(F['acc_empirical'][b], D.CONVERGENCE_ACCURACY[b]) for b in BENCHMARKS))

print('3. README.md  vs  data_tables.py')
readme = README.read_text(encoding='utf-8')
fam = re.findall(r'^\|\s*(\d+)%\s*\|(.*)\|\s*$', readme, flags=re.M)
check('README Family accuracy table = ACCURACY',
      len(fam) == 4 and all(
          same([float('0' + v) for v in re.findall(r'\.\d+', cells)],
               [D.ACCURACY[m]['Family'][D.NOISE_RATES.index(int(eta))] for m in METHODS])
          for eta, cells in fam), fam)
bench_rows = re.findall(r'^\|\s*\*\*(\w+)\*\*\s*\|[^|]*\|(.*)\|\s*$', readme, flags=re.M)
bench_ok = len(bench_rows) == 4
for name, cells in bench_rows:
    nums = [int(re.sub(r'[^\d]', '', c)) for c in cells.split('|')]
    s = D.BENCHMARK_STATS[name]
    bench_ok &= nums == [s['sig_c'], s['sig_r'], s['individuals'], s['axioms']]
check('README benchmark table = BENCHMARK_STATS', bench_ok, bench_rows)

print('4. Statements in the paper text, re-derived from the data')
A, eta = D.ACCURACY, D.NOISE_RATES.index
i10, i20, i30 = eta(10), eta(20), eta(30)
check('"accuracy >= 0.85 under 10% noise": min over benchmarks is 0.85',
      same(min(A['SRM-MaxSAT'][b][i10] for b in BENCHMARKS), 0.85) and '0.85' in tex)
check('"exact fitting collapses to 0.45 or below": max over benchmarks is 0.45',
      same(max(A['SPELL'][b][i10] for b in BENCHMARKS), 0.45) and '0.45' in tex)
gaps10 = [round(100 * (A['SRM-MaxSAT'][b][i10] - A[m][b][i10])) for m in ('DL-Learner', 'EvoLearner') for b in BENCHMARKS]
check('"DL-Learner and EvoLearner trail by 6--11 points at 10%"',
      (min(gaps10), max(gaps10)) == (6, 11) and '6--11' in tex, gaps10)
lead30 = [round(100 * (A['SRM-MaxSAT'][b][i30] - max(A[m][b][i30] for m in METHODS[2:]))) for b in BENCHMARKS]
check('"leading the best heuristic baseline by 10--13 points at 30%"',
      (min(lead30), max(lead30)) == (10, 13) and '10--13' in tex, lead30)
check('SRM-MaxSAT has the highest accuracy at every noise rate on every benchmark',
      all(A['SRM-MaxSAT'][b][i] >= max(A[m][b][i] for m in METHODS[1:])
          for b in BENCHMARKS for i in range(len(D.NOISE_RATES))))
check('SRM-MaxSAT and SPELL are tied at 0% noise',
      all(same(A['SRM-MaxSAT'][b][0], A['SPELL'][b][0]) for b in BENCHMARKS))
S = D.CONCEPT_SIZE_SRM
check('selected size: 3 on Family, 8 on Vicodi at 0%; grows by at most 5; never exceeds s_max = 12',
      S['Family'][0] == 3 and S['Vicodi'][0] == 8
      and max(S[b][-1] - S[b][0] for b in BENCHMARKS) == 5
      and max(max(S[b]) for b in BENCHMARKS) == D.S_MAX == 12)
check('SPELL attempted size exceeds 15 at 10% and 20 at 20%',
      all(D.CONCEPT_SIZE_SPELL_FORCED[b][i10] > 15 and D.CONCEPT_SIZE_SPELL_FORCED[b][i20] > 20 for b in BENCHMARKS))
check('SRM-MaxSAT runtime stays under 300 s (maximum: Vicodi at 30%)',
      max(max(D.RUNTIME['SRM-MaxSAT'][b]) for b in BENCHMARKS) == D.RUNTIME['SRM-MaxSAT']['Vicodi'][i30] < 300)
check('MAX-SAT totals = hard + soft, and soft = m = 200',
      all(s['hard_clauses'] + s['soft_clauses'] == s['total_clauses'] and s['soft_clauses'] == 200
          for s in D.MAXSAT_STATS.values()))
B = D.BENCHMARK_STATS
check('Vicodi signature size |Sigma| = 204',
      B['Vicodi']['sig_c'] + B['Vicodi']['sig_r'] == 204 and '|\\Sigma| = 204' in tex)
ratio = B['Vicodi']['individuals'] / B['Family']['individuals']
check('"160x range in knowledge base size" (33,238 / 202 = %.1f)' % ratio, 155 <= ratio < 165)
check('convergence: 0.83 at m = 50 to 0.98 at m = 800, s* = 3 throughout',
      D.CONVERGENCE_FAMILY['accuracy'][0] == 0.83 and D.CONVERGENCE_FAMILY['accuracy'][-1] == 0.98
      and set(D.CONVERGENCE_FAMILY['selected_s']) == {3})
check('Figure 4(b) at m = 200 = Table 4 at 10% noise, for all four benchmarks',
      all(same(D.CONVERGENCE_ACCURACY[b][2], A['SRM-MaxSAT'][b][i10]) for b in BENCHMARKS))
check('Table 7 runtime at m = 200 = Figure 3, Family at 10% noise',
      same(D.CONVERGENCE_FAMILY['runtime_s'][2], D.RUNTIME['SRM-MaxSAT']['Family'][i10]))
check('all Table 5 p-values are below the Bonferroni threshold 0.0125',
      all(float(p.lstrip('<')) < D.WILCOXON_ALPHA for row in D.WILCOXON_P.values() for p in row.values()))
check('protocol constants appear in the text (m = 200, s_max = 12, delta = 0.05, 5 seeds)',
      '$m = 200$' in tex and 's_{\\max} = 12' in tex and '\\delta = 0.05' in tex and '5 random seeds' in tex)

print('5. Files')
check('paper/ and figures/ hold byte-identical figure PDFs',
      all((ROOT / 'paper' / f).read_bytes() == (ROOT / 'figures' / f).read_bytes() for f in FIGURE_FILES))
check('every figure is included by the LaTeX source',
      all('{%s}' % f in tex_nc for f in FIGURE_FILES))
cited = {k.strip() for m in re.finditer(r'\\cite[tp]?\*?\{([^}]+)\}', tex_nc) for k in m.group(1).split(',')}
entries = set(re.findall(r'^@\w+\{([^,\s]+),', BIB.read_text(encoding='utf-8'), flags=re.M))
check('all %d cited keys have an entry in uai2026.bib' % len(cited), cited <= entries, sorted(cited - entries))

print()
print('%d checks passed, %d failed' % (len(passed), len(failed)))
sys.exit(1 if failed else 0)
