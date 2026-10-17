# ConceptBasis paper

Standalone LaTeX source for the ConceptBasis camera-ready paper in the
NeurReps 2026 Proceedings track. The project is intentionally separate from
the experiment repository so it can be imported directly into Overleaf.

The repository includes the official NeurReps `jmlr.cls` and `jmlrutils.sty`
files downloaded on 2026-08-24. The camera-ready manuscript drops the review
watermark and includes author information and the code link, as the template
requires.

## Build

```bash
python3 figures/dictionary-pipeline.py  # regenerates the TikZ source from figures/dictionary-pipeline.json
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd figures/dictionary-pipeline.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The Proceedings limit is 9 pages excluding references and appendices.

The official template asks authors to keep the paper body in one `.tex` file;
`main.tex` follows that requirement. Figure source files are provided only to
regenerate the included vector PDFs.
