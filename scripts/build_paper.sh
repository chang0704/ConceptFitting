#!/bin/bash
# Compile the paper (pdflatex + bibtex cycle) and report errors.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$(dirname "$SCRIPT_DIR")/paper"
TEX_FILE="uai2026-main-id228"

cd "$PAPER_DIR" || exit 1

echo "=== Building paper ==="
pdflatex -interaction=nonstopmode "$TEX_FILE" > /dev/null 2>&1
bibtex "$TEX_FILE" > /dev/null 2>&1
pdflatex -interaction=nonstopmode "$TEX_FILE" > /dev/null 2>&1
pdflatex -interaction=nonstopmode "$TEX_FILE" > /dev/null 2>&1

if [ ! -f "$TEX_FILE.pdf" ]; then
    echo "Build failed: no PDF produced. See $PAPER_DIR/$TEX_FILE.log"
    exit 1
fi

ERRORS=$(grep -c '^! ' "$TEX_FILE.log")
UNDEFINED=$(grep -c 'Reference.*undefined\|Citation.*undefined' "$TEX_FILE.log")
BIB_ISSUES=$(grep -c "^Warning--\|Repeated entry\|error message\|I couldn't open" "$TEX_FILE.blg")
echo "LaTeX errors: $ERRORS, undefined references/citations: $UNDEFINED, BibTeX issues: $BIB_ISSUES"

if [ "$ERRORS" -ne 0 ] || [ "$UNDEFINED" -ne 0 ] || [ "$BIB_ISSUES" -ne 0 ]; then
    echo "Build finished with problems. See $PAPER_DIR/$TEX_FILE.log"
    exit 1
fi
echo "=== Done: $PAPER_DIR/$TEX_FILE.pdf ==="
