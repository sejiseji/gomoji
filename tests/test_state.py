from __future__ import annotations

import unittest

from gomoji import content
from gomoji.app import RESULT_TEXT_BOTTOM, RESULT_TEXT_TOP, RESULT_WRAP_CHARS
from gomoji.input_model import InputLayer, InputState, ScreenState


class InputStateTest(unittest.TestCase):
    def test_starts_with_empty_input_slots(self) -> None:
        state = InputState()

        self.assertEqual(state.screen, ScreenState.INPUT)
        self.assertEqual(state.input_layer, InputLayer.ROWS)
        self.assertEqual(state.slots, [None, None, None, None, None])
        self.assertEqual(state.cursor_index, 0)

    def test_prefix_control_reaches_registered_word(self) -> None:
        state = InputState()

        for kana in ("ね", "こ", "ぱ", "ん", "ち"):
            self.assertTrue(state.select_kana(kana))

        self.assertEqual(state.word, "ねこぱんち")
        self.assertTrue(state.input_locked)
        self.assertEqual(state.enabled_kana(), ())
        self.assertTrue(state.can_confirm())
        self.assertTrue(state.confirm_word())
        self.assertEqual(state.screen, ScreenState.REVEAL)
        self.assertTrue(state.result_is_new)

        while state.screen == ScreenState.REVEAL:
            state.tick_reveal()

        self.assertEqual(state.screen, ScreenState.RESULT)
        self.assertEqual(state.result_entry, content.BY_WORD["ねこぱんち"])
        self.assertEqual(state.found_count, 1)

    def test_repeated_result_is_not_new(self) -> None:
        state = InputState()
        state.slots = list("ねこぱんち")

        self.assertTrue(state.confirm_word())
        state.finish_reveal()
        self.assertTrue(state.result_is_new)

        state.return_to_input(clear=False)
        self.assertTrue(state.confirm_word())
        state.finish_reveal()

        self.assertFalse(state.result_is_new)
        self.assertEqual(state.found_count, 1)

    def test_invalid_kana_is_rejected_by_prefix(self) -> None:
        state = InputState()

        self.assertFalse(state.select_kana("わ"))
        self.assertEqual(state.word, "")

    def test_completed_word_rejects_extra_kana_until_slot_is_selected(self) -> None:
        state = InputState()
        for kana in "ねこぱんち":
            self.assertTrue(state.select_kana(kana))

        self.assertFalse(state.select_kana("ま"))
        self.assertEqual(state.word, "ねこぱんち")

        state.select_slot(2)
        self.assertFalse(state.input_locked)
        self.assertTrue(state.select_kana("ぱ"))
        self.assertEqual(state.slots, ["ね", "こ", "ぱ", None, None])

    def test_editing_middle_slot_clears_following_slots(self) -> None:
        state = InputState()
        state.slots = list("ねこぱんち")

        state.select_slot(2)
        self.assertTrue(state.select_kana("ぱ"))

        self.assertEqual(state.slots, ["ね", "こ", "ぱ", None, None])
        self.assertEqual(state.cursor_index, 3)

    def test_delete_behaviour(self) -> None:
        state = InputState()
        state.slots = ["ね", "こ", None, None, None]
        state.cursor_index = 2

        state.delete_character()

        self.assertEqual(state.slots, ["ね", None, None, None, None])
        self.assertEqual(state.cursor_index, 1)

    def test_autofill_picks_registered_word(self) -> None:
        state = InputState()
        state.autofill_word()

        self.assertIn(state.word, content.BY_WORD)
        self.assertTrue(state.can_confirm())

    def test_result_heading_does_not_append_ngo(self) -> None:
        self.assertEqual(content.format_slot_text("ねこぱんち"), "ね こ ぱ ん ち")
        self.assertEqual(content.format_result_heading("ねこぱんち"), "【ねこぱんち】")

    def test_reviewed_result_text_fits_current_panel(self) -> None:
        for entry in content.RUNTIME_ENTRIES:
            y = RESULT_TEXT_TOP
            for paragraph in entry.paragraphs:
                y += len(self.wrap_text(paragraph, RESULT_WRAP_CHARS)) * 19
                y += 10
            self.assertLessEqual(y, RESULT_TEXT_BOTTOM, entry.word)

    def wrap_text(self, text: str, max_chars: int) -> list[str]:
        return [text[index : index + max_chars] for index in range(0, len(text), max_chars)]


if __name__ == "__main__":
    unittest.main()
