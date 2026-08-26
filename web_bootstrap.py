# title: Gomoji
# author: sejiseji
# desc: Pyxel project scaffold for Gomoji
# site: https://github.com/sejiseji/gomoji
# license: MIT
# version: 0.1.0

from __future__ import annotations

import sys


def main() -> None:
    sys.path.insert(0, "src")

    from gomoji.app import main as run_app

    run_app()


main()
