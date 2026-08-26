# ごもじンゴ 詳細仕様書 v0.2.0

- 文書種別: Codex実装用プロダクト・UX・技術・コンテンツ仕様
- 作成日: 2026-08-26
- 対象リポジトリ: `git@github.com:sejiseji/gomoji.git`
- 基準コミット: `9343568 Tune placeholder for Japanese iPhone layout`
- 対象ランタイム: Python / Pyxel 2.9.9 / Pyxel Web / GitHub Pages
- 基準画面: iPhone 16向け縦画面、Pyxel内部解像度 `396x696`
- コンテンツ目標: 5文字ひらがな1000語
- 文書ステータス: 実装開始可能
- 重要変更: **各語の後ろへ固定の「んご／ンゴ」を付けない**

---

## 0. Codexへの最上位指示

この文書と同梱データを「ごもじンゴ」の実装基準とする。

Codexは作業前にリポジトリ全体を読み、現在の構成、起動方法、テスト、GitHub Pagesワークフロー、`web_bootstrap.py`の制約を確認すること。既存の正常動作を壊さず、後述のタスク単位で実装する。

必須原則:

1. スマートフォンのタッチ操作を第一入力方式とする。
2. PCキーボード操作は補助入力として維持する。
3. 5文字の語と説明はすべて事前定義データから取得する。
4. 実行時の生成AI、外部API、ネットワーク辞書を使わない。
5. 1000語の編集用正本をPythonコードへ直接手書きしない。
6. 編集用JSONを検証し、ランタイム用Pythonへ決定的に生成する。
7. ローカル版とWeb版のゲームロジックを手作業で二重管理しない。
8. `ごもじンゴ`の「ンゴ」は**作品名だけ**に残す。
9. 入力語、文字スロット、結果見出し、定型メッセージへ「んご／ンゴ」を固定付加しない。
10. 仕様と現行リポジトリが衝突した場合は、既存の動作を保ちながら差異を報告する。
11. 無関係なファイルの改名、整理、大規模再構成を行わない。
12. 各タスク終了時に、変更、検証、実機確認、既知の問題、次タスクを報告する。

---

## 1. 確定事項

### 1.1 作品名

**ごもじンゴ**

### 1.2 一文説明

5文字のひらがなを選ぶと、その言葉についての妙にもっともらしい説明が表示される、短時間型の偽辞典ゲーム。

### 1.3 「ンゴ」の扱い

次を確定仕様とする。

- 作品名は`ごもじンゴ`のまま。
- 5文字の入力語へ`んご`や`ンゴ`を追加しない。
- 文字スロットの下や右下へ固定表示しない。
- 結果見出しは`【ねこぱんち】`とする。
- `【ねこぱんちンゴ】`にはしない。
- 説明本文でも`ンゴ`を定型句として使わない。
- 掲示板風の面白さは、乾いた断定、具体例、最後の一文の落差で出す。
- 個別の文章として必要なら使えるが、公開前レビュー対象とし、頻度は極端に低くする。

### 1.4 画面構造

起動後は大きなタイトル画面を挟まず、原則として直接入力画面へ入る。

基本構造:

```text
        ごもじンゴ

  ○   ○   ○   ○   ○

──────────────────

  入力時: かな選択パネル
  結果時: 言葉の説明
```

入力中は下部がかなパネルになる。確定後は同じ下部領域が説明パネルへ切り替わる。

### 1.5 コンテンツ

- 5文字のひらがな1000語を目標とする。
- 同じ語には常に同じ説明を返す。
- 未登録語を即興生成しない。
- P0は登録語へ必ず到達する候補制御付き入力とする。
- 完全自由入力はP2候補とする。

---

## 2. 現在のリポジトリ基準状態

ユーザー報告時点:

- Repository: `git@github.com:sejiseji/gomoji.git`
- Pages: `https://sejiseji.github.io/gomoji/?v=9343568`
- latest: `9343568 Tune placeholder for Japanese iPhone layout`
- branch: `main`
- working tree: clean
- Pyxel: `2.9.9`
- canvas: `396x696`
- 日本語BDF: `assets/umplus_j12r.bdf`
- ローカル本体: `src/gomoji/app.py`
- Webエントリ: `web_bootstrap.py`
- Pages HTML: `index.html`
- 現在のWeb版はpackage import問題を避けるため、`web_bootstrap.py`が自己完結している

