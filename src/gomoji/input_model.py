from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto

from gomoji import content

WORD_LENGTH = 5
DEFAULT_REVEAL_FRAMES = 12

KANA_GROUPS: dict[str, tuple[str, ...]] = {
    "あ": ("あ", "い", "う", "え", "お", "ぁ", "ぃ", "ぅ", "ぇ", "ぉ"),
    "か": ("か", "き", "く", "け", "こ", "が", "ぎ", "ぐ", "げ", "ご"),
    "さ": ("さ", "し", "す", "せ", "そ", "ざ", "じ", "ず", "ぜ", "ぞ"),
    "た": ("た", "ち", "つ", "て", "と", "だ", "ぢ", "づ", "で", "ど", "っ"),
    "な": ("な", "に", "ぬ", "ね", "の"),
    "は": (
        "は",
        "ひ",
        "ふ",
        "へ",
        "ほ",
        "ば",
        "び",
        "ぶ",
        "べ",
        "ぼ",
        "ぱ",
        "ぴ",
        "ぷ",
        "ぺ",
        "ぽ",
    ),
    "ま": ("ま", "み", "む", "め", "も"),
    "や": ("や", "ゆ", "よ", "ゃ", "ゅ", "ょ"),
    "ら": ("ら", "り", "る", "れ", "ろ"),
    "わ": ("わ", "を", "ん", "ゎ", "ゔ"),
}


class ScreenState(Enum):
    INPUT = auto()
    REVEAL = auto()
    RESULT = auto()


class InputLayer(Enum):
    ROWS = auto()
    CHARACTERS = auto()


@dataclass(frozen=True)
class ContentIndex:
    next_chars_by_prefix: dict[str, tuple[str, ...]]
    entry_ids_by_prefix: dict[str, tuple[str, ...]]

    @classmethod
    def build(cls, entries: tuple[content.ContentEntry, ...]) -> ContentIndex:
        next_chars: dict[str, set[str]] = defaultdict(set)
        entry_ids: dict[str, list[str]] = defaultdict(list)

        for entry in entries:
            for index, next_char in enumerate(entry.word):
                prefix = entry.word[:index]
                next_chars[prefix].add(next_char)
                entry_ids[prefix].append(entry.id)
            entry_ids[entry.word].append(entry.id)

        ordered_next_chars = {
            prefix: tuple(kana for kana in all_kana() if kana in chars)
            for prefix, chars in next_chars.items()
        }
        ordered_entry_ids = {prefix: tuple(ids) for prefix, ids in entry_ids.items()}
        return cls(ordered_next_chars, ordered_entry_ids)

    def next_chars(self, prefix: str) -> tuple[str, ...]:
        return self.next_chars_by_prefix.get(prefix, ())

    def entry_ids(self, prefix: str) -> tuple[str, ...]:
        return self.entry_ids_by_prefix.get(prefix, ())


def all_kana() -> tuple[str, ...]:
    return tuple(kana for group in KANA_GROUPS.values() for kana in group)


def build_content_index() -> ContentIndex:
    return ContentIndex.build(content.RUNTIME_ENTRIES)


