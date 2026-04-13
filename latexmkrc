# Used when `latexmk` is on PATH (e.g. MacTeX / BasicTeX). See scripts/build_pdf.sh.
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error %O %S';
$bibtex_use = 2;
@default_files = ('neurips_2026.tex');
