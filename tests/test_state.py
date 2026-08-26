from __future__ import annotations

import unittest

from gomoji import config
from gomoji.app import AppState


class AppStateTest(unittest.TestCase):
    def test_motif_cycles_through_configured_values(self) -> None:
        state = AppState()

        seen = []
        for _ in range(len(config.PLACEHOLDER_MOTIFS)):
            seen.append(state.motif)
            state.next_motif()

        self.assertEqual(tuple(seen), config.PLACEHOLDER_MOTIFS)
        self.assertEqual(state.motif, config.PLACEHOLDER_MOTIFS[0])

    def test_debug_starts_disabled(self) -> None:
        self.assertIs(AppState().debug_enabled, False)


if __name__ == "__main__":
    unittest.main()
