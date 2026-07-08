#!/bin/bash

set -e

cd "$(dirname "$0")"

echo
echo "Greek Medical Report Anonymizer"
echo

PY_CMD=""
ENV_LABEL=""

if [ -n "${CONDA_PREFIX:-}" ] && [ -x "${CONDA_PREFIX}/bin/python" ]; then
  PY_CMD="${CONDA_PREFIX}/bin/python"
  ENV_LABEL="active conda environment"
fi

if [ -z "$PY_CMD" ] && [ -x ".venv/bin/python" ]; then
  PY_CMD=".venv/bin/python"
  ENV_LABEL="local .venv"
fi

if [ -z "$PY_CMD" ]; then
  if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 was not found."
    echo "Please install Python 3.10 or newer, then run this file again."
    read -r -p "Press Enter to close..."
    exit 1
  fi

  echo "Creating local virtual environment..."
  python3 -m venv .venv
  PY_CMD=".venv/bin/python"
  ENV_LABEL="local .venv"
fi

if ! "$PY_CMD" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
  echo "Python 3.10 or newer is required."
  read -r -p "Press Enter to close..."
  exit 1
fi

echo "Using ${ENV_LABEL}."

if ! "$PY_CMD" -c "import streamlit" >/dev/null 2>&1; then
  echo "Installing required packages..."
  "$PY_CMD" -m pip install --upgrade pip
  "$PY_CMD" -m pip install -e ".[ml,ui]"
fi

echo "Launching web app..."
echo "If the browser does not open automatically, go to http://localhost:8501"
echo

"$PY_CMD" -m streamlit run src/greek_med_anonymizer/web_app.py
