# Greek Medical Report Anonymization

This repository contains a hybrid pipeline for anonymizing Greek medical reports. The approach combines rule-based processing for structured template fields with transformer-based PHI detection for free-text content.

## Overview

The pipeline supports:

- document ingestion from `.docx` and `.txt`
- template-aware anonymization for structured sections
- regex-based detection of phone numbers and patient IDs
- XLM-R-based detection of PHI spans in free text
- configurable processing modes for mixed-format and free-text-only reports

## Repository Structure

```text
src/greek_med_anonymizer/
  cli.py
  pipeline.py
  rules.py
  template_rules.py
  free_text_rules.py
  templates.py
  xlm_inference.py
  config.py
  io_utils.py
  docx_io.py
```

## Installation

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[ml]'
```

## Inference

```bash
greek-med-anonymizer anonymize \
  --input /path/to/report_or_directory \
  --output /path/to/output \
  --config /path/to/config.json
```

The input may be either:

- a single report file
- a directory of reports for batch processing

## Configuration

Example configuration files are provided in:

- `examples/config.example.json`
- `examples/config.local-example.json`
- `examples/config.mixed.example.json`
- `examples/config.free_text_only.example.json`

Supported `processing_mode` values:

- `auto`
- `mixed`
- `free_text_only`
- `template_only`

## Output

The pipeline produces:

- an anonymized text file
- optional span-level metadata in JSON format

## Notes

- Medical reports, model weights, and generated outputs are intended to remain outside the repository.
- The exported model is provided through a local path specified in the selected configuration file.
