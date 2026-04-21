from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass(slots=True)
class RuleConfig:
    phones: bool = True
    patient_ids: bool = True


@dataclass(slots=True)
class TemplateSectionConfig:
    name: str
    start_after: str | None = None
    end_before: str | None = None
    enabled_rules: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ModelConfig:
    enabled: bool = False
    model_dir: str | None = None
    labels_to_mask: list[str] = field(default_factory=lambda: ["PHI", "PERSON_NAME", "HOSPITAL_NAME"])
    aggregation_strategy: str = "simple"


@dataclass(slots=True)
class AppConfig:
    input_glob: str = "*.txt"
    output_suffix: str = ".anon.txt"
    mask_token: str = "[REDACTED]"
    processing_mode: str = "auto"
    rules: RuleConfig = field(default_factory=RuleConfig)
    template_sections: list[TemplateSectionConfig] = field(default_factory=list)
    model: ModelConfig = field(default_factory=ModelConfig)


def load_config(path: str | Path) -> AppConfig:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return AppConfig(
        input_glob=raw.get("input_glob", "*.txt"),
        output_suffix=raw.get("output_suffix", ".anon.txt"),
        mask_token=raw.get("mask_token", "[REDACTED]"),
        processing_mode=raw.get("processing_mode", "auto"),
        rules=RuleConfig(**raw.get("rules", {})),
        template_sections=[
            TemplateSectionConfig(**section) for section in raw.get("template_sections", [])
        ],
        model=ModelConfig(**raw.get("model", {})),
    )