既存の仮ワード切替と`Space`操作は、スマートフォン入力UIへ置き換えてよい。

---

## 3. 体験設計

### 3.1 中核体験

1. 5文字を選ぶ。
2. その並びから意味を想像する。
3. 確定する。
4. 予想外だが少し納得できる説明を読む。
5. 別の五文字を探す。

### 3.2 面白さの優先順位

1. 説明文そのもの
2. 音と意味の意外な対応
3. 5文字を掘り当てる入力
4. 結果画面の見せやすさ
5. 収集

派手な演出、長い導入、複雑なメニューは優先しない。

### 3.3 1回の所要時間

- 文字選択: 5〜20秒
- 確定演出: 0.2〜0.8秒
- 説明閲覧: 任意
- 1語だけなら30秒以内で満足できること

### 3.4 非目標

P0では実装しない。

- 実行時のAI生成
- サーバー通信
- ユーザー投稿
- ランキング
- アカウント
- 広告・課金
- 漢字、カタカナ、英数字の入力
- 日本語IMEへの依存
- フリック入力の再実装
- 自由入力での未登録語個別解説
- 長いストーリー
- ステージ制

---

## 4. 画面とレイアウト

### 4.1 内部解像度

```python
SCREEN_WIDTH = 396
SCREEN_HEIGHT = 696
FPS = 30
```

現行値を維持する。

### 4.2 セーフ領域

Pyxel画面内で次を確保する。

```python
SAFE_LEFT = 22
SAFE_RIGHT = 22
SAFE_TOP = 18
SAFE_BOTTOM = 30
```

主要操作を下端へ密着させない。Safariの下部UIが表示されても、ゲーム内の主要ボタンが視覚的に窮屈にならない配置とする。

### 4.3 タッチターゲット

- 主要ボタン高さ: 44px以上
- かな文字ボタン: 原則52〜60px四方
- スロット: 58〜64px四方
- ボタン間隔: 6〜10px
- 見た目の枠より、タッチ判定を2〜4px広げてよい
- 重なるタッチ判定は禁止

### 4.4 色

現行の黒背景、白、水色、青、黄色系を維持する。

状態:

| 状態 | 表現 |
|---|---|
| 通常 | 青系の枠、白系の文字 |
| 現在選択 | 水色の枠、下線 |
| 入力済み | 黄または明るい地 |
| 押下中 | 1〜2px沈む、枠が明るくなる |
| 無効 | 暗い青または灰色 |
| NEW | 黄色系の小さな表示 |

### 4.5 INPUT時の目安

```text
y=24       ごもじンゴ
y=72       5文字をえらぶ
y=120      [○][○][○][○][○]
y=210      ─────────────────
y=230      案内文
y=270      行選択 または 文字選択
y=580      けす / ぜんぶけす / おまかせ / しらべる
y=654      小さな操作ヒント
```

### 4.6 RESULT時の目安

```text
y=24       ごもじンゴ
y=92       ね こ ぱ ん ち
y=180      ─────────────────
y=208      【ねこぱんち】
y=246      分類
y=282      説明本文
y=586      もういちど / べつのことば
y=646      発見数
```

結果でも入力語は5文字のまま表示する。

---

## 5. スマートフォン入力仕様

### 5.1 二段階入力

全五十音を同時表示しない。

1. 行を選ぶ。
2. その行の文字を選ぶ。

行選択ボタン:

```text
あ  か  さ  た  な
は  ま  や  ら  わ
```

表示は`あ行`などでもよいが、ボタン内が窮屈なら代表文字だけでよい。選択時に上部案内へ`か行`と表示する。

### 5.2 行グループ

候補文字は次のグループを基準とする。

