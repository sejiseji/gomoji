# ごもじンゴ コンテンツ推敲 Wave 01 — Codex投入指示

このパッケージは、既存の1000語スキャフォールドから50件を手動推敲し、`reviewed`へ移す差分です。

## 対象

- 基準コンテンツ: v0.2.0
- 差分: 10カテゴリ各5語、合計50語
- 適用後: `reviewed 90 / draft 910 / approved 0`
- `approved`への変更は行わない

## 読む順番

1. `README.md`
2. `reports/wave_01_catalog.md`
3. `reports/wave_01_editorial_audit.md`
4. `content/patches/wave_01_50_reviewed.json`

## 適用

リポジトリ直下へ、次の2ファイルを同じ相対パスで配置してください。

- `content/patches/wave_01_50_reviewed.json`
- `scripts/apply_content_wave01.py`

その後、以下を実行してください。

```bash
python scripts/apply_content_wave01.py
python scripts/apply_content_wave01.py --check
python scripts/validate_content.py
python scripts/audit_content.py
python scripts/build_content.py --output src/gomoji/generated/content_data.py
python scripts/sync_web_bootstrap.py
python scripts/sync_web_bootstrap.py --check
```

既存リポジトリの実際のスクリプト名や出力先が異なる場合は、GMG004で確立した正本→Web同期の流れへ合わせてください。

`audit_content.py`の結論文が旧件数`reviewed 40 / draft 960`を固定記述している場合は、`status_counts`から動的に生成するよう直してください。集計表だけ更新され、結論文だけ古いまま残るのを防ぐためです。

## 実装上の制約

- ID、カテゴリ、レアリティは変更しない。
- patch内の`previous_word`と現在値が一致しない場合は自動適用を止め、差分を報告する。
- 50件は`reviewed`のまま登録する。
- 作品名以外へ固定の`んご／ンゴ`を加えない。
- 説明文をテンプレートへ再変換しない。
- 語尾統一、三段落の定型化、機械的な言い換えを行わない。
- 25文字折り返し後の実画面を、長い項目を中心に確認する。

## 重点実機確認

- `ひるのびる`
- `やるきまち`
- `まどすずめ`
- `もちあわせ`
- `しれっとめ`
- `ものさがし`
- `おやつわけ`
- `まよいみち`
- `かきなおし`
- `みちのさき`

## 完了報告

- 適用件数
- `reviewed / draft / approved`件数
- content validation結果
- audit結果
- runtime生成件数
- Web同期結果
- pytest / ruff / compileall / smoke結果
- iPhone縦画面での折り返し確認
- 文章または語の修正が必要と判断した項目
