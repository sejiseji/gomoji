from __future__ import annotations

from dataclasses import dataclass

from gomoji import config


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

        pyxel.init(
            config.SCREEN_WIDTH,
            config.SCREEN_HEIGHT,
            title=config.WINDOW_TITLE,
            fps=config.FPS,
            headless=headless,
        )
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
        cursor_index = (self.state.frame // 18) % 5
        wave_index = (self.state.frame // 10) % 5

        pyxel.rectb(
            18,
            18,
            config.SCREEN_WIDTH - 36,
            config.SCREEN_HEIGHT - 36,
            config.SHADOW_COLOR,
        )
        pyxel.text(center_x - 12, 34, "GOMOJI", config.TEXT_COLOR)
        pyxel.text(center_x - 38, 48, "5 LETTER PUZZLE BASE", config.GRID_COLOR)

        slot_size = 28
        gap = 6
        total_width = slot_size * 5 + gap * 4
        start_x = center_x - total_width // 2
        top_y = 74

        for index, letter in enumerate(self.state.word):
            x = start_x + index * (slot_size + gap)
            y = top_y - 2 if index == wave_index else top_y
            color = config.ACTIVE_COLOR if index == cursor_index else config.GRID_COLOR
            fill = config.ACCENT_COLOR if index < 2 else config.BACKGROUND_COLOR

            pyxel.rect(x + 2, y + 2, slot_size, slot_size, config.SHADOW_COLOR)
            pyxel.rect(x, y, slot_size, slot_size, fill)
            pyxel.rectb(x, y, slot_size, slot_size, color)
            pyxel.text(x + 12, y + 11, letter, config.BACKGROUND_COLOR if index < 2 else color)

            if index == cursor_index:
                pyxel.rect(x + 8, y + slot_size + 5, 12, 2, config.ACTIVE_COLOR)

        pyxel.text(center_x - 47, 126, "SPACE: CHANGE WORD", config.TEXT_COLOR)
        pyxel.text(center_x - 35, 138, "SPEC SLOT OPEN", config.LOCKED_COLOR)

        if self.state.debug_enabled:
            pyxel.text(4, 4, f"frame={self.state.frame}", config.DEBUG_COLOR)
            pyxel.text(4, 12, f"word={self.state.word}", config.DEBUG_COLOR)


def main() -> None:
    GomojiApp()
