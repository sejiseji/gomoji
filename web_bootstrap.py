# title: ごもじンゴ
# author: sejiseji
# desc: Pyxel project scaffold for Gomoji
# site: https://github.com/sejiseji/gomoji
# license: MIT
# version: 0.2.0

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto

WINDOW_TITLE = "ごもじンゴ"
SCREEN_WIDTH = 396
SCREEN_HEIGHT = 696
FPS = 30
FONT_PATH = "assets/umplus_j12r.bdf"

BACKGROUND_COLOR = 0
TEXT_COLOR = 7
ACCENT_COLOR = 10
SHADOW_COLOR = 1
DEBUG_COLOR = 13
GRID_COLOR = 5
ACTIVE_COLOR = 11
LOCKED_COLOR = 3

WORD_LENGTH = 5
KANA_GROUPS = {
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

ENTRIES = (
    {
        "id": "GMG0001",
        "word": "あめしらせ",
        "category": "現象",
        "rarity": 3,
        "paragraphs": (
            "雨が降る少し前に、なぜか洗濯物を外へ出したくなる現象。",
            "空模様を見た本人は「まだいける」と判断するが、その判断まで含めて発生条件とされる。",
            "なお、取り込んだ直後に晴れる場合も同じ現象へ含まれる。",
        ),
    },
    {
        "id": "GMG0012",
        "word": "ちょいずれ",
        "category": "現象",
        "rarity": 2,
        "paragraphs": (
            "時刻、位置、会話の意図などが、困らない程度に少しだけ食い違う現象。",
            "一つずつ直すと別の箇所がずれるため、最終的には全員が気づかないふりをする。",
            "大事故にはならないが、地味に一日を削ってくる。",
        ),
    },
    {
        "id": "GMG0023",
        "word": "すっぽぬけ",
        "category": "現象",
        "rarity": 5,
        "paragraphs": (
            "確実に覚えていたはずの情報だけが、必要な瞬間に抜け落ちる現象。",
            "人名、暗証番号、買う物の三種で特に起こりやすく、用事が終わると自然に戻る。",
            "記憶力の問題ではない。タイミングの性格が悪いだけである。",
        ),
    },
    {
        "id": "GMG0034",
        "word": "ぴゅうかぜ",
        "category": "現象",
        "rarity": 4,
        "paragraphs": (
            "窓を閉めた直後に限って、部屋へ入り込もうとする細い風。",
            "紙だけを選んで動かす性質があり、重い物には一切関心を示さない。",
            "換気には役立たないが、机の上の秩序は壊す。",
        ),
    },
    {
        "id": "GMG0501",
        "word": "ねこぱんち",
        "category": "技・動作",
        "rarity": 5,
        "paragraphs": (
            "猫が会話を打ち切る際に使用する、前脚による短い打撃。",
            "威力よりも使用者の態度に意味があり、防御しても関係は改善しない。",
            "なお、二発目から爪が出る場合がある。",
        ),
    },
)

BY_WORD = {entry["word"]: entry for entry in ENTRIES}
BY_ID = {entry["id"]: entry for entry in ENTRIES}


def all_kana():
    return tuple(kana for group in KANA_GROUPS.values() for kana in group)


def build_index():
    next_chars = defaultdict(set)
    entry_ids = defaultdict(list)
    for entry in ENTRIES:
        for index, next_char in enumerate(entry["word"]):
            prefix = entry["word"][:index]
            next_chars[prefix].add(next_char)
            entry_ids[prefix].append(entry["id"])
        entry_ids[entry["word"]].append(entry["id"])

    ordered_next = {
        prefix: tuple(kana for kana in all_kana() if kana in chars)
        for prefix, chars in next_chars.items()
    }
    return ordered_next, {prefix: tuple(ids) for prefix, ids in entry_ids.items()}


NEXT_CHARS_BY_PREFIX, ENTRY_IDS_BY_PREFIX = build_index()


class ScreenState(Enum):
    INPUT = auto()
    RESULT = auto()


class InputLayer(Enum):
    ROWS = auto()
    CHARACTERS = auto()


@dataclass
class Button:
    x: int
    y: int
    width: int
    height: int
    label: str
    action: str
    value: str | int | None = None
    enabled: bool = True


@dataclass
class WebState:
    screen: ScreenState = ScreenState.INPUT
    input_layer: InputLayer = InputLayer.ROWS
    slots: list[str | None] = field(default_factory=lambda: [None] * WORD_LENGTH)
    cursor_index: int = 0
    selected_group: str | None = None
    focused_button: int = 0
    result_entry_id: str | None = None

    @property
    def word(self):
        return "".join(slot or "" for slot in self.slots)

    @property
    def result_entry(self):
        if self.result_entry_id is None:
            return None
        return BY_ID.get(self.result_entry_id)

    def prefix_for_cursor(self):
        return "".join(slot or "" for slot in self.slots[: self.cursor_index])

    def filled_prefix(self):
        letters = []
        for slot in self.slots:
            if slot is None:
                break
            letters.append(slot)
        return "".join(letters)

    def valid_next_chars(self):
        return NEXT_CHARS_BY_PREFIX.get(self.prefix_for_cursor(), ())

    def enabled_groups(self):
        valid = set(self.valid_next_chars())
        return tuple(
            group_id
            for group_id, chars in KANA_GROUPS.items()
            if any(kana in valid for kana in chars)
        )

    def enabled_kana(self):
        if self.selected_group is None:
            return ()
        valid = set(self.valid_next_chars())
        return tuple(kana for kana in KANA_GROUPS[self.selected_group] if kana in valid)

    def can_confirm(self):
        return len(self.word) == WORD_LENGTH and self.word in BY_WORD

    def select_slot(self, index):
        self.cursor_index = max(0, min(WORD_LENGTH - 1, index))
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.focused_button = 0

    def open_kana_group(self, group_id):
        if group_id not in self.enabled_groups():
            return
        self.selected_group = group_id
        self.input_layer = InputLayer.CHARACTERS
        self.focused_button = 0

    def select_kana(self, kana):
        if kana not in self.enabled_kana():
            return
        self.slots[self.cursor_index] = kana
        for index in range(self.cursor_index + 1, WORD_LENGTH):
            self.slots[index] = None
        if self.cursor_index < WORD_LENGTH - 1:
            self.cursor_index += 1
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.focused_button = 0

    def delete_character(self):
        if self.slots[self.cursor_index] is not None:
            for index in range(self.cursor_index, WORD_LENGTH):
                self.slots[index] = None
        elif self.cursor_index > 0:
            self.cursor_index -= 1
            for index in range(self.cursor_index, WORD_LENGTH):
                self.slots[index] = None
        self.input_layer = InputLayer.ROWS
        self.selected_group = None

    def clear_word(self):
        self.slots = [None] * WORD_LENGTH
        self.cursor_index = 0
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.result_entry_id = None

    def autofill_word(self):
        candidate_ids = list(ENTRY_IDS_BY_PREFIX.get(self.filled_prefix(), ()))
        if not candidate_ids:
            return
        entry = BY_ID[random.choice(candidate_ids)]
        self.slots = list(entry["word"])
        self.cursor_index = WORD_LENGTH - 1
        self.input_layer = InputLayer.ROWS
        self.selected_group = None

    def confirm_word(self):
        if not self.can_confirm():
            return
        self.result_entry_id = BY_WORD[self.word]["id"]
        self.screen = ScreenState.RESULT
        self.input_layer = InputLayer.ROWS
        self.selected_group = None

    def return_to_input(self, clear):
        self.screen = ScreenState.INPUT
        self.result_entry_id = None
        if clear:
            self.clear_word()
        else:
            self.input_layer = InputLayer.ROWS
            self.selected_group = None


class GomojiWebApp:
    def __init__(self):
        import pyxel

        self.pyxel = pyxel
        self.state = WebState()
        self.buttons = []
        self.font = None
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=WINDOW_TITLE, fps=FPS)
        self.font = pyxel.Font(FONT_PATH)
        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel = self.pyxel
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            if self.state.input_layer == InputLayer.CHARACTERS:
                self.state.input_layer = InputLayer.ROWS
                self.state.selected_group = None
            return
        if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.state.delete_character()
        if pyxel.btnp(pyxel.KEY_C):
            self.state.clear_word()
        if pyxel.btnp(pyxel.KEY_R):
            self.state.autofill_word()
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN):
            self.activate_focused_button()

        mouse_button = getattr(pyxel, "MOUSE_BUTTON_LEFT", 0)
        if pyxel.btnp(mouse_button):
            self.activate_button_at(pyxel.mouse_x, pyxel.mouse_y)

    def draw(self):
        self.pyxel.cls(BACKGROUND_COLOR)
        self.buttons = []
        if self.state.screen == ScreenState.RESULT:
            self.draw_result()
        else:
            self.draw_input()

    def draw_input(self):
        pyxel = self.pyxel
        center_x = SCREEN_WIDTH // 2
        pyxel.rectb(16, 18, SCREEN_WIDTH - 32, SCREEN_HEIGHT - 44, SHADOW_COLOR)
        self.draw_text_centered(center_x, 28, "ごもじンゴ", TEXT_COLOR)
        self.draw_text_centered(center_x, 62, "5文字をえらぶ", GRID_COLOR)

        slot_size = 58
        gap = 10
        start_x = center_x - (slot_size * 5 + gap * 4) // 2
        top_y = 106
        for index, letter in enumerate(self.state.slots):
            x = start_x + index * (slot_size + gap)
            y = top_y
            color = ACTIVE_COLOR if index == self.state.cursor_index else GRID_COLOR
            fill = ACCENT_COLOR if letter is not None else BACKGROUND_COLOR
            pyxel.rect(x + 2, y + 2, slot_size, slot_size, SHADOW_COLOR)
            pyxel.rect(x, y, slot_size, slot_size, fill)
            pyxel.rectb(x, y, slot_size, slot_size, color)
            self.draw_text_centered(
                x + slot_size // 2,
                y + 21,
                letter or "・",
                BACKGROUND_COLOR if letter is not None else LOCKED_COLOR,
            )
            self.buttons.append(
                Button(x - 2, y - 2, slot_size + 4, slot_size + 4, "", "slot", index)
            )
            if index == self.state.cursor_index:
                pyxel.rect(x + 15, y + slot_size + 11, 28, 3, ACTIVE_COLOR)

        pyxel.line(24, 196, SCREEN_WIDTH - 24, 196, GRID_COLOR)
        guide = "行をえらぶ"
        if self.state.input_layer == InputLayer.CHARACTERS:
            guide = f"{self.state.selected_group}行からえらぶ"
        self.draw_text_centered(center_x, 220, guide, TEXT_COLOR)

        if self.state.input_layer == InputLayer.ROWS:
            self.draw_row_panel(252)
        else:
            self.draw_kana_panel(252)
        self.draw_actions()

    def draw_row_panel(self, top_y):
        enabled = set(self.state.enabled_groups())
        for index, group_id in enumerate(tuple(KANA_GROUPS)):
            row = index // 5
            col = index % 5
            self.draw_button(
                Button(
                    22 + col * 72,
                    top_y + row * 60,
                    64,
                    52,
                    group_id,
                    "row",
                    group_id,
                    group_id in enabled,
                )
            )

    def draw_kana_panel(self, top_y):
        if self.state.selected_group is None:
            return
        enabled = set(self.state.enabled_kana())
        for index, kana in enumerate(KANA_GROUPS[self.state.selected_group]):
            row = index // 5
            col = index % 5
            self.draw_button(
                Button(
                    22 + col * 72,
                    top_y + row * 56,
                    64,
                    48,
                    kana,
                    "kana",
                    kana,
                    kana in enabled,
                )
            )

    def draw_actions(self):
        y = 580
        self.draw_button(Button(22, y, 70, 46, "けす", "delete"))
        self.draw_button(Button(100, y, 94, 46, "ぜんぶけす", "clear"))
        self.draw_button(Button(202, y, 82, 46, "おまかせ", "auto"))
        self.draw_button(
            Button(292, y, 82, 46, "しらべる", "confirm", enabled=self.state.can_confirm())
        )
        self.draw_text_centered(SCREEN_WIDTH // 2, 648, "Z/Enter けってい  X もどる", LOCKED_COLOR)

    def draw_result(self):
        pyxel = self.pyxel
        entry = self.state.result_entry
        if entry is None:
            self.state.return_to_input(True)
            return
        center_x = SCREEN_WIDTH // 2
        pyxel.rectb(16, 18, SCREEN_WIDTH - 32, SCREEN_HEIGHT - 44, SHADOW_COLOR)
        self.draw_text_centered(center_x, 28, "ごもじンゴ", TEXT_COLOR)
        self.draw_text_centered(center_x, 88, " ".join(entry["word"]), ACCENT_COLOR)
        pyxel.line(24, 174, SCREEN_WIDTH - 24, 174, GRID_COLOR)
        self.draw_text_centered(center_x, 204, f"【{entry['word']}】", TEXT_COLOR)
        self.draw_text_centered(
            center_x,
            242,
            f"{entry['category']} / R{entry['rarity']}",
            ACTIVE_COLOR,
        )

        y = 282
        for paragraph in entry["paragraphs"]:
            for line in self.wrap_text(paragraph, 19):
                self.draw_text(34, y, line, TEXT_COLOR)
                y += 19
            y += 10
        self.draw_button(Button(58, 586, 126, 48, "もういちど", "again"))
        self.draw_button(Button(212, 586, 126, 48, "べつのことば", "new"))
        self.draw_text_centered(center_x, 650, f"{entry['id']} / {len(ENTRIES)}語", LOCKED_COLOR)

    def draw_button(self, button):
        pyxel = self.pyxel
        self.buttons.append(button)
        focused = False
        if button.enabled and button.label:
            buttons = self.focusable_buttons()
            focused = buttons.index(button) == self.focus_index()
        fill = SHADOW_COLOR if button.enabled else BACKGROUND_COLOR
        border = ACTIVE_COLOR if focused else GRID_COLOR
        text_color = TEXT_COLOR if button.enabled else LOCKED_COLOR
        pyxel.rect(button.x + 2, button.y + 2, button.width, button.height, SHADOW_COLOR)
        pyxel.rect(button.x, button.y, button.width, button.height, fill)
        pyxel.rectb(button.x, button.y, button.width, button.height, border)
        self.draw_text_centered(
            button.x + button.width // 2,
            button.y + button.height // 2 - 6,
            button.label,
            text_color,
        )

    def focusable_buttons(self):
        return [button for button in self.buttons if button.enabled and button.label]

    def focus_index(self):
        buttons = self.focusable_buttons()
        if not buttons:
            self.state.focused_button = 0
            return 0
        self.state.focused_button %= len(buttons)
        return self.state.focused_button

    def activate_focused_button(self):
        buttons = self.focusable_buttons()
        if buttons:
            self.run_button_action(buttons[self.focus_index()])

    def activate_button_at(self, x, y):
        for button in reversed(self.buttons):
            if (
                button.enabled
                and button.x <= x < button.x + button.width
                and button.y <= y < button.y + button.height
            ):
                self.run_button_action(button)
                return

    def run_button_action(self, button):
        if button.action == "slot":
            self.state.select_slot(button.value)
        elif button.action == "row":
            self.state.open_kana_group(button.value)
        elif button.action == "kana":
            self.state.select_kana(button.value)
        elif button.action == "delete":
            self.state.delete_character()
        elif button.action == "clear":
            self.state.clear_word()
        elif button.action == "auto":
            self.state.autofill_word()
        elif button.action == "confirm":
            self.state.confirm_word()
        elif button.action == "again":
            self.state.return_to_input(False)
        elif button.action == "new":
            self.state.return_to_input(True)

    def wrap_text(self, text, max_chars):
        return [text[index : index + max_chars] for index in range(0, len(text), max_chars)]

    def draw_text_centered(self, center_x, y, text, color):
        self.draw_text(center_x - self.text_width(text) // 2, y, text, color)

    def text_width(self, text):
        return sum(12 if ord(char) > 127 else 6 for char in text)

    def draw_text(self, x, y, text, color):
        self.pyxel.text(x, y, text, color, self.font)


GomojiWebApp()
