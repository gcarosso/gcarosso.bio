#!/bin/sh
# Render cv.html to assets/Giovanni-Carosso-CV.pdf with Chrome's print media (the @media print block in style.css).
# Run after editing cv.html: sh assets/make_cv_pdf.sh
cd "$(dirname "$0")/.." || exit 1
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=4000 \
  --print-to-pdf="$PWD/assets/Giovanni-Carosso-CV.pdf" "file://$PWD/cv.html" 2>/dev/null && ls -la assets/Giovanni-Carosso-CV.pdf
