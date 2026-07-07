# Greek Medical Report Anonymization

This repository provides two ways to anonymize Greek medical reports:

1. a local web app
2. a Google Colab notebook

For most users, the easiest option is the local web app.

## Web App

The web app:

- accepts `.docx`, `.txt`, or `.zip` files
- supports one or multiple reports
- shows the full anonymized output on screen
- lets you download a `.zip` file with the results
- downloads the model automatically the first time it runs

You need:

- Python 3.10 or newer
- internet access the first time the app runs

## Windows Setup

1. Download this repository from GitHub as a `.zip` file and extract it.
2. Open the extracted folder.
3. Click in the folder address bar, type `powershell`, and press Enter.
4. Run:

```powershell
py --version
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[ml,ui]"
greek-med-anonymizer-ui
```

If `py -3.10 -m venv .venv` does not work, try:

```powershell
py -m venv .venv
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

The app should open at:

`http://localhost:8501`

## Mac Setup

1. Download this repository from GitHub as a `.zip` file and extract it.
2. Open Terminal inside the project folder.
3. Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[ml,ui]"
greek-med-anonymizer-ui
```

The app should open at:

`http://localhost:8501`

## How To Use The Web App

1. Choose the report type.
2. Keep the default mask token or change it.
3. Upload one or more `.docx` or `.txt` files.
4. If you want to upload a whole folder, first compress it as a real `.zip` file and upload the `.zip`.
5. Click `Run anonymization`.
6. Review the anonymized output shown on screen.
7. Download the generated `.zip` file.

## Report Types

- `Report with template and free text`: for reports with structured template fields and narrative text
- `Free-text-only report`: for reports that only contain narrative text

## Output

The downloaded `.zip` file contains:

- one anonymized text file for each report
- one `.json` metadata file for each report

## Colab Option

If you prefer not to install anything locally, use the notebook:

[Open in Colab](https://colab.research.google.com/github/VanessaLislevand/greek-medical-anonymization/blob/main/Run_Anonymization_Colab.ipynb)

Inside Colab:

1. open the notebook
2. run the cells from top to bottom
3. upload your files
4. review the anonymized output
5. download the generated `.zip`

## Troubleshooting

If `pip` is not found, use:

```bash
python -m pip install -e ".[ml,ui]"
```

If `greek-med-anonymizer-ui` is not found, the virtual environment is usually not activated or the installation did not finish successfully.

If folder upload fails, make sure the folder was uploaded as a real `.zip` archive.
