from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def main() -> None:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

    from gomoji.app import main as run_app

    run_app()


if __name__ == "__main__":
    main()
