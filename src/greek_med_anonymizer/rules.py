from __future__ import annotations

import re

from greek_med_anonymizer.models import Entity


PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+30\s?)?(?:2\d{2}|69\d)\s?\d{3}\s?\d{4}(?!\d)")
PATIENT_ID_PATTERN = re.compile(r"(?i)\b(?:patient[\s_-]?id|id[\s_-]?ασθεν(?:η|ούς)?|αμκ(?:α)?|mrn)\s*[:#-]?\s*[a-z0-9\-]{4,}\b")


def detect_phone_entities(text: str) -> list[Entity]:
    return [
        Entity(
            start=match.start(),
            end=match.end(),
            label="PHONE",
            text=match.group(0),
            source="rule:phone",
        )
        for match in PHONE_PATTERN.finditer(text)
    ]


def detect_patient_id_entities(text: str) -> list[Entity]:
    return [
        Entity(
            start=match.start(),
            end=match.end(),
            label="PATIENT_ID",
            text=match.group(0),
            source="rule:patient_id",
        )
        for match in PATIENT_ID_PATTERN.finditer(text)
    ]