```python
KANA_GROUPS = {
    "あ": ("あ", "い", "う", "え", "お", "ぁ", "ぃ", "ぅ", "ぇ", "ぉ"),
    "か": ("か", "き", "く", "け", "こ", "が", "ぎ", "ぐ", "げ", "ご"),
    "さ": ("さ", "し", "す", "せ", "そ", "ざ", "じ", "ず", "ぜ", "ぞ"),
    "た": ("た", "ち", "つ", "て", "と", "だ", "ぢ", "づ", "で", "ど", "っ"),
    "な": ("な", "に", "ぬ", "ね", "の"),
    "は": ("は", "ひ", "ふ", "へ", "ほ", "ば", "び", "ぶ", "べ", "ぼ",
           "ぱ", "ぴ", "ぷ", "ぺ", "ぽ"),
    "ま": ("ま", "み", "む", "め", "も"),
    "や": ("や", "ゆ", "よ", "ゃ", "ゅ", "ょ"),
    "ら": ("ら", "り", "る", "れ", "ろ"),
    "わ": ("わ", "を", "ん", "ゎ", "ゔ"),
}
```

`は`行は最大15文字なので、5列×3段で表示する。

### 5.3 候補制御

P0では登録語のprefix trieを使う。

例:

```text
登録語:
ねこぱんち
ねこまくら
ねつさまし

入力済み:
ね

有効な次文字:
こ / つ
```

第1階層では、有効文字を一つ以上含む行だけ有効にする。第2階層では、現在のprefixから続けられる文字だけ有効にする。

### 5.4 文字入力

文字ボタンを押した時:

1. 現在スロットへ文字を入れる。
2. 現在位置より後ろのスロットを空にする。
3. 次スロットへ移動する。
4. 5文字未満なら行選択へ戻る。
5. 5文字になったら`しらべる`を有効にする。

### 5.5 スロット再編集

5つのスロットはタップ可能。

- スロットをタップするとカーソルを移動する。
- タップしただけでは既存文字を消さない。
- 新しい文字を入れた時点で、その位置より後ろを空にする。
- これはprefix trieの不変条件を守るためである。

例:

```text
ね こ ぱ ん ち
      ↑ 3文字目を選択
      ↓ 「ま」に変更
ね こ ま ○ ○
```

### 5.6 削除

`けす`:

- 現在位置が入力済みなら、その位置以降を消す。
- 現在位置が空なら、直前の文字を消して一つ戻る。
- 0文字では何もしない。

`ぜんぶけす`:

- 5枠を空にする。
- カーソルを0へ戻す。
- 行選択へ戻す。

長押しに重要操作を依存させない。

### 5.7 おまかせ

- 0文字なら登録語から1件選ぶ。
- 途中入力なら、そのprefixから到達可能な語を選ぶ。
- 後続文字をすべて埋める。
- 将来の保存実装後は未発見語を優先する。
- 直近5語を可能な範囲で避ける。
- 乱数はUI用途でよく、同じ入力から同じ説明を返す不変条件には影響しない。

### 5.8 しらべる

有効条件:

```python
len(word) == 5 and word in content_by_word
```

4文字以下、未登録語、内部不整合では無効。

押下後:

- 6〜24フレーム程度の短い待機を入れてよい。
- すぐ説明パネルへ切り替えてよい。
- 3秒を超える待機は禁止。
- 全画面フラッシュは禁止。

### 5.9 押下フィードバック

タッチ開始時に次のいずれかを2〜4フレーム表示する。

- ボタンを1px下へずらす
- 内枠を明るくする
- 背景と前景を一時的に反転する

スマホではホバー表現へ依存しない。

---

## 6. PC操作

タッチと同じアクション関数を呼び出す。

推奨:

| キー | 動作 |
|---|---|
| 矢印 | フォーカス移動 |
| `Z` / `Enter` | 決定 |
| `X` / `Backspace` | 戻る / 1文字削除 |
| `C` | 全消去 |
| `R` | おまかせ |
| `Space` | P0では未使用、仮ワード切替は削除 |
| `Escape` | 文字選択から行選択へ戻る |

日本語IMEの文字入力へ依存しない。

---

## 7. アプリケーション状態

推奨状態:

```python
class ScreenState(Enum):
    INPUT = auto()
    RESULT = auto()

class InputLayer(Enum):
    ROWS = auto()
    CHARACTERS = auto()
```

P1追加候補:

```python
DICTIONARY
SETTINGS
```

必要な状態値:

```python
@dataclass
class AppState:
    screen: ScreenState
    input_layer: InputLayer
    slots: list[str | None]  # 常に長さ5
    cursor_index: int        # 0..4
    selected_group: str | None
    focused_button: int
    result_entry_id: str | None
    press_feedback_frames: int
```

### 7.1 デバイス非依存アクション

最低限:

