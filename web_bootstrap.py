# title: ごもじンゴ
# author: sejiseji
# desc: Pyxel project scaffold for Gomoji
# site: https://github.com/sejiseji/gomoji
# license: MIT
# version: 0.3.0

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto

WINDOW_TITLE = "ごもじンゴ"
SCREEN_WIDTH = 396
SCREEN_HEIGHT = 696
FPS = 30
FONT_PATH = "assets/umplus_j12r.bdf"

BACKGROUND_COLOR = 0
TEXT_COLOR = 7
ACCENT_COLOR = 10
SHADOW_COLOR = 1
DEBUG_COLOR = 13
GRID_COLOR = 5
ACTIVE_COLOR = 11
LOCKED_COLOR = 3

WORD_LENGTH = 5
DEFAULT_REVEAL_FRAMES = 12
RESULT_WRAP_CHARS = 25
RESULT_TEXT_TOP = 282
KANA_GROUPS = {
    "あ": ("あ", "い", "う", "え", "お", "ぁ", "ぃ", "ぅ", "ぇ", "ぉ"),
    "か": ("か", "き", "く", "け", "こ", "が", "ぎ", "ぐ", "げ", "ご"),
    "さ": ("さ", "し", "す", "せ", "そ", "ざ", "じ", "ず", "ぜ", "ぞ"),
    "た": ("た", "ち", "つ", "て", "と", "だ", "ぢ", "づ", "で", "ど", "っ"),
    "な": ("な", "に", "ぬ", "ね", "の"),
    "は": (
        "は",
        "ひ",
        "ふ",
        "へ",
        "ほ",
        "ば",
        "び",
        "ぶ",
        "べ",
        "ぼ",
        "ぱ",
        "ぴ",
        "ぷ",
        "ぺ",
        "ぽ",
    ),
    "ま": ("ま", "み", "む", "め", "も"),
    "や": ("や", "ゆ", "よ", "ゃ", "ゅ", "ょ"),
    "ら": ("ら", "り", "る", "れ", "ろ"),
    "わ": ("わ", "を", "ん", "ゎ", "ゔ"),
}

