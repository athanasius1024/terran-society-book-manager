# PDF Generation with LaTeX

## Overview

The book is now generated directly to PDF using **Pandoc + XeLaTeX**, which provides professional book publishing quality with:

- ✓ Properly centered cover and author pages
- ✓ Automatic table of contents
- ✓ Headers and footers (only after front matter)
- ✓ Professional typography
- ✓ Proper page breaks and chapters
- ✓ Clickable table of contents (hyperlinks)

## Why LaTeX?

LaTeX is the industry standard for academic and professional book publishing. It handles all the formatting that was impossible with ODT:

- **Front matter vs main matter**: LaTeX has built-in concepts for this
- **Vertical centering**: Native support
- **Conditional headers/footers**: Easy with `\frontmatter` and `\mainmatter`
- **Professional typography**: Decades of refinement

## Requirements

Install XeLaTeX and required packages:

```bash
sudo apt-get update
sudo apt-get install pandoc texlive-xelatex texlive-fonts-recommended texlive-latex-extra
```

## Usage

### Via Web Interface

1. Click **"Regenerate Book (Markdown)"** to generate `book/manuscript.md`
2. Click **"Generate PDF (LaTeX)"** to create `book/TerranSocietyBook.pdf`
3. PDF opens automatically in your browser

### Via Command Line

```bash
# Generate markdown
python3 scripts/generate_book.py

# Generate PDF
python3 scripts/generate_pdf.py

# View PDF
xdg-open book/TerranSocietyBook.pdf
```

## What Happened to ODT?

ODT (Open Document Format) was removed because:

1. **Pandoc limitations**: Markdown→ODT conversion doesn't support:
   - Vertical centering
   - Conditional headers/footers based on page type
   - Proper front matter handling

2. **Manual formatting required**: Every ODT export required manual fixes in LibreOffice

3. **Not for publishing**: ODT is a word processor format, not a book publishing format

## Alternative Publishing Formats

If you need formats other than PDF:

### EPUB (eBooks)
```bash
pandoc book/manuscript.md -o book/TerranSocietyBook.epub --toc --toc-depth=3
```

### HTML (Web)
```bash
pandoc book/manuscript.md -o book/TerranSocietyBook.html --toc --toc-depth=3 --standalone --css=style.css
```

### DOCX (Microsoft Word)
```bash
pandoc book/manuscript.md -o book/TerranSocietyBook.docx --toc --toc-depth=3
```
Note: DOCX has same limitations as ODT - manual formatting required

## Customizing the PDF

The PDF generation uses Pandoc with these settings:

- **Document class**: `book` (professional book layout)
- **Paper size**: Letter (8.5" × 11")
- **Margins**: Left 1.5", Others 1"
- **Font size**: 11pt
- **Line spacing**: 1.25
- **PDF engine**: XeLaTeX (Unicode support)

To customize, edit `scripts/generate_pdf.py` and modify the pandoc command parameters.

## Advanced: Custom LaTeX Template

For complete control, create a custom LaTeX template:

1. Copy `templates/book_template.tex` to a new file
2. Modify formatting, fonts, page layout, etc.
3. Update `scripts/generate_pdf.py` to use your template:
   ```python
   cmd.extend(['--template', 'path/to/your/template.tex'])
   ```

## Troubleshooting

### "pandoc: xelatex not found"
Install texlive-xelatex:
```bash
sudo apt-get install texlive-xelatex
```

### "Package X not found"
Install additional LaTeX packages:
```bash
sudo apt-get install texlive-latex-extra texlive-fonts-extra
```

### PDF looks wrong
Check the Pandoc/LaTeX output in the terminal for warnings. Common issues:
- Missing fonts: Install with `sudo apt-get install fonts-liberation`
- Unicode errors: XeLaTeX should handle these automatically
- Layout issues: Modify geometry settings in `generate_pdf.py`

## Publishing Services

For professional printing, these services accept PDF:

- **Amazon KDP** (Kindle Direct Publishing)
- **IngramSpark**
- **Lulu**
- **Barnes & Noble Press**
- **Apple Books** (also accepts EPUB)

PDF from LaTeX is print-ready for all of these services.
