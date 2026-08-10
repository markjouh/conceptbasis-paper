# ConceptBasis paper

Standalone LaTeX source for the ConceptBasis paper. The project is intentionally
separate from the experiment repository so it can be imported directly into
Overleaf.

## Build

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

`main.tex` currently uses a neutral article wrapper. When a venue is selected,
replace the preamble with the venue's official class and bibliography style;
the paper body, `references.bib`, and vector figures can remain unchanged.

The current author line is non-anonymous; anonymize it if the venue requires blind review.