# BEGIN GENERATED ENTRIES
ENTRIES = (
    {
        "id": 'GMG0001',
        "word": 'あめしらせ',
        "category": '現象',
        "rarity": 3,
        "paragraphs": (
            '雨が降る少し前に、なぜか洗濯物を外へ出したくなる現象。',
            '空模様を見た本人は「まだいける」と判断するが、その判断まで含めて発生条件とされる。',
            'なお、取り込んだ直後に晴れる場合も同じ現象へ含まれる。',
        ),
    },
    {
        "id": 'GMG0012',
        "word": 'ちょいずれ',
        "category": '現象',
        "rarity": 2,
        "paragraphs": (
            '時刻、位置、会話の意図などが、困らない程度に少しだけ食い違う現象。',
            '一つずつ直すと別の箇所がずれるため、最終的には全員が気づかないふりをする。',
            '大事故にはならないが、地味に一日を削ってくる。',
        ),
    },
    {
        "id": 'GMG0023',
        "word": 'すっぽぬけ',
        "category": '現象',
        "rarity": 5,
        "paragraphs": (
            '確実に覚えていたはずの情報だけが、必要な瞬間に抜け落ちる現象。',
            '人名、暗証番号、買う物の三種で特に起こりやすく、用事が終わると自然に戻る。',
            '記憶力の問題ではない。タイミングの性格が悪いだけである。',
        ),
    },
    {
        "id": 'GMG0034',
        "word": 'ぴゅうかぜ',
        "category": '現象',
        "rarity": 4,
        "paragraphs": (
            '窓を閉めた直後に限って、部屋へ入り込もうとする細い風。',
            '紙だけを選んで動かす性質があり、重い物には一切関心を示さない。',
            '換気には役立たないが、机の上の秩序は壊す。',
        ),
    },
    {
        "id": 'GMG0172',
        "word": 'ふとねむい',
        "category": '状態・感情',
        "rarity": 3,
        "paragraphs": (
            '作業を始めた直後にだけ、急激な眠気が発生する状態。',
            '休憩中にはほとんど確認されず、締切の一時間前になると自然に治る。',
            '労働との因果関係が強く疑われている。',
        ),
    },
    {
        "id": 'GMG0183',
        "word": 'しょんぼり',
        "category": '状態・感情',
        "rarity": 2,
        "paragraphs": (
            '期待していた結果が出なかった時、肩だけが先に納得する状態。',
            '本人は平気だと主張できるが、姿勢がすべて説明してしまう。',
            '甘い物で一時的に改善するとの報告が多い。',
        ),
    },
    {
        "id": 'GMG0194',
        "word": 'ちょいねむ',
        "category": '状態・感情',
        "rarity": 2,
        "paragraphs": (
            '眠るほどではないが、起きていると断言するのも難しい状態。',
            '返事は可能でも内容が保存されないため、重要な相談には向かない。',
            '五分だけ休むという宣言から長編化しやすい。',
        ),
    },
    {
        "id": 'GMG0205',
        "word": 'ぐっとくる',
        "category": '状態・感情',
        "rarity": 5,
        "paragraphs": (
            '説明できない何かが胸の内側へ届き、数秒だけ言葉が遅れる状態。',
            '感動、懐かしさ、悔しさのどれでも起こるため、本人にも分類が難しい。',
            'とりあえず黙ってうなずくのが一般的な対処法である。',
        ),
    },
    {
        "id": 'GMG0291',
        "word": 'ねこもどき',
        "category": '生物',
        "rarity": 1,
        "paragraphs": (
            '猫に似た姿と態度を持つが、猫として重要な部分が少しずつ足りない生物。',
            '箱には入るものの収まりが悪く、呼んでも来ない点だけは本物に近い。',
            '専門家は猫ではないとしている。本人は特に気にしていない。',
        ),
    },
    {
        "id": 'GMG0302',
        "word": 'ぴょこたん',
        "category": '生物',
        "rarity": 5,
        "paragraphs": (
            '物陰から頭だけを出し、周囲の安全を何度も確認する小型生物。',
            '全身を見たという報告は少なく、頭部だけで生活している説もある。',
            '近づくと引っ込むため、観察は永遠に最初からやり直しになる。',
        ),
    },
    {
        "id": 'GMG0313',
        "word": 'にゃんこえ',
        "category": '生物',
        "rarity": 1,
        "paragraphs": (
            '姿は見えないが、猫らしい声だけで存在を主張する生物。',
            '返事をすると別の方向から鳴くため、位置の特定には向かない。',
            '餌袋の音を出した時だけ、急に実体を持つ。',
        ),
    },
    {
        "id": 'GMG0324',
        "word": 'ぎょろみる',
        "category": '生物',
        "rarity": 1,
        "paragraphs": (
            '目だけを大きく動かし、体を一切向けずに周囲を観察する生物。',
            '警戒しているように見えるが、実際にはだいたい退屈している。',
            'こちらが見返すと、なぜか見ていなかった顔をする。',
        ),
    },
    {
        "id": 'GMG0403',
        "word": 'もちあぶり',
        "category": '食べ物',
        "rarity": 1,
        "paragraphs": (
            '餅の表面だけを慎重に炙り、中身の危険性を残した料理。',
            '香ばしさは増すが伸びる力も増すため、食べる側にも技術が求められる。',
            '急ぐ理由がある日は選ばないほうがよい。',
        ),
    },
    {
        "id": 'GMG0412',
        "word": 'がっつめし',
        "category": '食べ物',
        "rarity": 4,
        "paragraphs": (
            '量の説明を省き、見た目の圧だけで満腹を予告する食事。',
            '食べ始めは勢いがあるが、中盤から箸と相談する時間が増える。',
            '完食より、注文した時の覚悟が評価される。',
        ),
    },
    {
        "id": 'GMG0423',
        "word": 'ふっくらめ',
        "category": '食べ物',
        "rarity": 1,
        "paragraphs": (
            '通常より少しだけ厚く、柔らかく仕上げる調理上の加減。',
            '数値で指定できないため、作る側の自信と食べる側の好意で成立する。',
            '失敗しても「ふっくらめ」と言えば説明としては丸い。',
        ),
    },
    {
        "id": 'GMG0434',
        "word": 'ぴりっから',
        "category": '食べ物',
        "rarity": 2,
        "paragraphs": (
            '辛いと言い切るほどではない刺激を、最後まで舌へ残す味付け。',
            '最初の一口では油断させ、二口目から飲み物の位置を確認させる。',
            '子ども向けかどうかは、作った人の自己申告による。',
        ),
    },
    {
        "id": 'GMG0501',
        "word": 'ねこぱんち',
        "category": '技・動作',
        "rarity": 5,
        "paragraphs": (
            '猫が会話を打ち切る際に使用する、前脚による短い打撃。',
            '威力よりも使用者の態度に意味があり、防御しても関係は改善しない。',
            'なお、二発目から爪が出る場合がある。',
        ),
    },
    {
        "id": 'GMG0512',
        "word": 'ひょいよけ',
        "category": '技・動作',
        "rarity": 2,
        "paragraphs": (
            '大げさに構えず、半歩だけ位置を変えて問題を避ける技。',
            '身体への負担は少ないが、避けた問題が後ろの人へ届く欠点がある。',
            '使用後は一度だけ振り返るのが礼儀とされる。',
        ),
    },
    {
        "id": 'GMG0523',
        "word": 'きゅっとめ',
        "category": '技・動作',
        "rarity": 3,
        "paragraphs": (
            '広がりかけた物事を、最小限の動きで一度だけ締める技。',
            '袋、話題、口元などに応用できるが、締めすぎると別の問題になる。',
            '力加減は経験ではなく、その場の空気で決まる。',
        ),
    },
    {
        "id": 'GMG0534',
        "word": 'しょいこみ',
        "category": '技・動作',
        "rarity": 2,
        "paragraphs": (
            '本来は複数人で持つべき役割を、一人で背負って進める動作。',
            '開始直後は頼もしく見えるが、途中から周囲が声をかけにくくなる。',
            '技というより癖であり、解除には他人の強制参加が必要である。',
        ),
    },
    {
        "id": 'GMG0601',
        "word": 'かみつまみ',
        "category": '道具',
        "rarity": 1,
        "paragraphs": (
            '机へ平らに張りついた紙の角だけを持ち上げるための小さな道具。',
            '爪で取れば済む場面でも使えるため、導入理由は主に気分である。',
            'なくした時に限って必要性を強く感じる。',
        ),
    },
    {
        "id": 'GMG0612',
        "word": 'ちょんおき',
        "category": '道具',
        "rarity": 2,
        "paragraphs": (
            '小物を一時的に置いたという事実だけを記録する台。',
            '定位置ではないため、数分後には置いた本人も場所を説明できない。',
            '整理用品として売られているが、散らかりの中継地点になりやすい。',
        ),
    },
    {
        "id": 'GMG0623',
        "word": 'ぴたっとめ',
        "category": '道具',
        "rarity": 4,
        "paragraphs": (
            '扉や紙などを、閉じ切らず開き切らずの位置で固定する道具。',
            '便利な角度は毎回違うため、製品より使う人の勘が重要になる。',
            '外した後の置き場所までは固定してくれない。',
        ),
    },
    {
        "id": 'GMG0634',
        "word": 'ぎゅうおし',
        "category": '道具',
        "rarity": 1,
        "paragraphs": (
            '蓋や荷物を、理屈ではなく面積と体重で押し込むための補助具。',
            '正しい使用法では少しずつ圧をかけるが、実際は一度に使われる。',
            '閉まった場合は成功、開かなくなった場合は別件である。',
        ),
    },
    {
        "id": 'GMG0701',
        "word": 'あさまつり',
        "category": '習慣・制度',
        "rarity": 1,
        "paragraphs": (
            '朝早く起きた事実を、必要以上に前向きな出来事として扱う小さな祭り。',
            '参加者は主に本人一人で、温かい飲み物を用意した時点で成立する。',
            '二度寝した場合は昼の部へ自動的に延期される。',
        ),
    },
    {
        "id": 'GMG0712',
        "word": 'ちょいまつ',
        "category": '習慣・制度',
        "rarity": 3,
        "paragraphs": (
            'すぐ戻るという言葉を信じ、予定より少し長く待つ習慣。',
            '待つ側は五分を想定し、待たせる側は時間を具体的に想定していない。',
            '両者の「ちょい」が一致した例は少ない。',
        ),
    },
    {
        "id": 'GMG0723',
        "word": 'きゅうやす',
        "category": '習慣・制度',
        "rarity": 1,
        "paragraphs": (
            '休む予定を立てず、その場の疲労だけを根拠に始める休止制度。',
            '開始は早いが終了条件が曖昧で、気づくと別の娯楽へ移行している。',
            '休憩としては正しい。計画としてはかなり弱い。',
        ),
    },
    {
        "id": 'GMG0734',
        "word": 'まったなし',
        "category": '習慣・制度',
        "rarity": 2,
        "paragraphs": (
            '先送りを重ねた結果、検討時間が完全に消えた状態で始まる慣習。',
            '関係者は以前から分かっていた顔をするが、準備物はだいたい足りない。',
            '緊張感だけは予定どおり到着する。',
        ),
    },
    {
        "id": 'GMG0803',
        "word": 'そらこみち',
        "category": '場所',
        "rarity": 3,
        "paragraphs": (
            '空を見上げたまま歩くと、一度だけ入り込めるとされる細い道。',
            '地図上では普通の路地だが、通行中だけ建物の高さが少し遠ざかる。',
            '出口へ着くころには、何を探していたか忘れている。',
        ),
    },
    {
        "id": 'GMG0812',
        "word": 'ちょいみち',
        "category": '場所',
        "rarity": 1,
        "paragraphs": (
            '近道のつもりで選ばれ、結果として少しだけ遠回りになる道。',
            '景色は悪くないため、案内した側は失敗を認めず散歩だったことにする。',
            '急いでいない日に限れば、かなり良い道である。',
        ),
    },
    {
        "id": 'GMG0823',
        "word": 'きゃくまち',
        "category": '場所',
        "rarity": 2,
        "paragraphs": (
            '誰かを迎えるために立つ場所が、待つ人の数だけ少しずつ移動した区域。',
            '駅前、玄関、店先などに発生し、正しい位置は相手が現れた後で判明する。',
            '目印を伝え合うほど互いに動くので、収束には時間がかかる。',
        ),
    },
    {
        "id": 'GMG0834',
        "word": 'ひょいまち',
        "category": '場所',
        "rarity": 1,
        "paragraphs": (
            '曲がり角を一つ越えただけで、知らない町へ入った気がする場所。',
            '実際の距離は短いが、看板と匂いが急に変わるため帰り道が長く感じる。',
            '写真を撮ると、だいたいいつもの町に戻る。',
        ),
    },
    {
        "id": 'GMG0881',
        "word": 'れすまわし',
        "category": 'インターネット',
        "rarity": 1,
        "paragraphs": (
            '一つの返信を別の話題へ持ち運び、少しずつ意味を変えていく行為。',
            '引用が増えるほど最初の発言は見えにくくなり、最後には語尾だけが残る。',
            '誰が始めたかは、だいたい全員が別の人だと思っている。',
        ),
    },
    {
        "id": 'GMG0892',
        "word": 'しゃべりて',
        "category": 'インターネット',
        "rarity": 1,
        "paragraphs": (
            '内容より先に会話へ参加し、流れを止めないことを役割とする人。',
            '詳しくなくても反応は速く、沈黙が続く場面では意外と重宝される。',
            '情報の正確さは、後から来る人へ委ねられる。',
        ),
    },
    {
        "id": 'GMG0903',
        "word": 'こめぴたっ',
        "category": 'インターネット',
        "rarity": 1,
        "paragraphs": (
            'コメント欄の流れが、特定の一言を境に突然止まる現象。',
            '強い反論より、返し方の分からない正論や妙に具体的な体験談で起こりやすい。',
            '止めた本人だけは、まだ通知を待っている。',
        ),
    },
    {
        "id": 'GMG0914',
        "word": 'ねたちょい',
        "category": 'インターネット',
        "rarity": 1,
        "paragraphs": (
            '完成していない話題を少しだけ出し、周囲の反応で続きを決める投稿形式。',
            '反応が良ければ予告だったことになり、悪ければ独り言だったことになる。',
            '撤退経路まで含めて一つの技法である。',
        ),
    },
    {
        "id": 'GMG0951',
        "word": 'かげわらい',
        "category": '怪異',
        "rarity": 5,
        "paragraphs": (
            '人が笑っていない時に、その影だけが口元を緩める怪異。',
            '日差しの強い場所ほど見つけやすいが、確認のため振り返ると普通の形へ戻る。',
            '害はない。ただし、同じ冗談を二度言う必要もない。',
        ),
    },
    {
        "id": 'GMG0962',
        "word": 'ゆめぴたっ',
        "category": '怪異',
        "rarity": 1,
        "paragraphs": (
            '夢の途中で景色も音も完全に止まり、自分だけが数歩動ける現象。',
            '止まった人物へ触れると目が覚めるため、詳しい調査は毎回そこで終わる。',
            '続きを見ようとして二度寝しても、別番組になる。',
        ),
    },
    {
        "id": 'GMG0973',
        "word": 'こえしゅん',
        "category": '怪異',
        "rarity": 2,
        "paragraphs": (
            '誰かに呼ばれた気がした直後、周囲の音が一瞬だけ遠ざかる現象。',
            '名前を知っている声にも知らない声にも聞こえるため、聞き分けはできない。',
            '返事をしなければ終わる。返事をしても、たぶん終わる。',
        ),
    },
    {
        "id": 'GMG0984',
        "word": 'まどのぞき',
        "category": '怪異',
        "rarity": 2,
        "paragraphs": (
            '夜の窓へ近づいた時、室内ではなく別の部屋が一瞬だけ映る怪異。',
            '家具の配置は似ているが、こちらにない物が一つだけ置かれている。',
            '確認のため照明を消す行為は推奨されない。普通に怖い。',
        ),
    },
)
# END GENERATED ENTRIES

