# title: ごもじンゴ
# author: sejiseji
# desc: Pyxel project scaffold for Gomoji
# site: https://github.com/sejiseji/gomoji
# license: MIT
# version: 0.1.0

from __future__ import annotations

from dataclasses import dataclass

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

PLACEHOLDER_WORDS = ("あめしらせ", "ちょいずれ", "すっぽぬけ", "ぴゅうかぜ")


@dataclass
class AppState:
    frame: int = 0
    word_index: int = 0
    debug_enabled: bool = False

    @property
    def word(self) -> str:
        return PLACEHOLDER_WORDS[self.word_index]

    def next_word(self) -> None:
        self.word_index = (self.word_index + 1) % len(PLACEHOLDER_WORDS)


class GomojiWebApp:
    def __init__(self) -> None:
        import pyxel

        self.pyxel = pyxel
        self.state = AppState()
        self.font = None
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=WINDOW_TITLE, fps=FPS)
        self.font = pyxel.Font(FONT_PATH)
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        pyxel = self.pyxel

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
            return

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state.next_word()

        if pyxel.btnp(pyxel.KEY_D):
            self.state.debug_enabled = not self.state.debug_enabled

        self.state.frame += 1

    def draw(self) -> None:
        pyxel = self.pyxel
        pyxel.cls(BACKGROUND_COLOR)

        center_x = SCREEN_WIDTH // 2
        word = self.state.word
        cursor_index = (self.state.frame // 18) % 5
        wave_index = (self.state.frame // 10) % 5

        pyxel.rectb(24, 32, SCREEN_WIDTH - 48, SCREEN_HEIGHT - 64, SHADOW_COLOR)
        self.draw_text(center_x - 30, 78, "ごもじンゴ", TEXT_COLOR)
        self.draw_text(center_x - 36, 108, "五文字の仮画面", GRID_COLOR)

        slot_size = 58
        gap = 10
        total_width = slot_size * 5 + gap * 4
        start_x = center_x - total_width // 2
        top_y = 190

        for index, letter in enumerate(word):
            x = start_x + index * (slot_size + gap)
            y = top_y - 6 if index == wave_index else top_y
            color = ACTIVE_COLOR if index == cursor_index else GRID_COLOR
            fill = ACCENT_COLOR if index < 2 else BACKGROUND_COLOR

            pyxel.rect(x + 2, y + 2, slot_size, slot_size, SHADOW_COLOR)
            pyxel.rect(x, y, slot_size, slot_size, fill)
            pyxel.rectb(x, y, slot_size, slot_size, color)
            self.draw_text(x + 23, y + 22, letter, BACKGROUND_COLOR if index < 2 else color)

            if index == cursor_index:
                pyxel.rect(x + 15, y + slot_size + 11, 28, 3, ACTIVE_COLOR)

        self.draw_text(center_x - 84, 332, "スペースで ことばを切替", TEXT_COLOR)
        self.draw_text(center_x - 66, 366, "iPhone 16 画面向け", LOCKED_COLOR)
        self.draw_text(center_x - 72, 420, "詳細仕様待ち", GRID_COLOR)

        if self.state.debug_enabled:
            pyxel.text(4, 4, f"frame={self.state.frame}", DEBUG_COLOR)
            pyxel.text(4, 12, f"word={self.state.word}", DEBUG_COLOR)

    def draw_text(self, x: int, y: int, text: str, color: int) -> None:
        self.pyxel.text(x, y, text, color, self.font)


GomojiWebApp()
