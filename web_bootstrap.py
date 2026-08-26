# title: Gomoji
# author: sejiseji
# desc: Pyxel project scaffold for Gomoji
# site: https://github.com/sejiseji/gomoji
# license: MIT
# version: 0.1.0

from __future__ import annotations

from dataclasses import dataclass

WINDOW_TITLE = "Gomoji"
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192
FPS = 30

BACKGROUND_COLOR = 0
TEXT_COLOR = 7
ACCENT_COLOR = 10
SHADOW_COLOR = 1
DEBUG_COLOR = 13
GRID_COLOR = 5
ACTIVE_COLOR = 11
LOCKED_COLOR = 3

PLACEHOLDER_WORDS = ("GOMJI", "KOTBA", "PYXEL", "MOJIQ")


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
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=WINDOW_TITLE, fps=FPS)
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
        cursor_index = (self.state.frame // 18) % 5
        wave_index = (self.state.frame // 10) % 5

        pyxel.rectb(18, 18, SCREEN_WIDTH - 36, SCREEN_HEIGHT - 36, SHADOW_COLOR)
        pyxel.text(center_x - 12, 34, "GOMOJI", TEXT_COLOR)
        pyxel.text(center_x - 38, 48, "5 LETTER PUZZLE BASE", GRID_COLOR)

        slot_size = 28
        gap = 6
        total_width = slot_size * 5 + gap * 4
        start_x = center_x - total_width // 2
        top_y = 74

        for index, letter in enumerate(self.state.word):
            x = start_x + index * (slot_size + gap)
            y = top_y - 2 if index == wave_index else top_y
            color = ACTIVE_COLOR if index == cursor_index else GRID_COLOR
            fill = ACCENT_COLOR if index < 2 else BACKGROUND_COLOR

            pyxel.rect(x + 2, y + 2, slot_size, slot_size, SHADOW_COLOR)
            pyxel.rect(x, y, slot_size, slot_size, fill)
            pyxel.rectb(x, y, slot_size, slot_size, color)
            pyxel.text(x + 12, y + 11, letter, BACKGROUND_COLOR if index < 2 else color)

            if index == cursor_index:
                pyxel.rect(x + 8, y + slot_size + 5, 12, 2, ACTIVE_COLOR)

        pyxel.text(center_x - 47, 126, "SPACE: CHANGE WORD", TEXT_COLOR)
        pyxel.text(center_x - 35, 138, "SPEC SLOT OPEN", LOCKED_COLOR)

        if self.state.debug_enabled:
            pyxel.text(4, 4, f"frame={self.state.frame}", DEBUG_COLOR)
            pyxel.text(4, 12, f"word={self.state.word}", DEBUG_COLOR)


GomojiWebApp()
