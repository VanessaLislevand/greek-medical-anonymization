# Greek Medical Report Anonymizer

Tool for anonymizing Greek medical reports with a hybrid pipeline that combines:

- template-aware rules για structured sections
- regex rules για τηλέφωνα και patient ids
- XLM-R token classification model για free-text PHI detection

## Τι περιλαμβάνει

- CLI για ανωνυμοποίηση ενός αρχείου ή ολόκληρου φακέλου
- config-driven pipeline
- υποστήριξη για `.txt` και `.docx`
- rule-based anonymization για τηλέφωνα και patient ids
- template-aware section handling
- model adapter για token classification μοντέλο όπως XLM-R
- υποστήριξη τόσο για binary `PHI` models όσο και για typed entity labels

## Ενδεικτική δομή

```text
src/greek_med_anonymizer/
  cli.py
  pipeline.py
  rules.py
  templates.py
  xlm_inference.py
  config.py
  io_utils.py
```

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[ml]'
```

## Inference

```bash
greek-med-anonymizer anonymize \
  --input /path/to/reports-or-docx \
  --output /path/to/anonymized \
  --config /path/to/config.json
```

Το `--input` μπορεί να είναι:

- ένα μεμονωμένο `.docx` ή `.txt` αρχείο
- ένας φάκελος για batch anonymization

## Config example

Υπάρχει παράδειγμα στο [examples/config.example.json](/Users/vanessalislevand/Documents/New%20project/examples/config.example.json).

Για local smoke test με πραγματικό model path υπάρχει και το [config.local-example.json](/Users/vanessalislevand/Documents/New%20project/examples/config.local-example.json).

Για reports με γνωστή/μικτή δομή υπάρχει και το [config.mixed.example.json](/Users/vanessalislevand/Documents/New%20project/examples/config.mixed.example.json).

Για reports που είναι εξ ολοκλήρου free text υπάρχει και το [config.free_text_only.example.json](/Users/vanessalislevand/Documents/New%20project/examples/config.free_text_only.example.json).

Μπορείς επίσης να ορίσεις `processing_mode`:
- `auto`
- `mixed`
- `free_text_only`
- `template_only`

## Runbook

Υπάρχει αναλυτικό setup και smoke-test guide στο [RUNBOOK.md](/Users/vanessalislevand/Documents/New%20project/RUNBOOK.md).

## Example commands

```bash
greek-med-anonymizer anonymize \
  --input "/absolute/path/to/report.docx" \
  --output "/absolute/path/to/report.anon.txt" \
  --config "/absolute/path/to/config.free_text_only.example.json" \
  --emit-metadata
```

```bash
greek-med-anonymizer anonymize \
  --input "/absolute/path/to/report.docx" \
  --output "/absolute/path/to/report.anon.txt" \
  --config "/absolute/path/to/config.mixed.example.json" \
  --emit-metadata
```

```bash
greek-med-anonymizer anonymize \
  --input "/absolute/path/to/reports_directory" \
  --output "/absolute/path/to/anonymized_directory" \
  --config "/absolute/path/to/config.free_text_only.example.json" \
  --emit-metadata
```

## Notes

- Actual medical reports, model weights, and generated outputs should remain outside the repository.
- The exported model should be provided via local path in the selected config file.

## Επόμενα βήματα

1. Μεταφορά των regex/template rules στα `rules.py` και `templates.py`
2. Export ή αποθήκευση του trained model σε local directory
3. Σύνδεση label mapping στο `xlm_inference.py`
4. Μεταφορά preprocessing σε καθαρές functions
5. Προσθήκη tests με πραγματικά redacted examples
