#!/usr/bin/env python3
"""Validate ごもじンゴ content packs using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

ALLOWED_HIRAGANA = frozenset(
    "あいうえお"
    "かきくけこ"
    "さしすせそ"
    "たちつてと"
    "なにぬねの"
    "はひふへほ"
    "まみむめも"
    "やゆよ"
    "らりるれろ"
    "わをん"
    "がぎぐげご"
    "ざじずぜぞ"
    "だぢづでど"
    "ばびぶべぼ"
    "ぱぴぷぺぽ"
    "ゔ"
    "ぁぃぅぇぉ"
    "っゃゅょゎ"
)

CATEGORIES = (
    "phenomenon",
    "condition",
    "creature",
    "food",
    "technique",
    "tool",
    "custom",
    "place",
    "internet",
    "mystery",
)
TONES = ("deadpan", "mock_academic", "observational", "dry", "absurd")
STATUSES = ("draft", "reviewed", "approved", "retired")
SOURCE_KINDS = ("manual_seed", "combinatorial_draft", "manual_revision")

EXPECTED_CATEGORY_COUNTS = {
    "phenomenon": 160,
    "condition": 130,
    "creature": 110,
    "food": 100,
    "technique": 100,
    "tool": 100,
    "custom": 100,
    "place": 80,
    "internet": 70,
    "mystery": 50,
}
EXPECTED_RARITY_COUNTS = {1: 500, 2: 300, 3: 150, 4: 45, 5: 5}

ENTRY_KEYS = {
    "id",
    "word",
    "category",
    "rarity",
    "paragraphs",
    "tags",
    "tone",
    "ending_family",
    "status",
    "source_kind",
    "editor_note",
}


class ValidationResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def normalize_word(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def load_packs(source_dir: Path, result: ValidationResult) -> list[dict[str, Any]]:
    files = sorted(source_dir.glob("pack_*.json"))
    if not files:
        result.error(f"No pack files found under: {source_dir}")
        return []

    entries: list[dict[str, Any]] = []
    expected_pack_number = 1

    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            result.error(f"{path.name}: could not read JSON: {exc}")
            continue

        expected_pack_id = f"pack_{expected_pack_number:03d}"
        if payload.get("schema_version") != 2:
            result.error(f"{path.name}: schema_version must be 2")
        if payload.get("pack_id") != expected_pack_id:
            result.error(
                f"{path.name}: pack_id must be {expected_pack_id!r}, "
                f"got {payload.get('pack_id')!r}"
            )

        pack_entries = payload.get("entries")
        if not isinstance(pack_entries, list):
            result.error(f"{path.name}: entries must be an array")
            expected_pack_number += 1
            continue

        if payload.get("entry_count") != len(pack_entries):
            result.error(
                f"{path.name}: entry_count={payload.get('entry_count')!r} "
                f"but actual count is {len(pack_entries)}"
            )
        if len(pack_entries) != 50:
            result.error(f"{path.name}: each source pack must contain exactly 50 entries")

        if pack_entries:
            actual_range = [pack_entries[0].get("id"), pack_entries[-1].get("id")]
            if payload.get("id_range") != actual_range:
                result.error(
                    f"{path.name}: id_range must be {actual_range!r}, "
                    f"got {payload.get('id_range')!r}"
                )

        entries.extend(pack_entries)
        expected_pack_number += 1

    if len(files) != 20:
        result.error(f"Expected 20 packs, found {len(files)}")
    return entries


def validate_entry(entry: Any, index: int, result: ValidationResult) -> None:
    label = f"entry[{index}]"
    if not isinstance(entry, dict):
        result.error(f"{label}: entry must be an object")
        return

    unknown = set(entry) - ENTRY_KEYS
    missing = ENTRY_KEYS - set(entry)
    if unknown:
        result.error(f"{label}: unknown fields: {sorted(unknown)}")
    if missing:
        result.error(f"{label}: missing fields: {sorted(missing)}")

    entry_id = entry.get("id")
    if not isinstance(entry_id, str) or len(entry_id) != 7:
        result.error(f"{label}: invalid id: {entry_id!r}")
    elif not (entry_id.startswith("GMG") and entry_id[3:].isdigit()):
        result.error(f"{label}: id must match GMG0001 format: {entry_id!r}")
    else:
        label = entry_id

    word = entry.get("word")
    if not isinstance(word, str):
        result.error(f"{label}: word must be a string")
    else:
        normalized = normalize_word(word)
        if word != normalized:
            result.error(f"{label}: word must already be NFC-normalized and trimmed")
        if len(normalized) != 5:
            result.error(f"{label}: word must be exactly 5 Unicode characters: {word!r}")
        invalid_chars = sorted(set(normalized) - ALLOWED_HIRAGANA)
        if invalid_chars:
            result.error(f"{label}: word contains invalid characters: {invalid_chars}")

    category = entry.get("category")
    if category not in CATEGORIES:
        result.error(f"{label}: invalid category: {category!r}")

    rarity = entry.get("rarity")
    if not isinstance(rarity, int) or isinstance(rarity, bool) or not 1 <= rarity <= 5:
        result.error(f"{label}: rarity must be an integer from 1 to 5")

    paragraphs = entry.get("paragraphs")
    if not isinstance(paragraphs, list) or not 2 <= len(paragraphs) <= 4:
        result.error(f"{label}: paragraphs must contain 2 to 4 strings")
    else:
        for paragraph_index, paragraph in enumerate(paragraphs):
            if not isinstance(paragraph, str) or not paragraph.strip():
                result.error(
                    f"{label}: paragraphs[{paragraph_index}] must be a non-empty string"
                )
        if all(isinstance(p, str) for p in paragraphs):
            total_length = sum(len(p) for p in paragraphs)
            if not 50 <= total_length <= 150:
                result.error(
                    f"{label}: total paragraph length must be 50..150, got {total_length}"
                )
            if len(set(paragraphs)) != len(paragraphs):
                result.error(f"{label}: duplicate paragraph inside one entry")
            joined = "\n".join(paragraphs)
            if "ンゴ" in joined or "んご" in joined:
                result.warn(
                    f"{label}: explanation contains 'ンゴ/んご'; "
                    "confirm that this is deliberate and not a fixed suffix"
                )

    tags = entry.get("tags")
    if not isinstance(tags, list) or not 1 <= len(tags) <= 6:
        result.error(f"{label}: tags must contain 1 to 6 strings")
    elif any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        result.error(f"{label}: tags must be non-empty strings")
    elif len(tags) != len(set(tags)):
        result.error(f"{label}: tags must be unique within the entry")

    tone = entry.get("tone")
    if tone not in TONES:
        result.error(f"{label}: invalid tone: {tone!r}")

    ending_family = entry.get("ending_family")
    if (
        not isinstance(ending_family, str)
        or not ending_family
        or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789_" for ch in ending_family)
    ):
        result.error(f"{label}: invalid ending_family: {ending_family!r}")

    status = entry.get("status")
    if status not in STATUSES:
        result.error(f"{label}: invalid status: {status!r}")

    source_kind = entry.get("source_kind")
    if source_kind not in SOURCE_KINDS:
        result.error(f"{label}: invalid source_kind: {source_kind!r}")

    editor_note = entry.get("editor_note")
    if not isinstance(editor_note, str):
        result.error(f"{label}: editor_note must be a string")


def validate_global(
    entries: list[dict[str, Any]],
    result: ValidationResult,
    *,
    release: bool,
) -> None:
    for index, entry in enumerate(entries):
        validate_entry(entry, index, result)

    ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    words = [entry.get("word") for entry in entries if isinstance(entry, dict)]
    descriptions = [
        "\n".join(entry.get("paragraphs", []))
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("paragraphs"), list)
    ]
    final_paragraphs = [
        entry["paragraphs"][-1]
        for entry in entries
        if isinstance(entry, dict)
        and isinstance(entry.get("paragraphs"), list)
        and entry["paragraphs"]
    ]

    for name, values in (
        ("id", ids),
        ("word", words),
        ("full description", descriptions),
        ("final paragraph", final_paragraphs),
    ):
        duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
        if duplicates:
            preview = duplicates[:10]
            result.error(f"Duplicate {name} values ({len(duplicates)}): {preview!r}")

    if len(entries) == 1000:
        expected_ids = [f"GMG{number:04d}" for number in range(1, 1001)]
        if ids != expected_ids:
            result.error("IDs must be contiguous and ordered from GMG0001 to GMG1000")

        category_counts = Counter(entry.get("category") for entry in entries)
        if dict(category_counts) != EXPECTED_CATEGORY_COUNTS:
            result.error(
                f"Category counts differ from contract: {dict(category_counts)!r}"
            )

        rarity_counts = Counter(entry.get("rarity") for entry in entries)
        if dict(rarity_counts) != EXPECTED_RARITY_COUNTS:
            result.error(f"Rarity counts differ from contract: {dict(rarity_counts)!r}")
    else:
        result.warn(f"Development corpus contains {len(entries)} entries, not 1000")

    status_counts = Counter(entry.get("status") for entry in entries)
    if release:
        if len(entries) != 1000:
            result.error("--release requires exactly 1000 entries")
        if status_counts.get("approved", 0) != 1000:
            result.error(
                "--release requires 1000 approved entries; "
                f"current status counts: {dict(status_counts)!r}"
            )
        if status_counts.get("draft", 0) or status_counts.get("reviewed", 0):
            result.error("--release forbids draft/reviewed entries")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "content" / "source",
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="Apply release gate: all 1000 entries must be approved.",
    )
    args = parser.parse_args()

    result = ValidationResult()
    entries = load_packs(args.source_dir, result)
    validate_global(entries, result, release=args.release)

    status_counts = Counter(entry.get("status") for entry in entries)
    category_counts = Counter(entry.get("category") for entry in entries)

    print(f"source_dir: {args.source_dir}")
    print(f"entries: {len(entries)}")
    print(f"status: {dict(status_counts)}")
    print(f"categories: {dict(category_counts)}")
    print(f"warnings: {len(result.warnings)}")
    for warning in result.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if result.errors:
        print(f"errors: {len(result.errors)}", file=sys.stderr)
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("errors: 0")
    print("content validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
