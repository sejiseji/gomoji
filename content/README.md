# コンテンツデータ

## 正本

`content/source/pack_001.json`〜`pack_020.json`が編集用の正本です。各50件、合計1000件です。

現状:

- `reviewed`: 90件
- `draft`: 910件
- `approved`: 0件

90件の`reviewed`は個別作成・推敲済みの確認セットです。910件の`draft`は、入力分岐・カテゴリ配分・画面折り返し・1000件運用を先に検証するための制作スキャフォールドです。**910件をそのまま公開品質とは扱わないでください。**

## 固定「んご」廃止

`ンゴ/んご`を各語の後ろへ付けません。

正しい結果見出し:

```text
【ねこぱんち】
```

誤り:

```text
【ねこぱんちンゴ】
ね こ ぱ ん ち
          んご
```

作品名の`ごもじンゴ`だけは維持します。

## 検証

```bash
python scripts/validate_content.py
python scripts/audit_content.py
```

公開判定:

```bash
python scripts/validate_content.py --release
```

現状は1000件が`approved`ではないため、`--release`が失敗するのが正しい状態です。

## 生成

レビュー済み90件だけ:

```bash
python scripts/build_content.py --output src/gomoji/generated/content_data.py
```

1000件すべてを開発用に含める:

```bash
python scripts/build_content.py --include-drafts --output src/gomoji/generated/content_data.py
```

本番生成では、1000件すべてを`approved`へ移した後に`--release`を使用します。