```python
select_slot(index: int) -> None
open_kana_group(group_id: str) -> None
select_kana(kana: str) -> None
delete_character() -> None
clear_word() -> None
autofill_word() -> None
confirm_word() -> None
return_to_input(*, clear: bool) -> None
```

タッチ、マウス、キーボードはこれらを呼ぶだけにする。

### 7.2 不変条件

- `slots`は常に5要素。
- 各要素は`None`か許可ひらがな1文字。
- 入力済み部分は常に登録語prefixとして有効。
- 5文字完成時は必ず登録語に一致する。
- 変更したスロットより後ろは空になる。
- RESULTへ入る時は`result_entry_id`が存在する。
- RESULT見出しへ`ンゴ/んご`を追加しない。

---

## 8. 入力候補インデックス

### 8.1 起動時構築

```python
by_id: dict[str, ContentEntry]
by_word: dict[str, ContentEntry]
next_chars_by_prefix: dict[str, tuple[str, ...]]
entry_ids_by_prefix: dict[str, tuple[str, ...]]
```

1000語×5文字なので、起動時に一度構築すれば十分である。毎フレーム再構築しない。

### 8.2 構築例

```python
for entry in entries:
    for index, next_char in enumerate(entry.word):
        prefix = entry.word[:index]
        next_chars_by_prefix[prefix].add(next_char)
        entry_ids_by_prefix[prefix].add(entry.id)
```

### 8.3 文字位置とprefix

再編集時は、カーソルより後ろを候補計算へ含めない。

```python
prefix = "".join(slot for slot in slots[:cursor_index] if slot is not None)
```

### 8.4 並び順

かな候補は辞書データの登録順ではなく、`KANA_GROUPS`の順序で描画する。これによりコンテンツ追加でUI順が変わらない。

---

## 9. RESULT仕様

### 9.1 見出し

正:

```text
【ねこぱんち】
```

誤:

```text
【ねこぱんちンゴ】
ねこぱんち んご
```

### 9.2 表示項目

P0:

1. 入力語
2. 辞書見出し
3. カテゴリ
4. 説明本文
5. `もういちど`
6. `べつのことば`

任意:

- レアリティ
- `NEW`
- 発見数

### 9.3 本文

- JSONの`paragraphs`を順に表示する。
- 段落間に1行相当の余白を置く。
- 日本語を文字幅で折り返す。
- 文字を極端に縮小しない。
- P0の説明は1画面へ収める。
- 同梱データは68〜126文字で構成している。
- 画面内に収まらない時は、開発ビルドで警告を出す。
- P1でページ送りを追加してよい。

### 9.4 文体

説明の基調:

- 擬似辞典
- 擬似Wikipedia
- 観察記録
- 乾いた日常ツッコミ

構成目安:

1. 真面目な定義
2. 具体的な挙動・条件
3. 少し崩す最後の文

`ンゴ`の連発、差別語、攻撃的な内輪ネタは使わない。

### 9.5 結果から戻る

`もういちど`:

- 同じ5文字を残す。
- INPUTへ戻す。
- 任意のスロットを編集できる。

`べつのことば`:

- 5文字を消す。
- INPUTへ戻す。
- カーソルを0へ戻す。

---

## 10. 文字仕様

### 10.1 入力語

- NFC正規化後、Pythonの`len()`でちょうど5。
- 小書き文字も1文字。
- 長音記号は不許可。
- カタカナ、漢字、英数字、記号は不許可。

### 10.2 許可文字

```text
あいうえお
かきくけこ
さしすせそ
たちつてと
なにぬねの
はひふへほ
まみむめも
やゆよ
らりるれろ
わをん

がぎぐげご
ざじずぜぞ
だぢづでど
ばびぶべぼ
ぱぴぷぺぽ
ゔ

ぁぃぅぇぉ
っゃゅょゎ
```

### 10.3 コンテンツ正規化

```python
word = unicodedata.normalize("NFC", raw_word.strip())
```

正規化後に長さと許可文字を検査する。

---

## 11. コンテンツデータ仕様

### 11.1 編集用正本

```text
content/
  schema/
    entry.schema.json
    content_pack.schema.json
  source/
    pack_001.json
    ...
    pack_020.json
  fixtures/
    golden_40.json
  reports/
    content_audit.generated.md
```

