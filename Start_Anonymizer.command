#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d ".venv" ]; then
  echo "Virtual environment not found."
  echo "Please complete the first-time setup from the README."
  read -r -p "Press Enter to close..."
  exit 1
fi

source ".venv/bin/activate"
python -m streamlit run "src/greek_med_anonymizer/web_app.py"
