# Runbook

## Στόχος

Να τρέξει το εργαλείο ανωνυμοποίησης τοπικά πάνω σε ελληνικά ιατρικά reports, με:

- template-aware rules για structured/template sections
- regex rules για τηλέφωνα και patient ids
- fine-tuned XLM-R για free-text PHI detection

## Τι περιμένει το σύστημα αυτή τη στιγμή

- input σε `.docx` ή `.txt`
- free text section που ξεκινά από `ΑΙΤΙΑ ΕΙΣΟΔΟΥ - ΙΣΤΟΡΙΚΟ` ή παραλλαγές με en dash / em dash
- template tail που ξεκινά από `Ο Διευθυντής`
- XLM-R model που έχει εκπαιδευτεί ως binary token classifier με labels:
  - `O`
  - `B-PHI`
  - `I-PHI`

## 1. Environment setup

Αν δεν υπάρχουν ακόμα τα Apple Command Line Tools:

```bash
xcode-select --install
```

Μετά:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[ml]
```

## 2. Model export

Χρειαζόμαστε ένα local directory που να περιέχει export από Hugging Face / Transformers model, συνήθως με αρχεία όπως:

```text
config.json
tokenizer.json
tokenizer_config.json
special_tokens_map.json
model.safetensors
```

ή εναλλακτικά:

```text
pytorch_model.bin
config.json
...
```

## 3. Config preparation

Πάρε το example:

- [config.local-example.json](/Users/vanessalislevand/Documents/New%20project/examples/config.local-example.json)

και άλλαξε μόνο:

- `model.model_dir`
- `processing_mode` αν θες διαφορετική στρατηγική
- προαιρετικά `input_glob`
- προαιρετικά `mask_token`

### `processing_mode`

Υποστηρίζονται:

- `auto`
  - ίδια συμπεριφορά με τώρα
  - προσπαθεί να βρει template/free-text split
  - αν δεν βρει boundaries, πέφτει σε `full_text`

- `mixed`
  - ίδιο με το `auto`, αλλά δηλώνει ρητά ότι περιμένεις mixed report

- `free_text_only`
  - όλο το report αντιμετωπίζεται ως free text
  - ιδανικό για reports από άλλο νοσοκομείο χωρίς template fields

- `template_only`
  - όλο το report αντιμετωπίζεται ως template/structured text

## 4. Smoke test

Για ένα αρχείο:

```bash
greek-med-anonymizer anonymize \
  --input /absolute/path/to/report.docx \
  --output /absolute/path/to/output/report.anon.txt \
  --config /Users/vanessalislevand/Documents/New\ project/examples/config.local-example.json \
  --emit-metadata
```

Για φάκελο:

```bash
greek-med-anonymizer anonymize \
  --input /absolute/path/to/reports \
  --output /absolute/path/to/anonymized \
  --config /Users/vanessalislevand/Documents/New\ project/examples/config.local-example.json \
  --emit-metadata
```

## 5. Τι να ελέγξεις στο output

- τα τηλέφωνα έχουν αντικατασταθεί
- τα patient ids έχουν αντικατασταθεί
- το free text anonymized output περιέχει redactions σε ονόματα / νοσοκομεία / άλλο PHI
- το metadata json γράφει spans με:
  - `start`
  - `end`
  - `label`
  - `text`
  - `source`

## 6. Πώς να διαβάσεις τα labels

Αυτή τη στιγμή τα labels μπορεί να προέρχονται από:

- rules:
  - `PHONE`
  - `PATIENT_ID`
  - `STAFF_NAME`
  - άλλα template labels
- model:
  - `PHI`

Το `PHI` εδώ σημαίνει ότι το model βρήκε ευαίσθητο span, χωρίς να το κατηγοριοποιεί περαιτέρω.

## 7. Πιθανά πρώτα failures

Αν αποτύχει το model loading:

- έλεγξε ότι το `model_dir` δείχνει σε σωστό exported directory
- έλεγξε ότι το `pip install -e .[ml]` ολοκληρώθηκε

Αν το free-text split δεν είναι σωστό:

- πιθανόν κάποιο report έχει διαφορετικό heading από το `ΑΙΤΙΑ ΕΙΣΟΔΟΥ - ΙΣΤΟΡΙΚΟ`
- πιθανόν κάποιο report δεν έχει το `Ο Διευθυντής`

Αν το template anonymization χάσει πεδία:

- πιθανόν το template wording διαφέρει από τα regex patterns

## 8. Τι θα κάνουμε μετά το πρώτο smoke test

Μετά το πρώτο επιτυχημένο run, το επόμενο iteration θα είναι:

1. έλεγχος σε 3-5 πραγματικά reports
2. καταγραφή false negatives / false positives
3. βελτίωση regex/template rules
4. βελτίωση post-processing του model output
5. προαιρετικά export σε API ή UI
