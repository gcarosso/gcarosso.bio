#!/bin/sh
# Gate for the CV download (assets/Giovanni-Carosso-CV.pdf). Run before committing a new PDF:
#   sh assets/cv_check.sh assets/Giovanni-Carosso-CV.pdf
# Export route that passes: open the phone-free DOCX in Pages (open -a Pages file.docx), File → Export → PDF.
# Word on this Mac cannot embed Helvetica Neue and silently swaps in Sylfaen (a serif); Chrome print of cv.html is not the source either.
set -u
PDF="${1:-assets/Giovanni-Carosso-CV.pdf}"; fail=0
say() { printf '%s %s\n' "$1" "$2"; }
fonts=$(strings "$PDF" | grep -o '/BaseFont */[A-Za-z+-]*' | sed 's#.*+##; s#.*/##' | sort -u | tr '\n' ' ')
case "$fonts" in *HelveticaNeue*) say ok "body font Helvetica Neue ($fonts)";; *) say FAIL "body font is not Helvetica Neue: $fonts"; fail=1;; esac
case "$fonts" in *Sylfaen*|*Arial*|*Times*|*Nimbus*) say FAIL "substituted font present: $fonts"; fail=1;; esac
info=$(osascript -l JavaScript -e "ObjC.import('Quartz'); var d=\$.PDFDocument.alloc.initWithURL(\$.NSURL.fileURLWithPath('$PDF')); var t=d.string.js; var n=0; for(var i=0;i<d.pageCount;i++){n+=Number(d.pageAtIndex(i).annotations.count);} console.log([d.pageCount,n,/\(\d{3}\)|\d{3}[-.]\d{3}[-.]\d{4}/.test(t),(t.match(/pending/gi)||[]).length,t.indexOf('PATENT APPLICATIONS')>=0,/[A-Z] [A-Z] [A-Z] [A-Z]/.test(t),t.indexOf('PATENTS')>=0].join(' '))" 2>&1)
set -- $info
[ "$1" = 2 ] && say ok "2 pages" || { say FAIL "pages: $1"; fail=1; }
[ "$2" -ge 5 ] && say ok "$2 link annotations" || { say FAIL "links: $2 (expect >= 5)"; fail=1; }
[ "$3" = false ] && say ok "no phone number" || { say FAIL "phone number present"; fail=1; }
[ "$4" = 0 ] && say ok "no 'pending'" || { say FAIL "'pending' appears $4 times"; fail=1; }
[ "$5" = false ] && [ "$7" = true ] && say ok "section is PATENTS" || { say FAIL "patents heading wrong"; fail=1; }
[ "$6" = false ] && say ok "headings not letter-spaced" || { say FAIL "letter-spaced heading (ATS)"; fail=1; }
exit $fail