- 20パック
- 各50件
- 合計1000件
- ID順
- JSONを正本とする

### 11.2 現在のデータ状態

同梱版:

| status | 件数 | 用途 |
|---|---:|---|
| `reviewed` | 40 | UI、折り返し、操作、初期MVP |
| `draft` | 960 | 1000語規模、入力分岐、制作レビュー用 |
| `approved` | 0 | 公開認定済み |
| 合計 | 1000 | |

重要:

- 1000語すべてに語と説明が存在する。
- ID、語、全文、最終段落の完全重複は0。
- 構造エラーは0。
- 960件は組合せ生成スキャフォールドであり、公開前に個別編集する。
- `reviewed` 40件だけを初期実装の標準ランタイムへ入れる。
- 1000件すべてを試す開発ビルドでは`--include-drafts`を使う。
- 公開時は1000件すべて`approved`が必要。

### 11.3 カテゴリ

| ID | 表示 | 件数 |
|---|---|---:|
| `phenomenon` | 現象 | 160 |
| `condition` | 状態・感情 | 130 |
| `creature` | 生物 | 110 |
| `food` | 食べ物 | 100 |
| `technique` | 技・動作 | 100 |
| `tool` | 道具 | 100 |
| `custom` | 習慣・制度 | 100 |
| `place` | 場所 | 80 |
| `internet` | インターネット | 70 |
| `mystery` | 怪異 | 50 |
| 合計 | | 1000 |

### 11.4 レアリティ

| 値 | 表示候補 | 件数 |
|---:|---|---:|
| 1 | N | 500 |
| 2 | R | 300 |
| 3 | SR | 150 |
| 4 | SSR | 45 |
| 5 | UR | 5 |

レアリティは文章品質ではない。語の奇妙さや発見演出用の装飾値である。

### 11.5 エントリ

```json
{
  "id": "GMG0501",
  "word": "ねこぱんち",
  "category": "technique",
  "rarity": 5,
  "paragraphs": [
    "猫が会話を打ち切る際に使用する、前脚による短い打撃。",
    "威力よりも使用者の態度に意味があり、防御しても関係は改善しない。",
    "なお、二発目から爪が出る場合がある。"
  ],
  "tags": ["猫", "打撃", "意思表示"],
  "tone": "deadpan",
  "ending_family": "manual_cat_punch",
  "status": "reviewed",
  "source_kind": "manual_seed",
  "editor_note": "初期シードとして個別作成・確認済み。"
}
```

### 11.6 必須フィールド

| フィールド | 型 | 条件 |
|---|---|---|
| `id` | string | `GMG0001`形式 |
| `word` | string | NFC後5文字、許可ひらがなのみ |
| `category` | enum | 定義済み10カテゴリ |
| `rarity` | int | 1〜5 |
| `paragraphs` | array[string] | 2〜4件、合計50〜150文字 |
| `tags` | array[string] | 1〜6件、重複なし |
| `tone` | enum | 文体監査用 |
| `ending_family` | string | 重複監査用 |
| `status` | enum | `draft/reviewed/approved/retired` |
| `source_kind` | enum | 生成元 |
| `editor_note` | string | ランタイムへ不要 |

### 11.7 ランタイム生成

```bash
python scripts/validate_content.py

# reviewed 40件
python scripts/build_content.py   --output generated/content_reviewed.py

# draftを含む1000件
python scripts/build_content.py   --include-drafts   --output generated/content_all_drafts.py
```

公開用:

```bash
python scripts/validate_content.py --release
python scripts/build_content.py   --release   --output src/gomoji/generated/content_data.py
```

現状で`--release`が失敗するのは正しい。

---

## 12. コンテンツ文章ガイド

### 12.1 比率

目安:

- 70%: 真面目な辞典・観察記録
- 25%: 日常の具体例
- 5%: 乾いた掲示板風の崩し

作品名だけで十分にネタ感があるため、本文を過剰にふざけさせない。

### 12.2 良い例

```text
【ふとねむい】

作業を始めた直後にだけ、急激な眠気が発生する状態。
休憩中にはほとんど確認されず、締切の一時間前になると自然に治る。

労働との因果関係が強く疑われている。
```

### 12.3 避ける例

```text
ふとねむいンゴ！
眠いンゴねぇ！
これもう寝るしかないンゴ！
```

