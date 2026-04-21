from __future__ import annotations

import re

from greek_med_anonymizer.models import Entity


PHONE_REGEX = re.compile(
    r"""
    (?:
        @\d{5,}
        |
        (?:(?:\(\s*\+30\s*\)|\+30)\s*[-–—]?\s*)?
        (?:
            69\d(?:[\s\-]?\d){7}
            |
            2\d{2}(?:[\s\-]?\d){7}
            |
            2\d{3}(?:[\s\-]?\d){6}
        )
    )
    """,
    re.VERBOSE,
)

PATIENT_ID_REGEX = re.compile(r"(?<!\d)\d{8}(?!\d)")
_NOISE_EQ = {"ΜΕΘ", "ΤΕΠ", "ΠΓΝΙ"}


def detect_phone_entities(text: str) -> list[Entity]:
    if not text:
        return []
    return [
        Entity(match.start(), match.end(), "PHONE", match.group(0), "rule:free_text_phone")
        for match in PHONE_REGEX.finditer(text)
    ]


def detect_patient_id_entities(text: str) -> list[Entity]:
    if not text:
        return []
    return [
        Entity(match.start(), match.end(), "PATIENT_ID", match.group(0), "rule:free_text_patient_id")
        for match in PATIENT_ID_REGEX.finditer(text)
    ]


def normalize_model_label(label: str) -> str:
    if not label:
        return "MISC"
    normalized = str(label).upper()
    if normalized in {"PHI", "B-PHI", "I-PHI"} or normalized.endswith("-PHI"):
        return "PHI"
    if "PER" in normalized or "PERSON" in normalized:
        return "PERSON_NAME"
    if "ORG" in normalized:
        return "HOSPITAL_NAME"
    if "LOC" in normalized or "GPE" in normalized:
        return "LOCATION"
    return "MISC"


def normalize_noise_token(value: str) -> str:
    normalized = (value or "").strip().upper()
    return re.sub(r"[\s\.\-–—\(\)\[\]\{\}]+", "", normalized)


def is_noise_entity_text(entity_text: str) -> bool:
    token = normalize_noise_token(entity_text)
    if not token:
        return True
    if token in _NOISE_EQ:
        return True
    if token.startswith("ΠΓΝΙ"):
        return True
    return False


def overlaps_any(start: int, end: int, ranges: list[tuple[int, int]]) -> bool:
    for left, right in ranges:
        if max(start, left) < min(end, right):
            return True
    return False
