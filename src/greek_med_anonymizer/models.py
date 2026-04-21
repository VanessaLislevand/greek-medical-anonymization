from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, order=True)
class Entity:
    start: int
    end: int
    label: str
    text: str
    source: str


@dataclass(slots=True)
class AnonymizationResult:
    original_text: str
    anonymized_text: str
    entities: list[Entity]
