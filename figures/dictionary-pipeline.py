#!/usr/bin/env python3
"""Generate dictionary-pipeline.tex (TikZ) from dictionary-pipeline.json.

Every value in the JSON is a real pipeline output; its "source" field says
which. The figure is drawn at the paper's exact text width (6 in), so it is
included at scale 1 and its fonts keep their nominal sizes.

Layout: three panels on one grid. Each panel has a title, a one-line
subtitle, and a content block sharing the same top and bottom edges.

    python3 dictionary-pipeline.py
    latexmk -pdf dictionary-pipeline.tex
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "dictionary-pipeline.json").read_text())

W, H = 152.4, 44.6  # mm
# Color encodes data only: blue intensity is phrase-class similarity in (2),
# and a filled cell is a yes label in (3). Everything else is neutral.

# Columns (mm): panel left edges and widths, with hairline dividers between.
P1, P1W = 0.0, 46.5
P2, P2W = 49.4, 55.0
P3, P3W = 107.0, 45.4
DIVIDERS = (47.5, 105.5)
TITLE_Y, SUB_Y = -3.0, -6.6       # baselines
TOP, BOTTOM = -8.9, -44.0         # shared content block

lines: list[str] = []
emit = lines.append


def n(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


emit(r"""\RequirePackage{fix-cm}
\documentclass[tikz,border=0pt]{standalone}
\usepackage{tcolorbox}
\usetikzlibrary{arrows.meta}
\definecolor{conceptred}{HTML}{C83E3A}
\definecolor{axisgray}{HTML}{3F4650}
\definecolor{pointgray}{HTML}{B8BEC7}
\definecolor{roundblue}{HTML}{3973A8}
\colorlet{heatbase}{pointgray!14}
\colorlet{nolabel}{pointgray!30}
\newtcbox{\tagchip}[1][]{on line, size=fbox, boxrule=.35pt, arc=1.1pt,
  boxsep=0pt, left=.62mm, right=.62mm, top=.42mm, bottom=.42mm,
  colback=pointgray!16, colframe=pointgray, coltext=axisgray,
  fontupper=\fontsize{6}{7.2}\selectfont, #1}
\tikzset{
  title/.style={font=\fontsize{8}{9.6}\selectfont\bfseries, text=axisgray,
                anchor=base west, inner sep=0pt},
  subtitle/.style={font=\fontsize{6}{7.2}\selectfont, text=axisgray!72,
                   anchor=base west, inner sep=0pt},
  plain/.style={font=\fontsize{6}{7.2}\selectfont, text=axisgray, inner sep=0pt},
  concept/.style={font=\fontsize{6.5}{7.8}\selectfont\bfseries, inner sep=0pt},
  photo/.style={inner sep=0pt, anchor=north west},
  frame/.style={draw=axisgray!45, line width=.35pt},
  divider/.style={draw=pointgray!75, line width=.3pt},
}
\begin{document}
\begin{tikzpicture}[x=1mm, y=1mm]""")
emit(rf"\useasboundingbox (0,0) rectangle ({n(W)},{n(-H)});")
for x in DIVIDERS:
    emit(rf"\draw[divider] ({n(x)},-0.6) -- ({n(x)},{n(BOTTOM)});")
counts = DATA["counts"]
examples = DATA["examples"]

# ------------------------------------------------------------------ (1) tags
emit(rf"\node[title] at ({n(P1)},{n(TITLE_Y)}) {{(1) Collect open tags}};")
emit(rf"\node[subtitle] at ({n(P1)},{n(SUB_Y)}) "
     rf"{{{counts['train_images']:,} training images $\to$ {counts['raw_phrases']:,} phrases}};")
photo = 10.0
row_gap = (TOP - BOTTOM - 3 * photo) / 2
chip_x = P1 + photo + 1.4
for i, example in enumerate(examples):
    top = TOP - i * (photo + row_gap)
    emit(rf"\node[photo] at ({n(P1)},{n(top)}) "
         rf"{{\includegraphics[width={n(photo)}mm,height={n(photo)}mm]{{{example['image']}}}}};")
    emit(rf"\draw[frame] ({n(P1)},{n(top)}) rectangle ++({n(photo)},{n(-photo)});")
    chips = [rf"\tagchip{{{t['text']}}}" for t in example["tags"]]
    body = r"\hspace{.6mm}\allowbreak".join(chips)
    emit(rf"\node[anchor=west, inner sep=0pt, text width={n(P1 + P1W - chip_x)}mm, align=left, "
         rf"font=\fontsize{{6}}{{11}}\selectfont] at ({n(chip_x)},{n(top - photo / 2)}) {{{body}}};")

# ------------------------------------------------------------------ (2) merge
emit(rf"\node[title] at ({n(P2)},{n(TITLE_Y)}) {{(2) Merge synonyms by usage}};")
emit(rf"\node[subtitle] at ({n(P2)},{n(SUB_Y)}) "
     rf"{{{counts['candidates']} phrases $\to$ {counts['clusters']} clusters $\to$ {counts['K']} concepts}};")
cell_w, col_pitch, col_gap = 2.2, 2.45, 0.85
cell_h, row_pitch, row_gap2 = 1.95, 2.25, 0.95
groups = DATA["profile_rows"]
n_rows = sum(len(g) for g in groups)
heat_h = n_rows * row_pitch - (row_pitch - cell_h) + (len(groups) - 1) * row_gap2
heat_top = BOTTOM + heat_h
heat_x = P2 + 9.8
col_x = []
x = heat_x
for group in DATA["profile_classes"]:
    for _ in group:
        col_x.append(x)
        x += col_pitch
    x += col_gap
heat_right = col_x[-1] + cell_w
# column header: an axis title over a rule, then class names on a common baseline
emit(rf"\node[plain, text=axisgray!72, anchor=base] at ({n((heat_x + heat_right) / 2)},{n(TOP - 1.5)}) {{training classes}};")
emit(rf"\draw[pointgray, line width=.3pt] ({n(heat_x)},{n(TOP - 2.4)}) -- ({n(heat_right)},{n(TOP - 2.4)});")
for cx, name in zip(col_x, [c for g in DATA["profile_classes"] for c in g]):
    emit(rf"\node[plain, rotate=90, anchor=west] at ({n(cx + cell_w / 2)},{n(heat_top + 0.8)}) {{{name}}};")
y = heat_top
bracket_x = heat_right + 1.1
for group in groups:
    group_top = y
    concept = group[0]["concept"]
    for row in group:
        emit(rf"\node[plain, anchor=east] at ({n(heat_x - 1.1)},{n(y - cell_h / 2)}) {{{row['phrase']}}};")
        values = [v for block in row["values"] for v in block]
        for cx, value in zip(col_x, values):
            share = round(100 * min(max(value, 0.0), 3.0) / 3.0)
            emit(rf"\fill[roundblue!{share}!heatbase] ({n(cx)},{n(y)}) rectangle ++({n(cell_w)},{n(-cell_h)});")
        y -= row_pitch
    group_bottom = y + row_pitch - cell_h
    mid = (group_top + group_bottom) / 2
    emit(rf"\draw[axisgray!80, line width=.45pt] ({n(bracket_x)},{n(group_top)}) -- ++(.75,0) "
         rf"-- ({n(bracket_x + .75)},{n(group_bottom)}) -- ++(-.75,0);")
    emit(rf"\node[concept, anchor=west, text=axisgray] at ({n(bracket_x + 1.6)},{n(mid)}) {{{concept}}};")
    y -= row_gap2

# ------------------------------------------------------------------ (3) labels
emit(rf"\node[title] at ({n(P3)},{n(TITLE_Y)}) {{(3) Label every concept}};")
x = P3
for fill, text in (("axisgray", "yes"), ("nolabel", "no")):
    emit(rf"\fill[{fill}] ({n(x)},{n(SUB_Y - 0.15)}) rectangle ++(1.9,1.9);")
    emit(rf"\node[subtitle] at ({n(x + 2.6)},{n(SUB_Y)}) {{{text}}};")
    x += 2.6 + 1.13 * len(text) + 2.4
emit(rf"\node[subtitle] at ({n(x)},{n(SUB_Y)}) {{for all {counts['K']} concepts}};")
thumb, col_gap3 = 10.0, 1.0  # same photo size as panel 1
label_right = P3 + 11.8
col_left = [label_right + 1.2 + i * (thumb + col_gap3) for i in range(len(examples))]
for cx, example in zip(col_left, examples):
    emit(rf"\node[photo] at ({n(cx)},{n(TOP)}) "
         rf"{{\includegraphics[width={n(thumb)}mm,height={n(thumb)}mm]{{{example['image']}}}}};")
    emit(rf"\draw[frame] ({n(cx)},{n(TOP)}) rectangle ++({n(thumb)},{n(-thumb)});")
tile_h, tile_pitch, tile_gap = 2.3, 3.35, 1.0
y = TOP - thumb - 1.5
for group in DATA["label_columns"]:
    for concept in group:
        emit(rf"\node[concept, anchor=east, text=axisgray] at ({n(label_right)},{n(y - tile_h / 2)}) {{{concept}}};")
        for cx, example in zip(col_left, examples):
            fill = "axisgray" if concept in example["labels"] else "nolabel"
            emit(rf"\fill[{fill}, rounded corners=.35mm] ({n(cx + 0.5)},{n(y)}) rectangle ++({n(thumb - 1.0)},{n(-tile_h)});")
        y -= tile_pitch
    y -= tile_gap

emit(r"\end{tikzpicture}")
emit(r"\end{document}")
(HERE / "dictionary-pipeline.tex").write_text("\n".join(lines) + "\n")
print(f"wrote dictionary-pipeline.tex ({len(lines)} lines)")
