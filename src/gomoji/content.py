from __future__ import annotations

from gomoji.generated.content_data import (
    BY_ID,
    BY_WORD,
    CONTENT_COUNT,
    CONTENT_INCLUDES_DRAFTS,
    CONTENT_REVISION,
    CONTENT_SCHEMA_VERSION,
    CONTENT_SOURCE_COUNT,
    ENTRIES,
    ContentEntry,
)

__all__ = [
    "BY_ID",
    "BY_WORD",
    "CONTENT_COUNT",
    "CONTENT_INCLUDES_DRAFTS",
    "CONTENT_REVISION",
    "CONTENT_SCHEMA_VERSION",
    "CONTENT_SOURCE_COUNT",
    "ContentEntry",
    "RUNTIME_ENTRIES",
    "RUNTIME_WORDS",
    "entry_at",
    "format_result_heading",
    "format_slot_text",
]


RUNTIME_ENTRIES: tuple[ContentEntry, ...] = ENTRIES
RUNTIME_WORDS: tuple[str, ...] = tuple(entry.word for entry in RUNTIME_ENTRIES)


def entry_at(index: int) -> ContentEntry:
    return RUNTIME_ENTRIES[index % len(RUNTIME_ENTRIES)]


def format_slot_text(word: str) -> str:
    return " ".join(word)


def format_result_heading(word: str) -> str:
    return f"【{word}】"
