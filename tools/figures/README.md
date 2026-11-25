# Animated icon figures

These scripts draw the animated SVG figures in `book/_static/figures/`, with a PNG copy of each for the PDF.

- `fig.py` and `icons.py` hold the drawing helpers and the icon library (original artwork, no third-party assets).
- `bk_redraws.py`, `bk_new_a.py`, `bk_new_b.py`, `bk_new_c.py`, `bk_new_d.py`, and `bk_new_e.py` draw the figures; each writes to `out/`.
- `integrate.py` holds the helpers that insert a figure into a page.

Each element of a figure carries a build step. A one-shot CSS fade, active only when the reader has not asked for
reduced motion, reveals the steps in order; `book/_static/figure-build.js` restarts the build when a figure scrolls
into view and adds a Replay button. Rendering a PNG needs `rsvg-convert`.

Every build step carries a numbered badge, so the numbers run 1 to N with no gaps. When a script does not place a
step's badge itself, `fig.py` adds one at save time beside the step's first box, label, or icon.