理由:

- 狙いが前へ出すぎる
- 1000語読むと疲れる
- 語ごとの差が消える
- タイトルの効果が薄れる

### 12.4 禁止内容

- 差別語、属性侮辱
- 実在人物への中傷
- 未成年の性的扱い
- 自傷、自殺を笑いの中心にする内容
- 具体的犯罪手順
- 生々しい暴力、性的、排泄描写
- 医療、法律、金融上の危険な偽情報
- 実在企業、店舗への根拠のない攻撃
- 既存作品の長い台詞、歌詞、コピペ

### 12.5 レビュー手順

各ドラフトで確認する。

1. 語が5文字か。
2. 声に出した時に読めるか。
3. 語から説明を少し想像できるか。
4. 一文目が定義として成立するか。
5. 二文目が一文目を具体化しているか。
6. 最後が同じ定型句へ偏っていないか。
7. 画面へ収まるか。
8. 他エントリと説明が似すぎていないか。
9. 不快さだけで笑いを取っていないか。
10. `ンゴ`を無理に足していないか。

---

## 13. データ検証

同梱`validate_content.py`は少なくとも次を検査する。

- 20パック×50件
- schema version
- ID形式、連番、順序
- ID重複
- 語重複
- NFC
- 5文字
- 許可文字
- カテゴリ
- レアリティ
- 段落数
- 説明合計文字数
- 空段落
- タグ
- tone
- ending_family
- status
- source_kind
- 説明全文重複
- 最終段落重複
- カテゴリ配分
- レアリティ配分
- release時の1000 approved

監査:

```bash
python scripts/audit_content.py
```

監査レポートには類似説明候補を含める。現在の960ドラフトは組合せ構造のため高類似候補が存在する。これは想定内であり、公開前レビューキューとして使う。

---

## 14. ローカル版とWeb版

### 14.1 現状の問題

現行Pagesでは`web_bootstrap.py`から`src/gomoji/app.py`のpackage importが失敗した経緯があり、Web側が自己完結ファイルになっている。

### 14.2 最終方針

**手作業による二重実装は禁止。**

優先案:

1. `src/gomoji/`を正本にする。
2. ビルドスクリプトでWeb用単一ファイルを生成する。
3. `web_bootstrap.py`を生成物として扱う。
4. GitHub Actionsで生成・差分確認する。

代替案:

- Pyxel Web上で安全にpackage importできる構成が確認できた場合だけ、共通module importへ移行する。

### 14.3 生成対象

Web用単一ファイルには少なくとも次を含める。

- 共有状態モデル
- UIレイアウト
- 入力処理
- prefix trie
- reviewedコンテンツ
- 日本語フォントパス
- 起動処理

`content_all_drafts.py`を本番Pagesへ含めない。

### 14.4 CI

推奨:

```bash
python scripts/validate_content.py
python scripts/build_content.py --output generated/content_reviewed.py
python scripts/build_content.py --check --output generated/content_reviewed.py
python scripts/build_web_bootstrap.py
python scripts/build_web_bootstrap.py --check
pytest -q
ruff check .
```

---

## 15. コード構成案

既存構成を尊重しつつ、次を目安とする。

```text
src/gomoji/
  app.py
  config.py
  state.py
  content.py
  input_model.py
  trie.py
  ui/
    geometry.py
    buttons.py
    input_screen.py
    result_screen.py
    text_layout.py
  generated/
    content_data.py

content/
  schema/
  source/
  fixtures/
  reports/

scripts/
  validate_content.py
  audit_content.py
  build_content.py
  build_web_bootstrap.py
```

過度に細分化しない。小規模作品として、一つの責務が明確になる範囲で分ける。

---

## 16. UI部品

### 16.1 Rect

```python
@dataclass(frozen=True, slots=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

    def contains(self, px: int, py: int) -> bool:
        return (
            self.x <= px < self.x + self.w
            and self.y <= py < self.y + self.h
        )
```

### 16.2 Button

```python
@dataclass(slots=True)
class Button:
    id: str
    rect: Rect
    label: str
    enabled: bool = True
    pressed_frames: int = 0
```

### 16.3 タッチ処理

- フレームごとに表示中ボタン一覧を作る。
- pointer downで一件だけhitさせる。
- disabledはactionを発火しない。
- ボタンactionは文字列分岐より、可能なら明示的なcommandへする。
- 描画用rectとhit rectを分けてもよい。

