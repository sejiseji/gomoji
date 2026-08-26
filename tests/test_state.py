from __future__ import annotations

import unittest

from gomoji import config
from gomoji.app import AppState


class AppStateTest(unittest.TestCase):
    def test_word_cycles_through_configured_values(self) -> None:
        state = AppState()

        seen = []
        for _ in range(len(config.PLACEHOLDER_WORDS)):
            seen.append(state.word)
            state.next_word()

        self.assertEqual(tuple(seen), config.PLACEHOLDER_WORDS)
        self.assertEqual(state.word, config.PLACEHOLDER_WORDS[0])

    def test_debug_starts_disabled(self) -> None:
        self.assertIs(AppState().debug_enabled, False)


if __name__ == "__main__":
    unittest.main()