BY_WORD = {entry["word"]: entry for entry in ENTRIES}
BY_ID = {entry["id"]: entry for entry in ENTRIES}


def all_kana():
    return tuple(kana for group in KANA_GROUPS.values() for kana in group)


def build_index():
    next_chars = defaultdict(set)
    entry_ids = defaultdict(list)
    for entry in ENTRIES:
        for index, next_char in enumerate(entry["word"]):
            prefix = entry["word"][:index]
            next_chars[prefix].add(next_char)
            entry_ids[prefix].append(entry["id"])
        entry_ids[entry["word"]].append(entry["id"])

    ordered_next = {
        prefix: tuple(kana for kana in all_kana() if kana in chars)
        for prefix, chars in next_chars.items()
    }
    return ordered_next, {prefix: tuple(ids) for prefix, ids in entry_ids.items()}


NEXT_CHARS_BY_PREFIX, ENTRY_IDS_BY_PREFIX = build_index()


class ScreenState(Enum):
    INPUT = auto()
    REVEAL = auto()
    RESULT = auto()


class InputLayer(Enum):
    ROWS = auto()
    CHARACTERS = auto()


@dataclass
class Button:
    x: int
    y: int
    width: int
    height: int
    label: str
    action: str
    value: str | int | None = None
    enabled: bool = True


