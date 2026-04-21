from __future__ import annotations

import argparse
import json
from pathlib import Path

from greek_med_anonymizer.config import load_config
from greek_med_anonymizer.io_utils import build_output_path, collect_input_files, read_input_text
from greek_med_anonymizer.pipeline import AnonymizationPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="greek-med-anonymizer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    anonymize_parser = subparsers.add_parser("anonymize", help="Anonymize one file or a directory")
    anonymize_parser.add_argument("--input", required=True, help="Input file or directory")
    anonymize_parser.add_argument("--output", required=True, help="Output file or directory")
    anonymize_parser.add_argument("--config", required=True, help="Path to JSON config")
    anonymize_parser.add_argument(
        "--emit-metadata",
        action="store_true",
        help="Emit JSON metadata with detected entities next to each output file",
    )
    return parser


def run_anonymize(input_path: str, output_path: str, config_path: str, emit_metadata: bool) -> int:
    config = load_config(config_path)
    pipeline = AnonymizationPipeline(config)
    source = Path(input_path)
    destination = Path(output_path)
    files = collect_input_files(source, config.input_glob)

    if not files:
        raise FileNotFoundError(f"No input files found under: {source}")

    if source.is_file():
        result = pipeline.anonymize_text(read_input_text(source))
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(result.anonymized_text, encoding="utf-8")
        if emit_metadata:
            _write_metadata(destination, result.entities)
        return 0

    destination.mkdir(parents=True, exist_ok=True)
    for input_file in files:
        output_file = build_output_path(input_file, source, destination, config.output_suffix)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        result = pipeline.anonymize_text(read_input_text(input_file))
        output_file.write_text(result.anonymized_text, encoding="utf-8")
        if emit_metadata:
            _write_metadata(output_file, result.entities)

    return 0


def _write_metadata(output_file: Path, entities: list) -> None:
    metadata_file = output_file.with_suffix(output_file.suffix + ".json")
    payload = [
        {
            "start": entity.start,
            "end": entity.end,
            "label": entity.label,
            "text": entity.text,
            "source": entity.source,
        }
        for entity in entities
    ]
    metadata_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "anonymize":
        return run_anonymize(
            input_path=args.input,
            output_path=args.output,
            config_path=args.config,
            emit_metadata=args.emit_metadata,
        )

    parser.error(f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
