from __future__ import annotations

from dataclasses import dataclass

from gomoji import config


@dataclass
class AppState:
    frame: int = 0
    motif_index: int = 0
    debug_enabled: bool = False

    @property
    def motif(self) -> str:
        return config.PLACEHOLDER_MOTIFS[self.motif_index]

    def next_motif(self) -> None:
        self.motif_index = (self.motif_index + 1) % len(config.PLACEHOLDER_MOTIFS)


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
            self.state.next_motif()

        if pyxel.btnp(pyxel.KEY_D):
            self.state.debug_enabled = not self.state.debug_enabled

        self.state.frame += 1
        if self.smoke_frames is not None and self.state.frame >= self.smoke_frames:
            pyxel.quit()

    def draw(self) -> None:
        pyxel = self.pyxel
        pyxel.cls(config.BACKGROUND_COLOR)

        center_x = config.SCREEN_WIDTH // 2
        center_y = config.SCREEN_HEIGHT // 2
        pulse = (self.state.frame // 12) % 2

        pyxel.rectb(
            24,
            24,
            config.SCREEN_WIDTH - 48,
            config.SCREEN_HEIGHT - 48,
            config.SHADOW_COLOR,
        )
        pyxel.circ(center_x - 34, center_y - 12, 18 + pulse, config.ACCENT_COLOR)
        pyxel.circ(center_x + 34, center_y - 12, 18 + pulse, config.ACCENT_COLOR)
        pyxel.rect(center_x - 42, center_y + 16, 84, 18, config.SHADOW_COLOR)

        title = "GOMOJI"
        motif = self.state.motif
        pyxel.text(center_x - len(title) * 2, 42, title, config.TEXT_COLOR)
        pyxel.text(center_x - len(motif) * 2, center_y - 16, motif, config.BACKGROUND_COLOR)
        pyxel.text(center_x - 43, center_y + 22, "SPEC READY SLOT", config.TEXT_COLOR)

        if self.state.debug_enabled:
            pyxel.text(4, 4, f"frame={self.state.frame}", config.DEBUG_COLOR)
            pyxel.text(4, 12, f"motif={motif}", config.DEBUG_COLOR)


def main() -> None:
    GomojiApp()
