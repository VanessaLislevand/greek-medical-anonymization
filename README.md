# Greek Medical Report Anonymization

This tool anonymizes Greek medical reports. It can be used either through Google Colab or through a simple local web app.

## Option 1: Google Colab

[Open in Colab](https://colab.research.google.com/github/delta-icu/de-identification/blob/main/Run_Anonymization_Colab.ipynb)

Steps:

1. Open the notebook in Colab.
2. Run the cells from top to bottom.
3. Upload one report, multiple reports, or a `.zip` file containing a folder of reports.
4. Review the full anonymized output inside the notebook.
5. Download the generated `.zip` file.

## Option 2: Local Web App

From the project folder, install the package and launch the app:

```bash
pip install -e ".[ml,ui]"
greek-med-anonymizer-ui
```

The web app will:

- download the model automatically if it is not already available
- accept `.docx`, `.txt`, or `.zip` uploads
- anonymize one or multiple reports
- show the full anonymized output for each file
- provide a download button for the output `.zip`

## Settings

Both interfaces expose only two main settings:

- `Report type`
- `Mask token`

Available report types:

- `Report with template and free text`
- `Free-text-only report`

## Output

The output `.zip` file contains:

- one anonymized text file for each report
- one `.json` metadata file for each report

## Notes

- Input reports can be `.docx` or `.txt`.
- Folder upload should be provided as a real `.zip` archive.
- The model is downloaded automatically from a shareable link when needed.
