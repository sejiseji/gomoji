#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_patch(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("patch_id") != "GMG-CONTENT-WAVE-01":
        raise SystemExit(f"unexpected patch_id: {data.get('patch_id')!r}")
    return data


def pack_path_for(source_dir: Path, entry_id: str) -> Path:
    number = int(entry_id[3:])
    pack_number = (number - 1) // 50 + 1
    return source_dir / f"pack_{pack_number:03d}.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=Path("content/source"))
    parser.add_argument(
        "--patch",
        type=Path,
        default=Path("content/patches/wave_01_50_reviewed.json"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    patch = load_patch(args.patch)
    changed_files: dict[Path, dict] = {}
    already_applied = 0
    pending = 0

    for change in patch["entries"]:
        entry_id = change["id"]
        previous_word = change["previous_word"]
        replacement = change["entry"]
        path = pack_path_for(args.source_dir, entry_id)
        if path not in changed_files:
            changed_files[path] = json.loads(path.read_text(encoding="utf-8"))
        pack = changed_files[path]

        for index, current in enumerate(pack["entries"]):
            if current["id"] != entry_id:
                continue
            if current == replacement:
                already_applied += 1
                break
            if current.get("word") != previous_word:
                raise SystemExit(
                    f"{entry_id}: expected previous word {previous_word!r}, "
                    f"found {current.get('word')!r}; refusing to overwrite"
                )
            pack["entries"][index] = replacement
            pending += 1
            break
        else:
            raise SystemExit(f"{entry_id}: not found in {path}")

    if args.check:
        if pending:
            print(f"wave 01 not applied: pending={pending}, already_applied={already_applied}")
            return 1
        print(f"wave 01 applied: already_applied={already_applied}")
        return 0

    for path, pack in changed_files.items():
        path.write_text(
            json.dumps(pack, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"wave 01 applied: changed={pending}, already_applied={already_applied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
