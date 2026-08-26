#!/usr/bin/env python3
"""Build deterministic Python content modules for ごもじンゴ."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from validate_content import ValidationResult, load_packs, validate_global


def canonical_json(entries: list[dict[str, Any]]) -> str:
    return json.dumps(
        entries,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def select_entries(
    entries: list[dict[str, Any]],
    *,
    include_drafts: bool,
    release: bool,
) -> list[dict[str, Any]]:
    if release:
        statuses = {"approved"}
    elif include_drafts:
        statuses = {"draft", "reviewed", "approved"}
    else:
        statuses = {"reviewed", "approved"}

    return [
        entry
        for entry in entries
        if entry.get("status") in statuses
    ]


def render_module(
    selected: list[dict[str, Any]],
    *,
    source_count: int,
    revision: str,
    include_drafts: bool,
) -> str:
    lines: list[str] = [
        '"""Generated content data. Do not edit by hand."""',
        "# ruff: noqa: E501",
        "",
        "from __future__ import annotations",
        "",
        "from typing import NamedTuple",
        "",
        "",
        "class ContentEntry(NamedTuple):",
        "    id: str",
        "    word: str",
        "    category: str",
        "    rarity: int",
        "    paragraphs: tuple[str, ...]",
        "    tags: tuple[str, ...]",
        "    tone: str",
        "    ending_family: str",
        "    status: str",
        "",
        "",
        "CONTENT_SCHEMA_VERSION = 2",
        f"CONTENT_REVISION = {revision!r}",
        f"CONTENT_SOURCE_COUNT = {source_count}",
        f"CONTENT_COUNT = {len(selected)}",
        f"CONTENT_INCLUDES_DRAFTS = {include_drafts!r}",
        "",
        "ENTRIES: tuple[ContentEntry, ...] = (",
    ]

    for entry in selected:
        lines.extend(
            [
                "    ContentEntry(",
                f"        id={entry['id']!r},",
                f"        word={entry['word']!r},",
                f"        category={entry['category']!r},",
                f"        rarity={entry['rarity']!r},",
                f"        paragraphs={tuple(entry['paragraphs'])!r},",
                f"        tags={tuple(entry['tags'])!r},",
                f"        tone={entry['tone']!r},",
                f"        ending_family={entry['ending_family']!r},",
                f"        status={entry['status']!r},",
                "    ),",
            ]
        )

    lines.extend(
        [
            ")",
            "",
            "BY_ID: dict[str, ContentEntry] = {entry.id: entry for entry in ENTRIES}",
            "BY_WORD: dict[str, ContentEntry] = {entry.word: entry for entry in ENTRIES}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=root / "content" / "source",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "generated" / "content_data.py",
    )
    parser.add_argument(
        "--include-drafts",
        action="store_true",
        help="Include draft entries for development builds.",
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="Require and include only 1000 approved entries.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the output differs from the deterministic build result.",
    )
    args = parser.parse_args()

    result = ValidationResult()
    entries = load_packs(args.source_dir, result)
    validate_global(entries, result, release=args.release)
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    selected = select_entries(
        entries,
        include_drafts=args.include_drafts,
        release=args.release,
    )
    canonical = canonical_json(selected).encode("utf-8")
    revision = "sha256:" + hashlib.sha256(canonical).hexdigest()
    rendered = render_module(
        selected,
        source_count=len(entries),
        revision=revision,
        include_drafts=args.include_drafts,
    )

    if args.check:
        if not args.output.exists():
            print(f"ERROR: generated file does not exist: {args.output}", file=sys.stderr)
            return 1
        current = args.output.read_text(encoding="utf-8")
        if current != rendered:
            print(
                f"ERROR: generated file is stale: {args.output}\n"
                "Run scripts/build_content.py with the same options.",
                file=sys.stderr,
            )
            return 1
        print(f"generated file is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"wrote {len(selected)} entries to {args.output}")
    print(f"revision: {revision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
