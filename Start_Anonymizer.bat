@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment not found.
  echo Please complete the first-time setup from the README.
  pause
  exit /b 1
)

call ".venv\Scripts\activate.bat"
python -m streamlit run "src\greek_med_anonymizer\web_app.py"
