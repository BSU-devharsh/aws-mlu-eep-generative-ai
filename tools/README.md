# PDF build tooling

Scripts used to render the book to a single, print-quality PDF for archiving
(e.g., on Zenodo). The website itself is built with Jupyter Book (`jupyter-book
build book`); these scripts are only for the PDF edition.

## Why these exist

A non-JavaScript HTML-to-PDF renderer (WeasyPrint) is used so the PDF builds
without a headless browser. That introduces two issues these scripts fix:

- **Code blocks:** Pygments wraps every token in styled spans, which corrupts the
  PDF text layer (dropped operators, merged words). `build_pdf.py` flattens each
  `<pre>` to clean, copy-pasteable monospace text.
- **Math:** MathJax renders formulas with JavaScript, which WeasyPrint does not
  run. `build_pdf.py` converts `\[...\]` / `\(...\)` LaTeX to Unicode (e.g.
  `\frac`, `\cdot`, `\lVert`) **outside** code blocks, so the cosine-similarity
  formula and similar render correctly.

It also adds `[IN]`/`[OUT]` badges to notebook cells and figure captions.

## Usage (adjust the hard-coded paths near the top first)

```bash
pip install jupyter-book weasyprint pypdf
jupyter-book build book                 # produces book/_build/html
python tools/make_cover.py              # writes the cover PDF
python tools/build_pdf.py 0 48          # renders each section to /tmp/parts
# then merge cover + parts in order (see the merge snippet in build_pdf.py history)
```

The scripts currently use absolute scratch paths (`/tmp/...`); generalize them to
your environment before running. They are committed for reproducibility of the
PDF edition, not as a turnkey CLI.
