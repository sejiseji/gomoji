from __future__ import annotations

import unittest

from gomoji import content
from gomoji.app import AppState


class AppStateTest(unittest.TestCase):
    def test_word_cycles_through_configured_values(self) -> None:
        state = AppState()

        seen = []
        for _ in range(content.CONTENT_COUNT):
            seen.append(state.word)
            state.next_word()

        self.assertEqual(tuple(seen), content.RUNTIME_WORDS)
        self.assertEqual(state.word, content.RUNTIME_WORDS[0])

    def test_debug_starts_disabled(self) -> None:
        self.assertIs(AppState().debug_enabled, False)

    def test_result_heading_does_not_append_ngo(self) -> None:
        self.assertEqual(content.format_slot_text("ねこぱんち"), "ね こ ぱ ん ち")
        self.assertEqual(content.format_result_heading("ねこぱんち"), "【ねこぱんち】")


if __name__ == "__main__":
    unittest.main()