@dataclass
class InputState:
    index: ContentIndex = field(default_factory=build_content_index)
    screen: ScreenState = ScreenState.INPUT
    input_layer: InputLayer = InputLayer.ROWS
    slots: list[str | None] = field(default_factory=lambda: [None] * WORD_LENGTH)
    cursor_index: int = 0
    selected_group: str | None = None
    focused_button: int = 0
    result_entry_id: str | None = None
    pending_result_entry_id: str | None = None
    result_is_new: bool = False
    reveal_frames_remaining: int = 0
    discovered_entry_ids: set[str] = field(default_factory=set)
    recent_entry_ids: list[str] = field(default_factory=list)
    rng: random.Random = field(default_factory=random.Random, repr=False)

    @property
    def word(self) -> str:
        return "".join(slot or "" for slot in self.slots)

    @property
    def result_entry(self) -> content.ContentEntry | None:
        if self.result_entry_id is None:
            return None
        return content.BY_ID.get(self.result_entry_id)

    @property
    def found_count(self) -> int:
        return len(self.discovered_entry_ids)

    def prefix_for_cursor(self) -> str:
        return "".join(slot or "" for slot in self.slots[: self.cursor_index])

    def filled_prefix(self) -> str:
        letters = []
        for slot in self.slots:
            if slot is None:
                break
            letters.append(slot)
        return "".join(letters)

    def valid_next_chars(self) -> tuple[str, ...]:
        return self.index.next_chars(self.prefix_for_cursor())

    def enabled_groups(self) -> tuple[str, ...]:
        valid = set(self.valid_next_chars())
        return tuple(
            group_id
            for group_id, chars in KANA_GROUPS.items()
            if any(kana in valid for kana in chars)
        )

    def enabled_kana(self) -> tuple[str, ...]:
        if self.selected_group is None:
            return ()
        valid = set(self.valid_next_chars())
        return tuple(kana for kana in KANA_GROUPS[self.selected_group] if kana in valid)

    def can_confirm(self) -> bool:
        return len(self.word) == WORD_LENGTH and self.word in content.BY_WORD

    def select_slot(self, index: int) -> None:
        self.cursor_index = max(0, min(WORD_LENGTH - 1, index))
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.focused_button = 0

    def open_kana_group(self, group_id: str) -> bool:
        if group_id not in self.enabled_groups():
            return False
        self.selected_group = group_id
        self.input_layer = InputLayer.CHARACTERS
        self.focused_button = 0
        return True

    def select_kana(self, kana: str) -> bool:
        if kana not in self.enabled_kana():
            return False

        self.slots[self.cursor_index] = kana
        for index in range(self.cursor_index + 1, WORD_LENGTH):
            self.slots[index] = None

        if self.cursor_index < WORD_LENGTH - 1:
            self.cursor_index += 1

        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.focused_button = 0
        return True

    def delete_character(self) -> None:
        if self.slots[self.cursor_index] is not None:
            for index in range(self.cursor_index, WORD_LENGTH):
                self.slots[index] = None
        elif self.cursor_index > 0:
            self.cursor_index -= 1
            for index in range(self.cursor_index, WORD_LENGTH):
                self.slots[index] = None

        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.focused_button = 0

    def clear_word(self) -> None:
        self.slots = [None] * WORD_LENGTH
        self.cursor_index = 0
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.result_entry_id = None
        self.pending_result_entry_id = None
        self.focused_button = 0

    def autofill_word(self) -> None:
        prefix = self.filled_prefix()
        candidate_ids = list(self.index.entry_ids(prefix))
        if not candidate_ids:
            return

        preferred_ids = [
            entry_id for entry_id in candidate_ids if entry_id not in self.recent_entry_ids
        ]
        chosen_id = self.rng.choice(preferred_ids or candidate_ids)
        entry = content.BY_ID[chosen_id]
        self.slots = list(entry.word)
        self.cursor_index = WORD_LENGTH - 1
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.focused_button = 0

    def confirm_word(self) -> bool:
        if not self.can_confirm():
            return False

        entry = content.BY_WORD[self.word]
        self.pending_result_entry_id = entry.id
        self.result_entry_id = None
        self.result_is_new = entry.id not in self.discovered_entry_ids
        self.screen = ScreenState.REVEAL
        self.reveal_frames_remaining = DEFAULT_REVEAL_FRAMES
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.focused_button = 0
        self.recent_entry_ids.append(entry.id)
        del self.recent_entry_ids[:-5]
        return True

    def tick_reveal(self) -> None:
        if self.screen != ScreenState.REVEAL:
            return
        if self.reveal_frames_remaining > 0:
            self.reveal_frames_remaining -= 1
        if self.reveal_frames_remaining <= 0:
            self.finish_reveal()

    def finish_reveal(self) -> None:
        if self.pending_result_entry_id is None:
            self.return_to_input(clear=True)
            return
        self.result_entry_id = self.pending_result_entry_id
        self.pending_result_entry_id = None
        self.discovered_entry_ids.add(self.result_entry_id)
        self.screen = ScreenState.RESULT
        self.focused_button = 0

    def return_to_input(self, *, clear: bool) -> None:
        self.screen = ScreenState.INPUT
        self.result_entry_id = None
        self.pending_result_entry_id = None
        self.reveal_frames_remaining = 0
        if clear:
            self.clear_word()
        else:
            self.input_layer = InputLayer.ROWS
            self.selected_group = None
            self.focused_button = 0
