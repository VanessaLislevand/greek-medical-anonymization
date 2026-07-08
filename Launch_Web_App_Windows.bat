@echo off
setlocal

cd /d "%~dp0"

echo.
echo Greek Medical Report Anonymizer
echo.

set "PY_CMD="
set "ENV_LABEL="

if defined CONDA_PREFIX if exist "%CONDA_PREFIX%\python.exe" (
  set "PY_CMD=%CONDA_PREFIX%\python.exe"
  set "ENV_LABEL=active conda environment"
)

if not defined PY_CMD (
  if exist ".venv\Scripts\python.exe" (
    set "PY_CMD=.venv\Scripts\python.exe"
    set "ENV_LABEL=local .venv"
  )
)

if not defined PY_CMD (
  echo Creating local virtual environment...
  where py >nul 2>nul
  if not errorlevel 1 (
    py -m venv .venv
  ) else (
    where python >nul 2>nul
    if errorlevel 1 (
      echo Python was not found.
      echo Please install Python 3.10 or newer, then run this file again.
      pause
      exit /b 1
    )
    python -m venv .venv
  )
  if errorlevel 1 (
    echo Failed to create the virtual environment.
    pause
    exit /b 1
  )
  set "PY_CMD=.venv\Scripts\python.exe"
  set "ENV_LABEL=local .venv"
)

%PY_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
  echo Python 3.10 or newer is required.
  pause
  exit /b 1
)

echo Using %ENV_LABEL%.

%PY_CMD% -c "import streamlit" >nul 2>nul
if errorlevel 1 (
  echo Installing required packages...
  %PY_CMD% -m pip install --upgrade pip
  %PY_CMD% -m pip install -e ".[ml,ui]"
  if errorlevel 1 (
    echo Installation failed.
    pause
    exit /b 1
  )
)

echo Launching web app...
echo If the browser does not open automatically, go to http://localhost:8501
echo.

%PY_CMD% -m streamlit run src\greek_med_anonymizer\web_app.py

endlocal