@dataclass
class WebState:
    screen: ScreenState = ScreenState.INPUT
    input_layer: InputLayer = InputLayer.ROWS
    slots: list[str | None] = field(default_factory=lambda: [None] * WORD_LENGTH)
    cursor_index: int = 0
    selected_group: str | None = None
    focused_button: int = 0
    result_entry_id: str | None = None
    pending_result_entry_id: str | None = None
    result_is_new: bool = False
    reveal_frames_remaining: int = 0
    discovered_entry_ids: set[str] = field(default_factory=set)

    @property
    def word(self):
        return "".join(slot or "" for slot in self.slots)

    @property
    def result_entry(self):
        if self.result_entry_id is None:
            return None
        return BY_ID.get(self.result_entry_id)

    @property
    def found_count(self):
        return len(self.discovered_entry_ids)

    def prefix_for_cursor(self):
        return "".join(slot or "" for slot in self.slots[: self.cursor_index])

    def filled_prefix(self):
        letters = []
        for slot in self.slots:
            if slot is None:
                break
            letters.append(slot)
        return "".join(letters)

    def valid_next_chars(self):
        return NEXT_CHARS_BY_PREFIX.get(self.prefix_for_cursor(), ())

    def enabled_groups(self):
        valid = set(self.valid_next_chars())
        return tuple(
            group_id
            for group_id, chars in KANA_GROUPS.items()
            if any(kana in valid for kana in chars)
        )

    def enabled_kana(self):
        if self.selected_group is None:
            return ()
        valid = set(self.valid_next_chars())
        return tuple(kana for kana in KANA_GROUPS[self.selected_group] if kana in valid)

    def can_confirm(self):
        return len(self.word) == WORD_LENGTH and self.word in BY_WORD

    def select_slot(self, index):
        self.cursor_index = max(0, min(WORD_LENGTH - 1, index))
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.focused_button = 0

    def open_kana_group(self, group_id):
        if group_id not in self.enabled_groups():
            return
        self.selected_group = group_id
        self.input_layer = InputLayer.CHARACTERS
        self.focused_button = 0

    def select_kana(self, kana):
        if kana not in self.enabled_kana():
            return
        self.slots[self.cursor_index] = kana
        for index in range(self.cursor_index + 1, WORD_LENGTH):
            self.slots[index] = None
        if self.cursor_index < WORD_LENGTH - 1:
            self.cursor_index += 1
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.focused_button = 0

    def delete_character(self):
        if self.slots[self.cursor_index] is not None:
            for index in range(self.cursor_index, WORD_LENGTH):
                self.slots[index] = None
        elif self.cursor_index > 0:
            self.cursor_index -= 1
            for index in range(self.cursor_index, WORD_LENGTH):
                self.slots[index] = None
        self.input_layer = InputLayer.ROWS
        self.selected_group = None

    def clear_word(self):
        self.slots = [None] * WORD_LENGTH
        self.cursor_index = 0
        self.input_layer = InputLayer.ROWS
        self.selected_group = None
        self.result_entry_id = None
        self.pending_result_entry_id = None

    def autofill_word(self):
        candidate_ids = list(ENTRY_IDS_BY_PREFIX.get(self.filled_prefix(), ()))
        if not candidate_ids:
            return
        entry = BY_ID[random.choice(candidate_ids)]
        self.slots = list(entry["word"])
        self.cursor_index = WORD_LENGTH - 1
        self.input_layer = InputLayer.ROWS
        self.selected_group = None

    def confirm_word(self):
        if not self.can_confirm():
            return
        entry_id = BY_WORD[self.word]["id"]
        self.pending_result_entry_id = entry_id
        self.result_entry_id = None
        self.result_is_new = entry_id not in self.discovered_entry_ids
        self.screen = ScreenState.REVEAL
        self.reveal_frames_remaining = DEFAULT_REVEAL_FRAMES
        self.input_layer = InputLayer.ROWS
        self.selected_group = None

    def tick_reveal(self):
        if self.screen != ScreenState.REVEAL:
            return
        if self.reveal_frames_remaining > 0:
            self.reveal_frames_remaining -= 1
        if self.reveal_frames_remaining <= 0:
            self.finish_reveal()

    def finish_reveal(self):
        if self.pending_result_entry_id is None:
            self.return_to_input(True)
            return
        self.result_entry_id = self.pending_result_entry_id
        self.pending_result_entry_id = None
        self.discovered_entry_ids.add(self.result_entry_id)
        self.screen = ScreenState.RESULT
        self.focused_button = 0

    def return_to_input(self, clear):
        self.screen = ScreenState.INPUT
        self.result_entry_id = None
        self.pending_result_entry_id = None
        self.reveal_frames_remaining = 0
        if clear:
            self.clear_word()
        else:
            self.input_layer = InputLayer.ROWS
            self.selected_group = None


