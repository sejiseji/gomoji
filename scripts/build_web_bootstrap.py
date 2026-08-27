from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gomoji import content  # noqa: E402

BEGIN_MARKER = "# BEGIN GENERATED ENTRIES\n"
END_MARKER = "# END GENERATED ENTRIES\n"

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


def quote(value: str) -> str:
    return repr(value)


def build_entries_block() -> str:
    lines = [BEGIN_MARKER, "ENTRIES = (\n"]
    for entry in content.RUNTIME_ENTRIES:
        category = CATEGORY_LABELS.get(entry.category, entry.category)
        lines.extend(
            [
                "    {\n",
                f"        \"id\": {quote(entry.id)},\n",
                f"        \"word\": {quote(entry.word)},\n",
                f"        \"category\": {quote(category)},\n",
                f"        \"rarity\": {entry.rarity},\n",
                "        \"paragraphs\": (\n",
            ]
        )
        for paragraph in entry.paragraphs:
            lines.append(f"            {quote(paragraph)},\n")
        lines.extend(["        ),\n", "    },\n"])
    lines.extend([")\n", END_MARKER])
    return "".join(lines)


def replace_entries_block(source: str) -> str:
    before, marker, remainder = source.partition(BEGIN_MARKER)
    if not marker:
        raise SystemExit(f"missing marker: {BEGIN_MARKER.strip()}")
    _old_block, marker, after = remainder.partition(END_MARKER)
    if not marker:
        raise SystemExit(f"missing marker: {END_MARKER.strip()}")
    return before + build_entries_block() + after


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync web_bootstrap.py embedded entries.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "web_bootstrap.py",
        help="web_bootstrap.py path to update.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the generated entries block is not current.",
    )
    args = parser.parse_args()

    source = args.output.read_text(encoding="utf-8")
    updated = replace_entries_block(source)
    if args.check:
        if updated != source:
            raise SystemExit(f"generated entries block is stale: {args.output}")
        print(f"generated entries block is current: {args.output}")
        return

    args.output.write_text(updated, encoding="utf-8")
    print(f"wrote {content.CONTENT_COUNT} entries to {args.output}")


if __name__ == "__main__":
    main()
