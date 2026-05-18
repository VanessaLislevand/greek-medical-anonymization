# Greek Medical Report Anonymization

This tool anonymizes Greek medical reports through a simple local web interface.

It supports:

- single `.docx` or `.txt` reports
- multiple reports uploaded together
- a `.zip` archive containing a folder of reports

## Before First Use

Open Terminal and clone the repository:

```bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_FOLDER>
```

Then run:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[ml,ui]'
```

The model files should be placed in:

```text
models/xlmr_phi_final
```

## Manual Start

After the first-time setup, the easiest way to open the tool is:

- Mac: double-click `Start_Anonymizer.command`
- Windows: double-click `Start_Anonymizer.bat`

If a browser window does not open automatically, open the local address shown in Terminal, usually:

```text
http://localhost:8501
```

## Start The App

You can also start it manually:

```bash
cd <REPOSITORY_FOLDER>
source .venv/bin/activate
greek-med-anonymizer-ui
```

## How To Use

1. Select the report type.
2. Upload one report, multiple reports, or a `.zip` file containing a folder of reports.
3. If needed, change the mask token under `Advanced options`.
4. Click `Run anonymization`.
5. Download the generated `.zip` file.

## Report Types

- `Report with template and free text`: use for reports that contain both structured fields and free text
- `Free-text-only report`: use for narrative reports without a fixed template
- `Template-only report`: use for reports that are mostly structured template fields

## Output

The downloaded `.zip` file contains:

- anonymized text output for each report
- a `.json` metadata file for each report

## Notes

- Input reports can be `.docx` or `.txt`.
- For folder upload, first create a real `.zip` archive of the folder.
- The tool runs locally on the computer where it is launched.
