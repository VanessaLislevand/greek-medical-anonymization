from __future__ import annotations

from greek_med_anonymizer.config import AppConfig
from greek_med_anonymizer.free_text_rules import (
    detect_patient_id_entities as detect_free_text_patient_id_entities,
    detect_phone_entities as detect_free_text_phone_entities,
    is_noise_entity_text,
    overlaps_any,
)
from greek_med_anonymizer.models import AnonymizationResult, Entity
from greek_med_anonymizer.rules import detect_patient_id_entities, detect_phone_entities
from greek_med_anonymizer.template_rules import detect_template_entities
from greek_med_anonymizer.templates import build_sections_for_mode
from greek_med_anonymizer.xlm_inference import XLMRDetector


class AnonymizationPipeline:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.model_detector = None
        if config.model.enabled and config.model.model_dir:
            self.model_detector = XLMRDetector(
                model_dir=config.model.model_dir,
                labels_to_mask=config.model.labels_to_mask,
                aggregation_strategy=config.model.aggregation_strategy,
            )

    def anonymize_text(self, text: str) -> AnonymizationResult:
        entities = self._collect_entities(text)
        anonymized_text = self._apply_mask(text, entities)
        return AnonymizationResult(
            original_text=text,
            anonymized_text=anonymized_text,
            entities=entities,
        )

    def _collect_entities(self, text: str) -> list[Entity]:
        sections = build_sections_for_mode(text, self.config.processing_mode)
        entities: list[Entity] = []

        for section in sections:
            section_text = section.text
            section_entities: list[Entity] = []

            if section.name.startswith("template"):
                section_entities.extend(detect_template_entities(section_text))
                if self.config.rules.phones:
                    section_entities.extend(detect_phone_entities(section_text))
                if self.config.rules.patient_ids:
                    section_entities.extend(detect_patient_id_entities(section_text))

            elif section.name == "free_text":
                if self.config.rules.phones:
                    section_entities.extend(detect_free_text_phone_entities(section_text))
                if self.config.rules.patient_ids:
                    section_entities.extend(detect_free_text_patient_id_entities(section_text))
                if self.model_detector is not None:
                    protected = [(entity.start, entity.end) for entity in section_entities]
                    for entity in self.model_detector.detect(section_text):
                        if overlaps_any(entity.start, entity.end, protected):
                            continue
                        if is_noise_entity_text(entity.text):
                            continue
                        section_entities.append(entity)

            else:
                if self.config.rules.phones:
                    section_entities.extend(detect_free_text_phone_entities(section_text))
                if self.config.rules.patient_ids:
                    section_entities.extend(detect_free_text_patient_id_entities(section_text))
                if self.model_detector is not None:
                    section_entities.extend(self.model_detector.detect(section_text))

            entities.extend(self._offset_entities(section.start, section_entities))

        return self._merge_entities(entities)

    @staticmethod
    def _offset_entities(offset: int, entities: list[Entity]) -> list[Entity]:
        return [
            Entity(
                start=entity.start + offset,
                end=entity.end + offset,
                label=entity.label,
                text=entity.text,
                source=entity.source,
            )
            for entity in entities
        ]

    @staticmethod
    def _merge_entities(entities: list[Entity]) -> list[Entity]:
        if not entities:
            return []

        ordered = sorted(entities, key=lambda item: (item.start, -(item.end - item.start)))
        merged = [ordered[0]]

        for entity in ordered[1:]:
            previous = merged[-1]
            if entity.start < previous.end:
                if entity.end > previous.end:
                    merged[-1] = Entity(
                        start=previous.start,
                        end=entity.end,
                        label=previous.label,
                        text=previous.text,
                        source=f"{previous.source}|{entity.source}",
                    )
                continue
            merged.append(entity)

        return merged

    def _apply_mask(self, text: str, entities: list[Entity]) -> str:
        if not entities:
            return text

        parts: list[str] = []
        cursor = 0
        for entity in entities:
            parts.append(text[cursor:entity.start])
            parts.append(self.config.mask_token)
            cursor = entity.end
        parts.append(text[cursor:])
        return "".join(parts)
