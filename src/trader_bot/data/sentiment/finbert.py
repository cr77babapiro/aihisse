from __future__ import annotations

from functools import lru_cache
from typing import Iterable, List, Tuple


@lru_cache(maxsize=1)
def _get_pipeline():
    try:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline
    except Exception as exc:
        raise RuntimeError("transformers not installed") from exc
    model_name = "ProsusAI/finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)


def score_texts(texts: Iterable[str]) -> List[Tuple[str, float]]:
    """Return list of (label, score) representing dominant sentiment per text."""
    pipe = _get_pipeline()
    results = []
    for text in texts:
        scores = pipe(text)[0]
        # choose highest score label
        label = max(scores, key=lambda s: s["score"])  # type: ignore
        results.append((label["label"], float(label["score"])) )
    return results
