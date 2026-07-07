# Greek Medical Report Anonymization

This repository provides two simple ways to anonymize Greek medical reports:

1. a Google Colab notebook
2. a local web app

The easiest option for most users is the local web app.

## Quick Start

If you only want to use the web app:

1. Download this repository to your computer.
2. Open a terminal inside the project folder.
3. Install the required packages.
4. Launch the app.
5. Upload your report files and run anonymization.

Detailed instructions are below for both Windows and Mac.

## Option 1: Local Web App

The web app:

- downloads the model automatically the first time it runs
- accepts `.docx`, `.txt`, or `.zip` files
- supports single or multiple reports
- shows the full anonymized output on screen
- lets you download a `.zip` file with the results

### Before You Start

You need:

- Python 3.10 or newer
- internet access the first time the app runs, so the model can be downloaded

## Windows Instructions

### Step 1: Download the repository

Open this repository in GitHub and download it as a `.zip` file, then extract it.

You should end up with a folder named something like:

`greek-medical-anonymization`

### Step 2: Open PowerShell inside the project folder

Open the extracted project folder, click in the address bar, type `powershell`, and press Enter.

This opens a PowerShell window already inside the correct folder.

### Step 3: Check Python

Run:

```powershell
py --version
```

If this does not work, try:

```powershell
python --version
```

If neither command works, Python needs to be installed first.

### Step 4: Create a virtual environment

Run:

```powershell
py -3.10 -m venv .venv
```

If that does not work, try:

```powershell
py -m venv .venv
```

### Step 5: Activate the virtual environment

Run:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks this command, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

and then run again:

```powershell
.venv\Scripts\Activate.ps1
```

When activation succeeds, you should see `(.venv)` at the beginning of the line.

### Step 6: Install the app

Run:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[ml,ui]"
```

This may take a few minutes.

### Step 7: Launch the web app

Run:

```powershell
greek-med-anonymizer-ui
```

After a few seconds, a local web address should appear, usually:

`http://localhost:8501`

Open that address in your browser if it does not open automatically.

## Mac Instructions

### Step 1: Download the repository

Open this repository in GitHub and download it as a `.zip` file, then extract it.

### Step 2: Open Terminal inside the project folder

Open the project folder, then:

1. right-click inside the folder
2. choose `New Terminal at Folder`

If that option is not available, open Terminal manually and run:

```bash
cd "/path/to/greek-medical-anonymization"
```

### Step 3: Create a virtual environment

Run:

```bash
python3 -m venv .venv
```

### Step 4: Activate the virtual environment

Run:

```bash
source .venv/bin/activate
```

When activation succeeds, you should see `(.venv)` at the beginning of the line.

### Step 5: Install the app

Run:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[ml,ui]"
```

### Step 6: Launch the web app

Run:

```bash
greek-med-anonymizer-ui
```

After a few seconds, a local web address should appear, usually:

`http://localhost:8501`

Open that address in your browser if it does not open automatically.

## How To Use The Web App

After the page opens:

1. Choose the report type.
2. Keep the default mask token or change it.
3. Upload one or more `.docx` or `.txt` files.
4. If you want to upload a whole folder, first compress it as a real `.zip` file and upload the `.zip`.
5. Click `Run anonymization`.
6. Review the anonymized output shown on screen.
7. Click the download button to save the anonymized results.

## Web App Settings

### Report type

Choose:

- `Report with template and free text` for reports that contain structured fields and narrative text
- `Free-text-only report` for reports that only contain narrative text

### Mask token

This is the text that replaces sensitive information.

Default value:

`[REDACTED]`

## Output Files

The downloaded `.zip` file contains:

- one anonymized text file for each input report
- one `.json` metadata file for each input report

## Option 2: Google Colab

If you prefer not to install anything locally, you can use the Colab notebook:

[Open in Colab](https://colab.research.google.com/github/VanessaLislevand/greek-medical-anonymization/blob/main/Run_Anonymization_Colab.ipynb)

Inside Colab:

1. open the notebook
2. run the cells from top to bottom
3. upload your files
4. review the anonymized output
5. download the generated `.zip`

## Troubleshooting

### `pip` is not found

Use:

```bash
python -m pip install -e ".[ml,ui]"
```

instead of:

```bash
pip install -e ".[ml,ui]"
```

### `greek-med-anonymizer-ui` is not found

This usually means one of these:

- the virtual environment is not activated
- the package installation did not finish successfully

Activate the environment again and rerun:

```bash
python -m pip install -e ".[ml,ui]"
```

### The model download fails

Check that:

- the computer has internet access
- Google Drive is reachable from the network

### A folder upload does not work

Make sure the folder was uploaded as a real `.zip` archive, not as a renamed file.

## Supported Input Formats

- `.docx`
- `.txt`
- `.zip` containing `.docx` and/or `.txt`
