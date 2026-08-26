from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from gomoji import config

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FONT_FILE = PROJECT_ROOT / config.FONT_PATH


@dataclass
class AppState:
    frame: int = 0
    word_index: int = 0
    debug_enabled: bool = False

    @property
    def word(self) -> str:
        return config.PLACEHOLDER_WORDS[self.word_index]

    def next_word(self) -> None:
        self.word_index = (self.word_index + 1) % len(config.PLACEHOLDER_WORDS)


class GomojiApp:
    def __init__(self, headless: bool = False, smoke_frames: int | None = None) -> None:
        import pyxel

        self.pyxel = pyxel
        self.state = AppState()
        self.smoke_frames = smoke_frames
        self.font = None

        pyxel.init(
            config.SCREEN_WIDTH,
            config.SCREEN_HEIGHT,
            title=config.WINDOW_TITLE,
            fps=config.FPS,
            headless=headless,
        )
        if FONT_FILE.exists():
            self.font = pyxel.Font(str(FONT_FILE))
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
        if self.smoke_frames is not None and self.state.frame >= self.smoke_frames:
            pyxel.quit()

    def draw(self) -> None:
        pyxel = self.pyxel
        pyxel.cls(config.BACKGROUND_COLOR)

        center_x = config.SCREEN_WIDTH // 2
        word = self.state.word
        cursor_index = (self.state.frame // 18) % 5
        wave_index = (self.state.frame // 10) % 5

        pyxel.rectb(
            24,
            32,
            config.SCREEN_WIDTH - 48,
            config.SCREEN_HEIGHT - 64,
            config.SHADOW_COLOR,
        )
        self.draw_text(center_x - 18, 78, "ごもじ", config.TEXT_COLOR)
        self.draw_text(center_x - 36, 108, "五文字の仮画面", config.GRID_COLOR)

        slot_size = 58
        gap = 10
        total_width = slot_size * 5 + gap * 4
        start_x = center_x - total_width // 2
        top_y = 190

        for index, letter in enumerate(word):
            x = start_x + index * (slot_size + gap)
            y = top_y - 6 if index == wave_index else top_y
            color = config.ACTIVE_COLOR if index == cursor_index else config.GRID_COLOR
            fill = config.ACCENT_COLOR if index < 2 else config.BACKGROUND_COLOR

            pyxel.rect(x + 2, y + 2, slot_size, slot_size, config.SHADOW_COLOR)
            pyxel.rect(x, y, slot_size, slot_size, fill)
            pyxel.rectb(x, y, slot_size, slot_size, color)
            self.draw_text(
                x + 23,
                y + 22,
                letter,
                config.BACKGROUND_COLOR if index < 2 else color,
            )

            if index == cursor_index:
                pyxel.rect(x + 15, y + slot_size + 11, 28, 3, config.ACTIVE_COLOR)

        self.draw_text(center_x - 84, 332, "スペースで ことばを切替", config.TEXT_COLOR)
        self.draw_text(center_x - 66, 366, "iPhone 16 画面向け", config.LOCKED_COLOR)
        self.draw_text(center_x - 72, 420, "詳細仕様待ち", config.GRID_COLOR)

        if self.state.debug_enabled:
            pyxel.text(4, 4, f"frame={self.state.frame}", config.DEBUG_COLOR)
            pyxel.text(4, 12, f"word={self.state.word}", config.DEBUG_COLOR)

    def draw_text(self, x: int, y: int, text: str, color: int) -> None:
        self.pyxel.text(x, y, text, color, self.font)


def main() -> None:
    GomojiApp()
