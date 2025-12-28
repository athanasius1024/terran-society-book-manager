# LaTeX Installation Guide

This guide explains how to install and use LaTeX for direct Markdown to PDF conversion.

## Why LaTeX?

While LibreOffice (via ODT) works well for most users, LaTeX provides:
- **Professional typography** - Better spacing, ligatures, hyphenation
- **Consistent formatting** - More control over document appearance
- **Print-ready output** - Industry-standard PDF generation
- **Better for technical content** - Superior handling of complex layouts

## Installation

### Option 1: Automated Installation (Recommended)

Run the provided setup script:

```bash
cd /media/infodine/LaCie/z_stash/z-terran/TerranSocietyBook/infobuild
sudo bash scripts/setup_latex.sh
```

This script will:
1. Update package lists
2. Install XeLaTeX and required fonts
3. Verify the installation
4. Test PDF generation with your manuscript

### Option 2: Manual Installation

Install the required packages:

```bash
sudo apt-get update
sudo apt-get install -y texlive-xetex texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
```

**Installation size:** Approximately 500MB-1GB  
**Installation time:** 5-15 minutes depending on your internet connection

### Verify Installation

Check that XeLaTeX is installed:

```bash
which xelatex
xelatex --version
```

Expected output:
```
/usr/bin/xelatex
XeTeX 3.141592653-2.6-0.999995 (TeX Live 2023/Debian)
```

## Usage

### Via Web Interface

After installation, use the **Convert to PDF** button on the Dashboard:
1. Click the dropdown arrow
2. Select **"From MD (XeLaTeX)"**
3. Wait for conversion (may take 30-60 seconds)
4. PDF will be saved as `book/TerranSocietyBook.pdf`

### Via Command Line

Direct conversion from Markdown:

```bash
cd /media/infodine/LaCie/z_stash/z-terran/TerranSocietyBook/infobuild

pandoc book/manuscript.md -o book/TerranSocietyBook.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=book
```

### Advanced Options

**Custom margins:**
```bash
-V geometry:margin=1.5in
-V geometry:top=1in,bottom=1in,left=1.25in,right=1.25in
```

**Font size options:**
```bash
-V fontsize=10pt   # Smaller (more text per page)
-V fontsize=11pt   # Default
-V fontsize=12pt   # Larger (easier to read)
```

**Document class:**
```bash
-V documentclass=book      # Two-sided layout with chapters
-V documentclass=report    # One-sided with chapters
-V documentclass=article   # Simple layout without chapters
```

**Custom fonts (if installed):**
```bash
-V mainfont="Times New Roman"
-V sansfont="Arial"
-V monofont="Courier New"
```

**Line spacing:**
```bash
-V linestretch=1.5   # 1.5 line spacing
-V linestretch=2.0   # Double spacing
```

## Comparison: LibreOffice vs LaTeX

| Feature | LibreOffice (ODT→PDF) | LaTeX (MD→PDF) |
|---------|----------------------|----------------|
| **Installation** | Already installed | Requires ~500MB-1GB |
| **Speed** | Fast (2-5 seconds) | Slower (30-60 seconds) |
| **Typography** | Good | Excellent |
| **Manual editing** | Easy in Writer | Requires LaTeX knowledge |
| **Consistency** | Good | Excellent |
| **Headers/Footers** | Full support | Limited (needs template) |
| **Best for** | Quick previews, editing | Final publication, print |

## Recommendation

- **For drafts and quick reviews:** Use LibreOffice (ODT → PDF)
- **For final publication:** Use LaTeX (MD → PDF)
- **For distribution to editors:** Use ODT format (editable in LibreOffice/Word)

## Troubleshooting

### "xelatex: command not found"

LaTeX is not installed or not in your PATH. Run:
```bash
sudo apt-get install texlive-xetex
```

### "! LaTeX Error: File 'book.cls' not found"

Missing LaTeX packages. Install the full suite:
```bash
sudo apt-get install texlive-latex-extra
```

### Conversion takes too long / hangs

First conversion compiles fonts and caches packages (60+ seconds). Subsequent conversions should be faster (20-30 seconds).

If it hangs, check for LaTeX errors:
```bash
pandoc book/manuscript.md -o book/test.pdf --pdf-engine=xelatex 2>&1 | tail -50
```

### Unicode characters not rendering

XeLaTeX should handle Unicode. If issues persist, try:
```bash
-V CJKmainfont="Noto Sans CJK"  # For Chinese/Japanese/Korean
```

### "Undefined control sequence" errors

Usually indicates special characters in the Markdown that LaTeX interprets as commands. Check the error output for the problematic line.

## Testing Your Installation

After installation, test with a simple document:

```bash
cd /media/infodine/LaCie/z_stash/z-terran/TerranSocietyBook/infobuild

# Create test document
echo "# Test Document

This is a test.

## Section 1
Some content here.
" > book/test.md

# Convert to PDF
pandoc book/test.md -o book/test.pdf --pdf-engine=xelatex

# Check result
ls -lh book/test.pdf
```

If `test.pdf` is created, your installation works correctly!

## Uninstalling

If you need to remove LaTeX to free up space:

```bash
sudo apt-get remove texlive-xetex texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
sudo apt-get autoremove
```

This will free up ~1GB of space. You can still use the LibreOffice conversion method.