---

## 17. 日本語折り返し

### 17.1 要件

- BDFフォントの実幅を使う。
- 空白がなくても1文字単位で折り返す。
- 段落境界を維持する。
- 句読点を極端に行頭へ置かない。
- 結果をキャッシュしてよい。

### 17.2 禁則

最低限:

```text
行頭へ置かない:
、。！？）」』】〕〉》・：；

行末へ置かない:
（「『【〔〈《
```

### 17.3 テスト

- 句読点
- かぎ括弧
- 小書き文字
- reviewed 40件
- 最長126文字
- 396px画面の本文領域

---

## 18. 保存と辞典

P0の入力・結果を阻害しないよう、保存と辞典は次ウェーブでよい。

### 18.1 保存候補

```json
{
  "schema_version": 1,
  "content_revision": "sha256:...",
  "discovered_ids": ["GMG0001"],
  "favorite_ids": [],
  "recent_ids": ["GMG0001"],
  "total_lookups": 1,
  "sound_enabled": true
}
```

### 18.2 保存抽象化

```python
class SaveRepository(Protocol):
    def load(self) -> SaveData: ...
    def save(self, data: SaveData) -> None: ...
```

ネイティブとWebの保存先差異をこの層へ閉じ込める。具体APIは現行Pyxel 2.9.9とPages環境をCodexが確認して決める。

### 18.3 辞典

P1:

- 発見済みだけ表示
- 未発見は`？？？？？`
- お気に入り
- カテゴリフィルタ
- 結果詳細の再表示

---

## 19. サウンド

P1でよい。

候補:

- 文字入力: 短いクリック
- 行選択: 低めのクリック
- 削除: 乾いた音
- 決定: 二音
- NEW: 短い上昇音

説明文を邪魔するBGMは不要。無音でも成立すること。

---

## 20. テスト仕様

### 20.1 状態

- 初期スロットは5つ空
- 初期カーソル0
- 行選択
- 有効文字入力
- 無効文字を入力できない
- 入力後にカーソルが進む
- 5文字目でconfirm有効
- 4文字以下でconfirm無効
- スロット再選択
- 中間文字変更で後続が消える
- `けす`
- `ぜんぶけす`
- `おまかせ`
- RESULT遷移
- INPUT復帰

### 20.2 trie

- 空prefixの候補
- 1〜4文字prefix
- 不明prefixは空
- 5文字完成時にby_word一致
- 発見状態で候補が変わらない
- 重複語を受け入れない

### 20.3 タッチ

- 境界内
- 境界外
- 隣接ボタンの重複なし
- disabled
- 下部セーフマージン
- 396×696で全主要ボタンが画面内

### 20.4 「固定ンゴ」回帰防止

最低限:

```python
assert format_result_heading("ねこぱんち") == "【ねこぱんち】"
assert format_slot_text("ねこぱんち") == "ね こ ぱ ん ち"
```

次を禁止:

```python
"ねこぱんちンゴ"
"ねこぱんちんご"
```

プロダクトタイトル`ごもじンゴ`だけは許可する。

### 20.5 コンテンツ

同梱`tests/test_content_contract.py`を移植または利用する。

### 20.6 Webスモーク

- `index.html` 200
- `web_bootstrap.py` 200
- BDF 200
- iPhone縦画面で起動
- タップ入力
- 5文字確定
- 説明表示
- 戻る
- 横スクロールなし
- Safari UIと主要操作が干渉しない

---

## 21. パフォーマンス

目標:

- 30 FPS
- 起動時索引構築は一度
- 毎フレームJSON解析をしない
- 毎フレーム全1000件を走査しない
- 折り返し結果をentry ID単位でキャッシュ可能
- Web本番へ960 draftを含めない
- 文字ボタンのRectを毎フレーム大量生成せず、レイアウト変更時に再構築してよい

1000語×5文字のtrieは小規模であり、複雑な最適化は不要。

---

## 22. 実装ロードマップ

## GMG000 — 基盤

現状ほぼ完了。

- Pyxel scaffold
- 396×696
- 日本語BDF
- Pages
- テスト
- ruff
- 仮スロット画面

## GMG001 — 仕様・コンテンツ基盤導入

