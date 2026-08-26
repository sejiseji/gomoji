from __future__ import annotations

import unittest

from gomoji import content
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

        for group_id, kana in (
            ("な", "ね"),
            ("か", "こ"),
            ("は", "ぱ"),
            ("わ", "ん"),
            ("た", "ち"),
        ):
            self.assertTrue(state.open_kana_group(group_id))
            self.assertTrue(state.select_kana(kana))

        self.assertEqual(state.word, "ねこぱんち")
        self.assertTrue(state.can_confirm())
        self.assertTrue(state.confirm_word())
        self.assertEqual(state.screen, ScreenState.RESULT)
        self.assertEqual(state.result_entry, content.BY_WORD["ねこぱんち"])

    def test_invalid_kana_is_rejected_by_prefix(self) -> None:
        state = InputState()

        self.assertFalse(state.open_kana_group("わ"))
        self.assertEqual(state.word, "")

    def test_editing_middle_slot_clears_following_slots(self) -> None:
        state = InputState()
        state.slots = list("ねこぱんち")

        state.select_slot(2)
        self.assertTrue(state.open_kana_group("は"))
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


if __name__ == "__main__":
    unittest.main()
