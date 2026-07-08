@echo off
setlocal

cd /d "%~dp0"

echo.
echo Greek Medical Report Anonymizer
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo Python was not found.
  echo Please install Python 3.10 or newer, then run this file again.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  py -m venv .venv
  if errorlevel 1 (
    echo Failed to create the virtual environment.
    pause
    exit /b 1
  )
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
  echo Failed to activate the virtual environment.
  pause
  exit /b 1
)

python -c "import streamlit" >nul 2>nul
if errorlevel 1 (
  echo Installing required packages...
  python -m pip install --upgrade pip
  python -m pip install -e ".[ml,ui]"
  if errorlevel 1 (
    echo Installation failed.
    pause
    exit /b 1
  )
)

echo Launching web app...
echo If the browser does not open automatically, go to http://localhost:8501
echo.

python -m streamlit run src\greek_med_anonymizer\web_app.py

endlocal
