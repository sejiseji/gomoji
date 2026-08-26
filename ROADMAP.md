# ごもじンゴ Roadmap

## GMG000 — 基盤

Done.

- Pyxel scaffold
- `396x696` iPhone 16-oriented screen
- Japanese BDF font
- GitHub Pages
- pytest and ruff
- Placeholder 5-slot screen

## GMG001 — 仕様・コンテンツ基盤導入

Done in this branch.

- Detailed spec copied to `docs/`
- Content source packs copied to `content/source/`
- Schemas, fixtures, and audit reports copied to `content/`
- Validation, audit, and deterministic build scripts copied to `scripts/`
- Reviewed 40-entry runtime data generated at `src/gomoji/generated/content_data.py`
- Runtime app imports generated content via `src/gomoji/content.py`
- Existing Pages bootstrap kept self-contained to avoid the known Pyxel Web package import issue
- Existing `Space` placeholder cycling remains temporary and should be replaced in GMG002

## GMG002 — スマートフォン5文字入力

Next recommended task.

- Tap-selectable 5 slots
- Row selection and character selection
- Voiced, semi-voiced, and small kana
- Delete, clear all, random word
- Prefix trie candidate control
- PC helper controls

## GMG003 — 結果パネル

- Confirm selected word
- Result heading without fixed `んご/ンゴ`
- Category and rarity display
- Wrapped explanation panel
- Retry and different word actions

## GMG004 — Web共通化

- Make `src/gomoji` the single source of truth
- Generate `web_bootstrap.py` deterministically
- Add web bootstrap `--check` to CI workflow

## GMG005+ — 保存・辞典・1000語運用

- Discovery persistence
- Dictionary view
- Development-only 1000-entry draft builds
- Draft review workflow
- Final 1000 approved release gate
