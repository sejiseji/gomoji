#!/usr/bin/env python3
"""Generate a Markdown audit report for ごもじンゴ content."""

from __future__ import annotations

import argparse
import difflib
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from validate_content import ValidationResult, load_packs, validate_global

SMALL_KANA = frozenset("ぁぃぅぇぉっゃゅょゎ")
VOICED_KANA = frozenset(
    "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゔ"
)


def normalized_description(entry: dict[str, Any]) -> str:
    text = "".join(entry["paragraphs"])
    return re.sub(r"[「」『』【】、。！？・：；（）\s]", "", text)


def find_similarity_candidates(
    entries: list[dict[str, Any]],
    *,
    threshold: float,
    limit: int,
) -> list[tuple[float, str, str, str, str]]:
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        by_category[entry["category"]].append(entry)

    candidates: list[tuple[float, str, str, str, str]] = []
    for category_entries in by_category.values():
        normalized = [
            (entry, normalized_description(entry))
            for entry in category_entries
        ]
        for left_index in range(len(normalized)):
            left, left_text = normalized[left_index]
            for right_index in range(left_index + 1, len(normalized)):
                right, right_text = normalized[right_index]
                ratio = difflib.SequenceMatcher(
                    None,
                    left_text,
                    right_text,
                    autojunk=False,
                ).ratio()
                if ratio >= threshold:
                    candidates.append(
                        (
                            ratio,
                            left["id"],
                            left["word"],
                            right["id"],
                            right["word"],
                        )
                    )

    candidates.sort(reverse=True)
    return candidates[:limit]


def render_counter_table(counter: Counter[Any], *, label: str) -> list[str]:
    lines = [f"| {label} | 件数 |", "|---|---:|"]
    for key, count in sorted(counter.items(), key=lambda item: str(item[0])):
        lines.append(f"| `{key}` | {count} |")
    return lines


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=root / "content" / "source",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "content" / "reports" / "content_audit.generated.md",
    )
    parser.add_argument("--similarity-threshold", type=float, default=0.82)
    parser.add_argument("--similarity-limit", type=int, default=50)
    args = parser.parse_args()

    result = ValidationResult()
    entries = load_packs(args.source_dir, result)
    validate_global(entries, result, release=False)

    lengths = [sum(len(p) for p in entry["paragraphs"]) for entry in entries]
    status_counts = Counter(entry["status"] for entry in entries)
    category_counts = Counter(entry["category"] for entry in entries)
    rarity_counts = Counter(entry["rarity"] for entry in entries)
    source_counts = Counter(entry["source_kind"] for entry in entries)
    first_counts = Counter(entry["word"][0] for entry in entries)
    ending_counts = Counter(entry["ending_family"] for entry in entries)

    small_kana_words = [
        entry for entry in entries if any(ch in SMALL_KANA for ch in entry["word"])
    ]
    voiced_words = [
        entry for entry in entries if any(ch in VOICED_KANA for ch in entry["word"])
    ]
    similarity = find_similarity_candidates(
        entries,
        threshold=args.similarity_threshold,
        limit=args.similarity_limit,
    )

    lines: list[str] = [
        "# ごもじンゴ コンテンツ監査レポート",
        "",
        "> このレポートは構造監査であり、960件のドラフトを公開品質と認定するものではない。",
        "",
        "## 概要",
        "",
        f"- 総件数: **{len(entries)}**",
        f"- 構造エラー: **{len(result.errors)}**",
        f"- 警告: **{len(result.warnings)}**",
        (
            f"- 説明文字数: 最小 **{min(lengths)}** / "
            f"中央値 **{statistics.median(lengths):.1f}** / "
            f"平均 **{statistics.mean(lengths):.1f}** / 最大 **{max(lengths)}**"
        ),
        f"- 小書き文字を含む語: **{len(small_kana_words)}**",
        f"- 濁音・半濁音を含む語: **{len(voiced_words)}**",
        (
            f"- 類似度候補: **{len(similarity)}**"
            f"（閾値 {args.similarity_threshold:.2f}、上位 {args.similarity_limit} 件まで）"
        ),
        "",
        "## ステータス",
        "",
        *render_counter_table(status_counts, label="status"),
        "",
        "## カテゴリ",
        "",
        *render_counter_table(category_counts, label="category"),
        "",
        "## レアリティ",
        "",
        *render_counter_table(rarity_counts, label="rarity"),
        "",
        "## 生成元",
        "",
        *render_counter_table(source_counts, label="source_kind"),
        "",
        "## 先頭文字",
        "",
        *render_counter_table(first_counts, label="先頭文字"),
        "",
        "## ending_family 上位",
        "",
        "| ending_family | 件数 |",
        "|---|---:|",
    ]
    for family, count in ending_counts.most_common(30):
        lines.append(f"| `{family}` | {count} |")

    lines.extend(
        [
            "",
            "## 小書き文字を含む語",
            "",
            "| ID | 語 | category | status |",
            "|---|---|---|---|",
        ]
    )
    for entry in small_kana_words:
        lines.append(
            f"| `{entry['id']}` | {entry['word']} | `{entry['category']}` | `{entry['status']}` |"
        )

    lines.extend(
        [
            "",
            "## 類似説明候補",
            "",
            "| 類似度 | 左 | 右 |",
            "|---:|---|---|",
        ]
    )
    if similarity:
        for ratio, left_id, left_word, right_id, right_word in similarity:
            lines.append(
                f"| {ratio:.3f} | `{left_id}` {left_word} | `{right_id}` {right_word} |"
            )
    else:
        lines.append("| - | 候補なし | 候補なし |")

    if result.errors:
        lines.extend(["", "## 構造エラー", ""])
        for error in result.errors:
            lines.append(f"- {error}")

    if result.warnings:
        lines.extend(["", "## 警告", ""])
        for warning in result.warnings:
            lines.append(f"- {warning}")

    lines.extend(
        [
            "",
            "## 編集上の結論",
            "",
            "- `reviewed` 40件はUI・入力・本文折り返しのゴールデンセットとして使用できる。",
            (
                "- `draft` 960件は語数・分岐・カテゴリ・レアリティを満たす"
                "制作スキャフォールドであり、公開前に個別レビューが必要。"
            ),
            (
                "- リリース判定では1000件すべてを`approved`へ移し、"
                "`validate_content.py --release`を通す。"
            ),
            (
                "- `ごもじンゴ`の「ンゴ」は作品名だけに残し、"
                "各語・結果見出し・定型説明へ固定付加しない。"
            ),
            "",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote audit report: {args.output}")
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
