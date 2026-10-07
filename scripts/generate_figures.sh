#!/bin/bash
# Generate all figures of the paper (Figures 1-4).
# Output: figures/*.pdf, copied to paper/ for LaTeX compilation.
# Optional arguments select a subset: accuracy, concept_size, runtime, ablation.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
OUT_DIR="$ROOT_DIR/figures"

echo "=== Generating figures ==="
cd "$OUT_DIR"
python3 src/generate_all_figures.py "$@"

# Copy to paper/ for LaTeX compilation
cp "$OUT_DIR"/fig_*.pdf "$ROOT_DIR/paper/"

echo "=== Done. Figures saved to $OUT_DIR/ and copied to $ROOT_DIR/paper/ ==="
