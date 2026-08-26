from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from gomoji import config, content
from gomoji.input_model import KANA_GROUPS, InputLayer, InputState, ScreenState

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FONT_FILE = PROJECT_ROOT / config.FONT_PATH

CATEGORY_LABELS = {
    "phenomenon": "現象",
    "condition": "状態・感情",
    "creature": "生物",
    "food": "食べ物",
    "technique": "技・動作",
    "tool": "道具",
    "custom": "習慣・制度",
    "place": "場所",
    "internet": "インターネット",
    "mystery": "怪異",
}


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


class GomojiApp:
    def __init__(self, headless: bool = False, smoke_frames: int | None = None) -> None:
        import pyxel

        self.pyxel = pyxel
        self.state = InputState()
        self.frame = 0
        self.debug_enabled = False
        self.buttons: list[Button] = []
        self.press_feedback_frames = 0
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
            if self.state.input_layer == InputLayer.CHARACTERS:
                self.state.input_layer = InputLayer.ROWS
                self.state.selected_group = None
            else:
                pyxel.quit()
            return

        if pyxel.btnp(pyxel.KEY_D):
            self.debug_enabled = not self.debug_enabled

        if pyxel.btnp(pyxel.KEY_LEFT):
            self.move_focus(-1)
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.move_focus(1)
        if pyxel.btnp(pyxel.KEY_UP):
            self.move_focus(-5)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.move_focus(5)
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN):
            self.activate_focused_button()
        if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_BACKSPACE):
            if self.state.input_layer == InputLayer.CHARACTERS:
                self.state.input_layer = InputLayer.ROWS
                self.state.selected_group = None
            else:
                self.state.delete_character()
        if pyxel.btnp(pyxel.KEY_C):
            self.state.clear_word()
        if pyxel.btnp(pyxel.KEY_R):
            self.state.autofill_word()

        mouse_button = getattr(pyxel, "MOUSE_BUTTON_LEFT", 0)
        if pyxel.btnp(mouse_button):
            self.activate_button_at(pyxel.mouse_x, pyxel.mouse_y)

        self.frame += 1
        if self.press_feedback_frames > 0:
            self.press_feedback_frames -= 1
        if self.smoke_frames is not None and self.frame >= self.smoke_frames:
            pyxel.quit()

    def draw(self) -> None:
        pyxel = self.pyxel
        pyxel.cls(config.BACKGROUND_COLOR)
        self.buttons = []

        if self.state.screen == ScreenState.RESULT:
            self.draw_result()
        else:
            self.draw_input()

        if self.debug_enabled:
            pyxel.text(4, 4, f"frame={self.frame}", config.DEBUG_COLOR)
            pyxel.text(4, 12, f"word={self.state.word}", config.DEBUG_COLOR)
            pyxel.text(4, 20, f"content={content.CONTENT_COUNT}", config.DEBUG_COLOR)
            pyxel.text(4, 28, f"screen={self.state.screen.name}", config.DEBUG_COLOR)

    def draw_input(self) -> None:
        pyxel = self.pyxel

        center_x = config.SCREEN_WIDTH // 2
        pyxel.rectb(
            16,
            18,
            config.SCREEN_WIDTH - 32,
            config.SCREEN_HEIGHT - 44,
            config.SHADOW_COLOR,
        )
        self.draw_text_centered(center_x, 28, "ごもじンゴ", config.TEXT_COLOR)
        self.draw_text_centered(center_x, 62, "5文字をえらぶ", config.GRID_COLOR)

        slot_size = 58
        gap = 10
        total_width = slot_size * 5 + gap * 4
        start_x = center_x - total_width // 2
        top_y = 106

        for index, letter in enumerate(self.state.slots):
            x = start_x + index * (slot_size + gap)
            y = top_y
            color = config.ACTIVE_COLOR if index == self.state.cursor_index else config.GRID_COLOR
            fill = config.ACCENT_COLOR if letter is not None else config.BACKGROUND_COLOR

            pyxel.rect(x + 2, y + 2, slot_size, slot_size, config.SHADOW_COLOR)
            pyxel.rect(x, y, slot_size, slot_size, fill)
            pyxel.rectb(x, y, slot_size, slot_size, color)
            if letter is not None:
                self.draw_text_centered(x + slot_size // 2, y + 21, letter, config.BACKGROUND_COLOR)
            else:
                self.draw_text_centered(x + slot_size // 2, y + 21, "・", config.LOCKED_COLOR)
            self.buttons.append(
                Button(x - 2, y - 2, slot_size + 4, slot_size + 4, "", "slot", index)
            )

            if index == self.state.cursor_index:
                pyxel.rect(x + 15, y + slot_size + 11, 28, 3, config.ACTIVE_COLOR)

        pyxel.line(24, 196, config.SCREEN_WIDTH - 24, 196, config.GRID_COLOR)
        if self.state.input_layer == InputLayer.ROWS:
            guide = "行をえらぶ"
        else:
            guide = f"{self.state.selected_group}行からえらぶ"
        self.draw_text_centered(center_x, 220, guide, config.TEXT_COLOR)

        if self.state.input_layer == InputLayer.ROWS:
            self.draw_row_panel(252)
        else:
            self.draw_kana_panel(252)

        self.draw_input_actions()

    def draw_row_panel(self, top_y: int) -> None:
        enabled_groups = set(self.state.enabled_groups())
        labels = tuple(KANA_GROUPS)
        start_x = 22
        button_w = 64
        button_h = 52
        gap = 8

        for index, group_id in enumerate(labels):
            row = index // 5
            col = index % 5
            self.draw_button(
                Button(
                    start_x + col * (button_w + gap),
                    top_y + row * (button_h + gap),
                    button_w,
                    button_h,
                    group_id,
                    "row",
                    group_id,
                    group_id in enabled_groups,
                )
            )

    def draw_kana_panel(self, top_y: int) -> None:
        if self.state.selected_group is None:
            return

        enabled_kana = set(self.state.enabled_kana())
        start_x = 22
        button_w = 64
        button_h = 48
        gap = 8

        for index, kana in enumerate(KANA_GROUPS[self.state.selected_group]):
            row = index // 5
            col = index % 5
            self.draw_button(
                Button(
                    start_x + col * (button_w + gap),
                    top_y + row * (button_h + gap),
                    button_w,
                    button_h,
                    kana,
                    "kana",
                    kana,
                    kana in enabled_kana,
                )
            )

    def draw_input_actions(self) -> None:
        y = 580
        self.draw_button(Button(22, y, 70, 46, "けす", "delete"))
        self.draw_button(Button(100, y, 94, 46, "ぜんぶけす", "clear"))
        self.draw_button(Button(202, y, 82, 46, "おまかせ", "auto"))
        self.draw_button(
            Button(292, y, 82, 46, "しらべる", "confirm", enabled=self.state.can_confirm())
        )
        self.draw_text_centered(
            config.SCREEN_WIDTH // 2,
            648,
            "Z/Enter けってい  X もどる",
            config.LOCKED_COLOR,
        )

    def draw_result(self) -> None:
        pyxel = self.pyxel
        entry = self.state.result_entry
        if entry is None:
            self.state.return_to_input(clear=True)
            return

        center_x = config.SCREEN_WIDTH // 2
        pyxel.rectb(
            16,
            18,
            config.SCREEN_WIDTH - 32,
            config.SCREEN_HEIGHT - 44,
            config.SHADOW_COLOR,
        )
        self.draw_text_centered(center_x, 28, "ごもじンゴ", config.TEXT_COLOR)
        self.draw_text_centered(
            center_x,
            88,
            content.format_slot_text(entry.word),
            config.ACCENT_COLOR,
        )
        pyxel.line(24, 174, config.SCREEN_WIDTH - 24, 174, config.GRID_COLOR)
        self.draw_text_centered(
            center_x,
            204,
            content.format_result_heading(entry.word),
            config.TEXT_COLOR,
        )

        category = CATEGORY_LABELS.get(entry.category, entry.category)
        self.draw_text_centered(center_x, 242, f"{category} / R{entry.rarity}", config.ACTIVE_COLOR)

        y = 282
        for paragraph in entry.paragraphs:
            for line in self.wrap_text(paragraph, 19):
                self.draw_text(34, y, line, config.TEXT_COLOR)
                y += 19
            y += 10

        self.draw_button(Button(58, 586, 126, 48, "もういちど", "again"))
        self.draw_button(Button(212, 586, 126, 48, "べつのことば", "new"))
        self.draw_text_centered(
            center_x,
            650,
            f"{entry.id} / {content.CONTENT_COUNT}語",
            config.LOCKED_COLOR,
        )

    def draw_button(self, button: Button) -> None:
        pyxel = self.pyxel
        self.buttons.append(button)
        focused = False
        if button.enabled:
            focused = self.focusable_buttons().index(button) == self.focus_index()
        fill = config.SHADOW_COLOR if button.enabled else config.BACKGROUND_COLOR
        border = config.ACTIVE_COLOR if focused else config.GRID_COLOR
        text_color = config.TEXT_COLOR if button.enabled else config.LOCKED_COLOR
        y = button.y + (1 if focused and self.press_feedback_frames > 0 else 0)

        pyxel.rect(button.x + 2, y + 2, button.width, button.height, config.SHADOW_COLOR)
        pyxel.rect(button.x, y, button.width, button.height, fill)
        pyxel.rectb(button.x, y, button.width, button.height, border)
        self.draw_text_centered(
            button.x + button.width // 2,
            y + button.height // 2 - 6,
            button.label,
            text_color,
        )

    def focusable_buttons(self) -> list[Button]:
        return [button for button in self.buttons if button.enabled and button.label]

    def focus_index(self) -> int:
        buttons = self.focusable_buttons()
        if not buttons:
            self.state.focused_button = 0
            return 0
        self.state.focused_button %= len(buttons)
        return self.state.focused_button

    def move_focus(self, delta: int) -> None:
        buttons = self.focusable_buttons()
        if not buttons:
            return
        self.state.focused_button = (self.state.focused_button + delta) % len(buttons)

    def activate_focused_button(self) -> None:
        buttons = self.focusable_buttons()
        if not buttons:
            return
        self.run_button_action(buttons[self.focus_index()])

    def activate_button_at(self, x: int, y: int) -> None:
        for button in reversed(self.buttons):
            if (
                button.enabled
                and button.x <= x < button.x + button.width
                and button.y <= y < button.y + button.height
            ):
                self.run_button_action(button)
                return

    def run_button_action(self, button: Button) -> None:
        if not button.enabled:
            return

        if button.action == "slot" and isinstance(button.value, int):
            self.state.select_slot(button.value)
        elif button.action == "row" and isinstance(button.value, str):
            self.state.open_kana_group(button.value)
        elif button.action == "kana" and isinstance(button.value, str):
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
            self.state.return_to_input(clear=False)
        elif button.action == "new":
            self.state.return_to_input(clear=True)

        self.press_feedback_frames = 3

    def wrap_text(self, text: str, max_chars: int) -> list[str]:
        return [text[index : index + max_chars] for index in range(0, len(text), max_chars)]

    def draw_text_centered(self, center_x: int, y: int, text: str, color: int) -> None:
        self.draw_text(center_x - self.text_width(text) // 2, y, text, color)

    def text_width(self, text: str) -> int:
        return sum(12 if ord(char) > 127 else 6 for char in text)

    def draw_text(self, x: int, y: int, text: str, color: int) -> None:
        self.pyxel.text(x, y, text, color, self.font)


def main() -> None:
    GomojiApp()
