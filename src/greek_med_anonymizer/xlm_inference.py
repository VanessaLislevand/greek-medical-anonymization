from __future__ import annotations

from greek_med_anonymizer.models import Entity
from greek_med_anonymizer.free_text_rules import normalize_model_label


class XLMRDetector:
    def __init__(
        self,
        model_dir: str,
        labels_to_mask: list[str],
        aggregation_strategy: str = "simple",
    ) -> None:
        self.model_dir = model_dir
        self.labels_to_mask = set(labels_to_mask)
        self.aggregation_strategy = aggregation_strategy
        self._pipeline = None

    def _load(self) -> None:
        if self._pipeline is not None:
            return

        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError(
                "The optional 'ml' dependencies are not installed. Install with: pip install -e .[ml]"
            ) from exc

        self._pipeline = pipeline(
            task="token-classification",
            model=self.model_dir,
            tokenizer=self.model_dir,
            aggregation_strategy=self.aggregation_strategy,
        )

    def detect(self, text: str) -> list[Entity]:
        self._load()
        predictions = self._pipeline(text)
        entities: list[Entity] = []
        for prediction in predictions:
            raw_label = prediction.get("entity_group") or prediction.get("entity")
            normalized_label = normalize_model_label(raw_label)
            if normalized_label not in self.labels_to_mask:
                continue
            start = int(prediction["start"])
            end = int(prediction["end"])
            entities.append(
                Entity(
                    start=start,
                    end=end,
                    label=normalized_label,
                    text=text[start:end],
                    source="model:xlmr",
                )
            )
        return entities
