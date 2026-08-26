# Codex投入指示 — ごもじンゴ GMG001

リポジトリ:

```text
git@github.com:sejiseji/gomoji.git
```

基準コミット:

```text
9343568 Tune placeholder for Japanese iPhone layout
```

添付パッケージの`docs/gomojingo_detailed_spec_v0.2.0.md`を実装基準として使用してください。

## 今回の範囲

**GMG001 — 仕様・コンテンツ基盤導入だけを実施してください。**

スマートフォン入力UIは次タスクGMG002で行います。今回はデータ基盤を安全に取り込み、既存Pagesを壊さないことを優先します。

## 実施内容

1. リポジトリ全体を確認する。
2. 現行の`src/gomoji`、`web_bootstrap.py`、Pages workflow、pytest、ruff、READMEを把握する。
3. 添付の`content/`、`scripts/`、`tests/test_content_contract.py`を、既存構成へ適合させて追加する。
4. `python scripts/validate_content.py`を通す。
5. reviewed 40件だけを次へ生成する。

```bash
python scripts/build_content.py   --output src/gomoji/generated/content_data.py
```

6. 生成モジュールをローカルアプリからimportできるようにする。
7. 現在の仮ワード配列は、生成済みreviewedデータから数件を表示する形へ置換してよい。
8. 既存のSpace切替は、GMG002で削除予定であることを文書へ記録する。
9. `web_bootstrap.py`は今回壊さない。共通化はGMG004で行う。
10. README、ロードマップ、handoffが存在する場合は状態を更新する。
11. pytest、ruff、headless smokeを実行する。
12. 変更をコミットし、Pagesが従来どおり起動することを確認する。

## 固定「んご」廃止の必須確認

作品名`ごもじンゴ`以外へ、固定の`んご/ンゴ`を表示しないでください。

正:

```text
ね こ ぱ ん ち
【ねこぱんち】
```

誤:

```text
ね こ ぱ ん ち
          んご

【ねこぱんちンゴ】
```

今回は仮画面であっても、固定`んご`を追加しないでください。

## データの扱い

同梱データは合計1000件です。

```text
reviewed: 40
draft:    960
approved: 0
```

- 標準生成ではreviewed 40件だけを使う。
- `--include-drafts`は開発規模確認に限る。
- 960 draftを公開品質と扱わない。
- `--release`が失敗するのは現状では正しい。
- 1000件すべてを一括で`approved`へ変更しない。

## 完了報告

以下を報告してください。

- 実装内容
- 主な変更ファイル
- コンテンツ件数
- validation結果
- build結果
- pytest結果
- ruff結果
- headless smoke結果
- Pages確認
- 固定`んご/ンゴ`が作品名以外へ入っていないこと
- 既知の問題
- 次タスクGMG002への推奨事項