class GomojiWebApp:
    def __init__(self):
        import pyxel

        self.pyxel = pyxel
        self.state = WebState()
        self.buttons = []
        self.font = None
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=WINDOW_TITLE, fps=FPS)
        self.font = pyxel.Font(FONT_PATH)
        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel = self.pyxel
        if self.state.screen == ScreenState.REVEAL:
            mouse_button = getattr(pyxel, "MOUSE_BUTTON_LEFT", 0)
            if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(mouse_button):
                self.state.finish_reveal()
            else:
                self.state.tick_reveal()
            return

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            if self.state.input_layer == InputLayer.CHARACTERS:
                self.state.input_layer = InputLayer.ROWS
                self.state.selected_group = None
            return
        if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.state.delete_character()
        if pyxel.btnp(pyxel.KEY_C):
            self.state.clear_word()
        if pyxel.btnp(pyxel.KEY_R):
            self.state.autofill_word()
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.move_focus(-1, 0)
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.move_focus(1, 0)
        if pyxel.btnp(pyxel.KEY_UP):
            self.move_focus(0, -1)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.move_focus(0, 1)
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN):
            self.activate_focused_button()

        mouse_button = getattr(pyxel, "MOUSE_BUTTON_LEFT", 0)
        if pyxel.btnp(mouse_button):
            self.activate_button_at(pyxel.mouse_x, pyxel.mouse_y)

    def draw(self):
        self.pyxel.cls(BACKGROUND_COLOR)
        self.buttons = []
        if self.state.screen == ScreenState.REVEAL:
            self.draw_reveal()
        elif self.state.screen == ScreenState.RESULT:
            self.draw_result()
        else:
            self.draw_input()

    def draw_reveal(self):
        pyxel = self.pyxel
        center_x = SCREEN_WIDTH // 2
        pulse = self.state.reveal_frames_remaining % 6
        pyxel.rectb(16, 18, SCREEN_WIDTH - 32, SCREEN_HEIGHT - 44, SHADOW_COLOR)
        self.draw_text_centered(center_x, 28, "ごもじンゴ", TEXT_COLOR)
        self.draw_text_centered(center_x, 120, " ".join(self.state.word), ACCENT_COLOR)
        pyxel.rectb(96 - pulse, 228 - pulse, 204 + pulse * 2, 104 + pulse * 2, ACTIVE_COLOR)
        self.draw_text_centered(center_x, 266, "みつけた", TEXT_COLOR)
        if self.state.result_is_new:
            self.draw_text_centered(center_x, 300, "NEW", ACCENT_COLOR)

    def draw_input(self):
        pyxel = self.pyxel
        center_x = SCREEN_WIDTH // 2
        pyxel.rectb(16, 18, SCREEN_WIDTH - 32, SCREEN_HEIGHT - 44, SHADOW_COLOR)
        self.draw_text_centered(center_x, 28, "ごもじンゴ", TEXT_COLOR)
        self.draw_text_centered(center_x, 62, "5文字をえらぶ", GRID_COLOR)

        slot_size = 58
        gap = 10
        start_x = center_x - (slot_size * 5 + gap * 4) // 2
        top_y = 106
        for index, letter in enumerate(self.state.slots):
            x = start_x + index * (slot_size + gap)
            y = top_y
            color = ACTIVE_COLOR if index == self.state.cursor_index else GRID_COLOR
            fill = ACCENT_COLOR if letter is not None else BACKGROUND_COLOR
            pyxel.rect(x + 2, y + 2, slot_size, slot_size, SHADOW_COLOR)
            pyxel.rect(x, y, slot_size, slot_size, fill)
            pyxel.rectb(x, y, slot_size, slot_size, color)
            self.draw_text_centered(
                x + slot_size // 2,
                y + 21,
                letter or "・",
                BACKGROUND_COLOR if letter is not None else LOCKED_COLOR,
            )
            self.buttons.append(
                Button(x - 2, y - 2, slot_size + 4, slot_size + 4, "", "slot", index)
            )
            if index == self.state.cursor_index:
                pyxel.rect(x + 15, y + slot_size + 11, 28, 3, ACTIVE_COLOR)

        pyxel.line(24, 196, SCREEN_WIDTH - 24, 196, GRID_COLOR)
        guide = "行をえらぶ"
        if self.state.input_layer == InputLayer.CHARACTERS:
            guide = f"{self.state.selected_group}行からえらぶ"
        self.draw_text_centered(center_x, 220, guide, TEXT_COLOR)

        if self.state.input_layer == InputLayer.ROWS:
            self.draw_row_panel(252)
        else:
            self.draw_kana_panel(252)
        self.draw_actions()

    def draw_row_panel(self, top_y):
        enabled = set(self.state.enabled_groups())
        for index, group_id in enumerate(tuple(KANA_GROUPS)):
            row = index // 5
            col = index % 5
            self.draw_button(
                Button(
                    22 + col * 72,
                    top_y + row * 60,
                    64,
                    52,
                    group_id,
                    "row",
                    group_id,
                    group_id in enabled,
                )
            )

    def draw_kana_panel(self, top_y):
        if self.state.selected_group is None:
            return
        enabled = set(self.state.enabled_kana())
        for index, kana in enumerate(KANA_GROUPS[self.state.selected_group]):
            row = index // 5
            col = index % 5
            self.draw_button(
                Button(
                    22 + col * 72,
                    top_y + row * 56,
                    64,
                    48,
                    kana,
                    "kana",
                    kana,
                    kana in enabled,
                )
            )

    def draw_actions(self):
        y = 580
        self.draw_button(Button(22, y, 70, 46, "けす", "delete"))
        self.draw_button(Button(100, y, 94, 46, "ぜんぶけす", "clear"))
        self.draw_button(Button(202, y, 82, 46, "おまかせ", "auto"))
        self.draw_button(
            Button(292, y, 82, 46, "しらべる", "confirm", enabled=self.state.can_confirm())
        )
        self.draw_text_centered(SCREEN_WIDTH // 2, 648, "Z/Enter けってい  X もどる", LOCKED_COLOR)

    def draw_result(self):
        pyxel = self.pyxel
        entry = self.state.result_entry
        if entry is None:
            self.state.return_to_input(True)
            return
        center_x = SCREEN_WIDTH // 2
        pyxel.rectb(16, 18, SCREEN_WIDTH - 32, SCREEN_HEIGHT - 44, SHADOW_COLOR)
        self.draw_text_centered(center_x, 28, "ごもじンゴ", TEXT_COLOR)
        self.draw_text_centered(center_x, 88, " ".join(entry["word"]), ACCENT_COLOR)
        pyxel.line(24, 174, SCREEN_WIDTH - 24, 174, GRID_COLOR)
        self.draw_text_centered(center_x, 204, f"【{entry['word']}】", TEXT_COLOR)
        self.draw_text_centered(
            center_x,
            242,
            f"{entry['category']} / R{entry['rarity']}",
            ACTIVE_COLOR,
        )
        if self.state.result_is_new:
            self.draw_text_centered(center_x, 266, "NEW", ACCENT_COLOR)
        elif entry["id"] in self.state.discovered_entry_ids:
            self.draw_text_centered(center_x, 266, "発見済み", LOCKED_COLOR)

        y = RESULT_TEXT_TOP
        for paragraph in entry["paragraphs"]:
            for line in self.wrap_text(paragraph, RESULT_WRAP_CHARS):
                self.draw_text(34, y, line, TEXT_COLOR)
                y += 19
            y += 10
        self.draw_button(Button(58, 586, 126, 48, "もういちど", "again"))
        self.draw_button(Button(212, 586, 126, 48, "べつのことば", "new"))
        self.draw_text_centered(
            center_x,
            650,
            f"発見 {self.state.found_count}/{len(ENTRIES)}  {entry['id']}",
            LOCKED_COLOR,
        )

    def draw_button(self, button):
        pyxel = self.pyxel
        self.buttons.append(button)
        focused = False
        if button.enabled and button.label:
            buttons = self.focusable_buttons()
            focused = buttons.index(button) == self.focus_index()
        fill = SHADOW_COLOR if button.enabled else BACKGROUND_COLOR
        border = ACTIVE_COLOR if focused else GRID_COLOR
        text_color = TEXT_COLOR if button.enabled else LOCKED_COLOR
        pyxel.rect(button.x + 2, button.y + 2, button.width, button.height, SHADOW_COLOR)
        pyxel.rect(button.x, button.y, button.width, button.height, fill)
        pyxel.rectb(button.x, button.y, button.width, button.height, border)
        self.draw_text_centered(
            button.x + button.width // 2,
            button.y + button.height // 2 - 6,
            button.label,
            text_color,
        )

    def focusable_buttons(self):
        return [button for button in self.buttons if button.enabled and button.label]

    def focus_index(self):
        buttons = self.focusable_buttons()
        if not buttons:
            self.state.focused_button = 0
            return 0
        self.state.focused_button %= len(buttons)
        return self.state.focused_button

    def move_focus(self, dx, dy):
        buttons = self.focusable_buttons()
        if not buttons:
            return
        current = buttons[self.focus_index()]
        current_x = current.x + current.width / 2
        current_y = current.y + current.height / 2
        candidates = []
        for index, button in enumerate(buttons):
            if button is current:
                continue
            button_x = button.x + button.width / 2
            button_y = button.y + button.height / 2
            offset_x = button_x - current_x
            offset_y = button_y - current_y
            if dx and offset_x * dx <= 0:
                continue
            if dy and offset_y * dy <= 0:
                continue
            axis_distance = abs(offset_x) if dx else abs(offset_y)
            cross_distance = abs(offset_y) if dx else abs(offset_x)
            candidates.append((axis_distance * 10 + cross_distance, index))
        if candidates:
            self.state.focused_button = min(candidates)[1]

    def activate_focused_button(self):
        buttons = self.focusable_buttons()
        if buttons:
            self.run_button_action(buttons[self.focus_index()])

    def activate_button_at(self, x, y):
        for button in reversed(self.buttons):
            if (
                button.enabled
                and button.x <= x < button.x + button.width
                and button.y <= y < button.y + button.height
            ):
                self.run_button_action(button)
                return

    def run_button_action(self, button):
        if button.action == "slot":
            self.state.select_slot(button.value)
        elif button.action == "row":
            self.state.open_kana_group(button.value)
        elif button.action == "kana":
            self.state.select_kana(button.value)
        elif button.action == "delete":
            self.state.delete_character()
        elif button.action == "clear":
            self.state.clear_word()
        elif button.action == "auto":
            self.state.autofill_word()
        elif button.action == "confirm":
            self.state.confirm_word()
        elif button.action == "again":
            self.state.return_to_input(False)
        elif button.action == "new":
            self.state.return_to_input(True)

    def wrap_text(self, text, max_chars):
        return [text[index : index + max_chars] for index in range(0, len(text), max_chars)]

    def draw_text_centered(self, center_x, y, text, color):
        self.draw_text(center_x - self.text_width(text) // 2, y, text, color)

    def text_width(self, text):
        return sum(12 if ord(char) > 127 else 6 for char in text)

    def draw_text(self, x, y, text, color):
        self.pyxel.text(x, y, text, color, self.font)


GomojiWebApp()
