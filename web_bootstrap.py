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

PLACEHOLDER_MOTIFS = ("GO", "MO", "JI")


@dataclass
class AppState:
    frame: int = 0
    motif_index: int = 0
    debug_enabled: bool = False

    @property
    def motif(self) -> str:
        return PLACEHOLDER_MOTIFS[self.motif_index]

    def next_motif(self) -> None:
        self.motif_index = (self.motif_index + 1) % len(PLACEHOLDER_MOTIFS)


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
            self.state.next_motif()

        if pyxel.btnp(pyxel.KEY_D):
            self.state.debug_enabled = not self.state.debug_enabled

        self.state.frame += 1

    def draw(self) -> None:
        pyxel = self.pyxel
        pyxel.cls(BACKGROUND_COLOR)

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        pulse = (self.state.frame // 12) % 2

        pyxel.rectb(24, 24, SCREEN_WIDTH - 48, SCREEN_HEIGHT - 48, SHADOW_COLOR)
        pyxel.circ(center_x - 34, center_y - 12, 18 + pulse, ACCENT_COLOR)
        pyxel.circ(center_x + 34, center_y - 12, 18 + pulse, ACCENT_COLOR)
        pyxel.rect(center_x - 42, center_y + 16, 84, 18, SHADOW_COLOR)

        title = "GOMOJI"
        motif = self.state.motif
        pyxel.text(center_x - len(title) * 2, 42, title, TEXT_COLOR)
        pyxel.text(center_x - len(motif) * 2, center_y - 16, motif, BACKGROUND_COLOR)
        pyxel.text(center_x - 43, center_y + 22, "SPEC READY SLOT", TEXT_COLOR)

        if self.state.debug_enabled:
            pyxel.text(4, 4, f"frame={self.state.frame}", DEBUG_COLOR)
            pyxel.text(4, 12, f"motif={motif}", DEBUG_COLOR)


GomojiWebApp()
