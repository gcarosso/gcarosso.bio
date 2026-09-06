#!/bin/bash
# Double-click this file in Finder to preview the site locally.
# It serves the folder at http://localhost:8000 and opens your browser.
# Close the Terminal window (or press Ctrl-C) to stop.
cd "$(dirname "$0")"
PORT=8000
while lsof -i :$PORT >/dev/null 2>&1; do PORT=$((PORT+1)); done
echo ""
echo "  Serving  $(pwd)"
echo "  Open     http://localhost:$PORT"
echo "  Stop     Ctrl-C, or just close this window"
echo ""
( sleep 1; open "http://localhost:$PORT" ) &
python3 -m http.server $PORT
