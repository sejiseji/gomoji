# ごもじンゴ Roadmap

## GMG000 — 基盤

Done.

- Pyxel scaffold
- `396x696` iPhone 16-oriented screen
- Japanese BDF font
- GitHub Pages
- pytest and ruff
- Initial placeholder 5-slot screen

## GMG001 — 仕様・コンテンツ基盤導入

Done in this branch.

- Detailed spec copied to `docs/`
- Content source packs copied to `content/source/`
- Schemas, fixtures, and audit reports copied to `content/`
- Validation, audit, and deterministic build scripts copied to `scripts/`
- Reviewed 40-entry runtime data generated at `src/gomoji/generated/content_data.py`
- Runtime app imports generated content via `src/gomoji/content.py`
- Existing Pages bootstrap kept self-contained to avoid the known Pyxel Web package import issue

## GMG002 — スマートフォン5文字入力

Done.

- Tap-selectable 5 slots
- Scrollable kana grid
- Voiced, semi-voiced, and small kana
- Delete, clear all, random word
- Prefix trie candidate control
- Completed-word input lock
- PC helper controls
- Result panel for completed words
- Self-contained Pages bootstrap updated with the same mobile input flow

## GMG003 — 結果演出・発見体験

Done.

- Discovery animation and short confirm delay
- NEW and found-count presentation
- Result text overflow QA across the reviewed runtime set
- Stronger PC focus-grid behavior

## GMG004 — Web共通化

Done.

- Runtime content is the source of truth for the Pages bootstrap entries
- `scripts/build_web_bootstrap.py` deterministically syncs `web_bootstrap.py`
- Pages workflow checks the generated bootstrap entry block

## GMG005+ — 保存・辞典・1000語運用

- Discovery persistence
- Dictionary view
- Development-only 1000-entry draft builds
- Draft review workflow
- Wave-by-wave 50-entry editorial review
- Final 1000 approved release gate
