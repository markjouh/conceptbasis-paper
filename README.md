# ConceptBasis paper

Standalone LaTeX source for the anonymous ConceptBasis submission to the
NeurReps 2026 Proceedings track. The project is intentionally separate from
the experiment repository so it can be imported directly into Overleaf.

The repository includes the official NeurReps `jmlr.cls` and `jmlrutils.sty`
files downloaded on 2026-08-24. The review manuscript uses the required
Proceedings watermark and omits author information.

## Build

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error figures/dictionary-pipeline.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The Proceedings limit is 9 pages excluding references and appendices. Before
camera ready, restore author information and remove the four watermark commands
identified in the preamble, following `NEURREPS_TEMPLATE_INSTRUCTIONS.txt`.

The official template asks authors to keep the paper body in one `.tex` file;
`main.tex` follows that requirement. Figure source files are provided only to
regenerate the included vector PDFs.