- 本仕様を`docs/`へ配置
- `content/`導入
- validator
- audit
- build_content
- reviewed 40件生成
- 既存テスト維持

完了条件:

```bash
python scripts/validate_content.py
python scripts/build_content.py --output src/gomoji/generated/content_data.py
pytest -q
ruff check .
```

## GMG002 — スマートフォン5文字入力

- 5スロット
- スロットタップ
- 行選択
- 文字選択
- 濁音、半濁音、小字
- 削除
- 全消去
- おまかせ
- 押下フィードバック
- PC操作
- prefix trie

## GMG003 — 結果パネル

- 確定
- 短い切替
- 見出し
- カテゴリ
- 本文
- 折り返し
- もういちど
- べつのことば
- 固定ンゴ回帰テスト

## GMG004 — Web共通化

- ローカルを正本化
- Web用単一ファイル生成
- 手編集重複の解消
- Pages workflowへ`--check`
- iPhone実機確認

## GMG005 — 発見保存・辞典

- discovered
- recent
- favorite
- save repository
- 辞典
- NEW

## GMG006 — 1000語開発ビルド

- `--include-drafts`
- 1000語trie
- 入力分岐確認
- 画面オーバーフロー監査
- 類似度レビューキュー

## GMG007 — コンテンツ編集

- 960 draftを個別レビュー
- `reviewed`
- 最終校正
- `approved`
- 1000 approved
- 類似説明の解消
- 不快表現監査

## GMG008 — 公開監査

- `validate_content.py --release`
- 1000 approved
- Pages
- iPhone
- PC
- README
- credits
- font license
- release tag

---

## 23. GMG001の具体的作業指示

Codexへ最初に渡す作業範囲はGMG001だけとする。

1. リポジトリ全体を確認。
2. 同梱`content/`, `scripts/`, `tests/`を現行構成へ適合させる。
3. 既存の`src/gomoji`パッケージ名を維持。
4. `generated/content_data.py`をreviewed 40件で生成。
5. ローカルアプリが生成コンテンツをimportできることを確認。
6. 仮ワード配列を、reviewedコンテンツ由来へ置換してよい。
7. スマホ入力UIはまだ実装しない。
8. Web版を壊さない。
9. README、ロードマップ、handoffが存在するなら更新。
10. コミット前にpytest、ruff、headless smokeを実行。

---

## 24. 完成受入条件

P0完成:

- iPhone縦画面で5文字をタップ入力できる。
- 濁音、半濁音、小書き文字を入力できる。
- 登録語へ必ず到達できる。
- 途中修正できる。
- 削除、全消去、おまかせが動く。
- 5文字で説明が表示される。
- 結果へ固定`んご/ンゴ`が付かない。
- 40 reviewed語で全文が画面へ収まる。
- ローカルとPagesが同じゲームロジックを使う。
- pytest、ruff、content validationが通る。
- iPhone Safariで主要ボタンを指で押せる。
- 横スクロールしない。
- 作業ツリーがclean。
- READMEと仕様が実装に一致する。

初回公開完成:

- 1000 approved
- `validate_content.py --release`成功
- 重複0
- 類似説明の目視確認
- 不快表現監査
- フォントライセンス
- Pages実機確認
- リリースタグ

---

## 25. Codex完了報告テンプレート

```text
## 実装タスク
GMG00X

## 実装内容
- ...

## 主な変更ファイル
- ...

## コンテンツ
- source:
- draft:
- reviewed:
- approved:
- generated:

## 検証
- pytest:
- ruff:
- content validation:
- build --check:
- headless smoke:
- Pages:

## スマホ確認
- 端末:
- ブラウザ:
- タップ:
- 横スクロール:
- Safari UI干渉:

## 固定ンゴ回帰確認
- スロット:
- 結果見出し:
- 説明定型文:

## 既知の問題
- ...

## 次の推奨タスク
- ...
```

---

## 26. 最終判断

迷った場合は次を優先する。

1. 説明文が読みやすい。
2. 指で押しやすい。
3. 5文字を直しやすい。
4. 既存Pagesを壊さない。
5. ローカルとWebを二重管理しない。
6. 1000語をコードから独立して編集できる。
7. タイトル以外へ`ンゴ`を足さない。
8. 面白さを説明しすぎない。
