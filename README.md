# Greek Medical Report Anonymizer

Αυτό το repository είναι ένα αρχικό wrapping για να μεταφερθεί η δουλειά από notebooks σε επαναχρησιμοποιήσιμο εργαλείο.

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

## Γρήγορη χρήση

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
greek-med-anonymizer anonymize \
  --input /path/to/reports-or-docx \
  --output /path/to/anonymized \
  --config /path/to/config.json
```

## Config example

Υπάρχει παράδειγμα στο [examples/config.example.json](/Users/vanessalislevand/Documents/New%20project/examples/config.example.json).

Για local smoke test με πραγματικό model path υπάρχει και το [config.local-example.json](/Users/vanessalislevand/Documents/New%20project/examples/config.local-example.json).

Μπορείς επίσης να ορίσεις `processing_mode`:
- `auto`
- `mixed`
- `free_text_only`
- `template_only`

## Runbook

Υπάρχει αναλυτικό setup και smoke-test guide στο [RUNBOOK.md](/Users/vanessalislevand/Documents/New%20project/RUNBOOK.md).

## Επόμενα βήματα για migration από notebooks

1. Μεταφορά των regex/template rules στα `rules.py` και `templates.py`
2. Export ή αποθήκευση του trained model σε local directory
3. Σύνδεση label mapping στο `xlm_inference.py`
4. Μεταφορά preprocessing σε καθαρές functions
5. Προσθήκη tests με πραγματικά redacted examples
