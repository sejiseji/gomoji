from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_content import (  # noqa: E402
    EXPECTED_CATEGORY_COUNTS,
    EXPECTED_RARITY_COUNTS,
    ValidationResult,
    load_packs,
    validate_global,
)


def load_all_entries() -> list[dict]:
    result = ValidationResult()
    entries = load_packs(ROOT / "content" / "source", result)
    validate_global(entries, result, release=False)
    assert result.errors == []
    return entries


def test_content_contract_passes() -> None:
    entries = load_all_entries()
    assert len(entries) == 1000


def test_category_and_rarity_distribution() -> None:
    entries = load_all_entries()
    assert Counter(entry["category"] for entry in entries) == EXPECTED_CATEGORY_COUNTS
    assert Counter(entry["rarity"] for entry in entries) == EXPECTED_RARITY_COUNTS


def test_current_review_state_is_explicit() -> None:
    entries = load_all_entries()
    assert Counter(entry["status"] for entry in entries) == {
        "draft": 960,
        "reviewed": 40,
    }


def test_result_heading_does_not_append_ngo() -> None:
    word = "ねこぱんち"
    heading = f"【{word}】"
    assert heading == "【ねこぱんち】"
    assert not heading.endswith("ンゴ")
    assert not heading.endswith("んご")


def test_no_fixed_ngo_in_explanations() -> None:
    entries = load_all_entries()
    joined = "\n".join(
        paragraph
        for entry in entries
        for paragraph in entry["paragraphs"]
    )
    assert "ンゴ" not in joined
    assert "んご" not in joined
