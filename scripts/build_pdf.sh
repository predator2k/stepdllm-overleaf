#!/usr/bin/env sh
# Reproducible NeurIPS PDF build from repo root (latexmk > pdflatex+bibtex > tectonic).
set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

DOC="neurips_2026.tex"
STEM="neurips_2026"

usage() {
  printf '%s\n' "Usage: $0 [--help] [--print-engine]" \
    "" \
    "Build ${DOC} using the first available backend:" \
    "  1) latexmk -pdf (uses ./latexmkrc when present)" \
    "  2) pdflatex + bibtex + pdflatex x2 (halt-on-error)" \
    "  3) tectonic (no local TeX tree; downloads packages; XeTeX-class engine)" \
    "" \
    "Requires network on first tectonic run. Install MacTeX/BasicTeX for pdflatex parity."
}

print_engine() {
  if command -v latexmk >/dev/null 2>&1; then
    printf '%s\n' latexmk
    return 0
  fi
  if command -v pdflatex >/dev/null 2>&1 && command -v bibtex >/dev/null 2>&1; then
    printf '%s\n' pdflatex
    return 0
  fi
  if command -v tectonic >/dev/null 2>&1; then
    printf '%s\n' tectonic
    return 0
  fi
  return 1
}

case "${1:-}" in
  -h | --help)
    usage
    exit 0
    ;;
  --print-engine)
    if print_engine; then
      exit 0
    fi
    printf '%s\n' "none" >&2
    printf '%s\n' "No latexmk, no pdflatex+bibtex, and no tectonic on PATH." >&2
    exit 1
    ;;
  "")
    ;;
  *)
    printf '%s\n' "Unknown option: $1" >&2
    usage >&2
    exit 2
    ;;
esac

if command -v latexmk >/dev/null 2>&1; then
  exec latexmk -pdf -interaction=nonstopmode -halt-on-error "$DOC"
fi

if command -v pdflatex >/dev/null 2>&1 && command -v bibtex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error "$DOC"
  bibtex "$STEM"
  pdflatex -interaction=nonstopmode -halt-on-error "$DOC"
  pdflatex -interaction=nonstopmode -halt-on-error "$DOC"
  exit 0
fi

if command -v tectonic >/dev/null 2>&1; then
  exec tectonic "$DOC"
fi

printf '%s\n' "No usable TeX toolchain on PATH (latexmk; or pdflatex+bibtex; or tectonic)." >&2
printf '%s\n' "macOS: brew install --cask basictex  # then restart shell or: eval \"\$(/usr/libexec/path_helper)\"" >&2
printf '%s\n' "Or: brew install tectonic && $0   # XeTeX-class engine; first run may download packages" >&2
exit 127
