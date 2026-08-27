# title: ごもじンゴ
# author: sejiseji
# desc: Pyxel project scaffold for Gomoji
# site: https://github.com/sejiseji/gomoji
# license: MIT
# version: 0.3.1

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
        "id": 'GMG0002',
        "word": 'ひるのびる',
        "category": '現象',
        "rarity": 2,
        "paragraphs": (
            '昼休みの終わりが近づくほど、時計の一分だけが妙に長く感じられる現象。',
            '食事を終えて席へ戻るつもりでいると起こりやすく、片づけや歯みがきまで済ませた人にはほとんど現れない。',
            '実際の時刻は進んでいるため、のびた昼はたいてい午後の予定から差し引かれる。',
        ),
    },
    {
        "id": 'GMG0003',
        "word": 'まどくもり',
        "category": '現象',
        "rarity": 1,
        "paragraphs": (
            '窓ガラスの一部だけが曇り、外の見たい場所を狙って隠す現象。',
            '指で拭けば視界は戻るが、その跡が気になって二度目の掃除が始まりやすい。',
            '結露そのものより、最初の一拭きが生活を遅らせる。',
        ),
    },
    {
        "id": 'GMG0004',
        "word": 'かぜまよい',
        "category": '現象',
        "rarity": 1,
        "paragraphs": (
            '開いた窓から入った風が出口を見失い、部屋の中を一周してから同じ窓へ戻る現象。',
            'カーテン、紙袋、吊るした服の順に触れていくため、通った道だけは分かりやすい。',
            '換気量は少ないが、室内に何が置かれているかは丁寧に確認していく。',
        ),
    },
    {
        "id": 'GMG0005',
        "word": 'あめおどり',
        "category": '現象',
        "rarity": 1,
        "paragraphs": (
            '弱い雨粒が手すりや傘の縁で一度だけ跳ね、落ちる向きを変える現象。',
            '粒が小さいほど軽やかに見えるが、見とれていると同じ場所へ次の一滴が当たる。',
            '踊っているのは雨であり、袖口まで参加させる必要はない。',
        ),
    },
    {
        "id": 'GMG0006',
        "word": 'こえのこり',
        "category": '現象',
        "rarity": 3,
        "paragraphs": (
            '会話が終わったあとも、最後のひと言だけが部屋に残って聞こえるように感じる現象。',
            '言い方を気にした時ほど繰り返され、別の作業を始めても語尾だけが勝手についてくる。',
            '聞き直しても相手はもう帰っているので、修正できるのは次の会話からである。',
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
        "id": 'GMG0161',
        "word": 'やるきまち',
        "category": '状態・感情',
        "rarity": 2,
        "paragraphs": (
            '作業を始める準備だけ整え、やる気が到着するまで静かに待っている状態。',
            '机を拭く、飲み物を用意する、必要のない設定を見直すなど、待合室の設備だけは充実していく。',
            'やる気は準備が終わった頃ではなく、別の予定が始まる頃に来ることが多い。',
        ),
    },
    {
        "id": 'GMG0162',
        "word": 'ねむりかけ',
        "category": '状態・感情',
        "rarity": 3,
        "paragraphs": (
            '眠ってはいないが、返事の一部を夢側へ預け始めている状態。',
            '目は開いていても会話の接続が弱くなり、質問に対して少し前の話題が返ってくる。',
            '本人は起きていたと主張するが、その証言も半分ほど眠っている。',
        ),
    },
    {
        "id": 'GMG0163',
        "word": 'きもちあと',
        "category": '状態・感情',
        "rarity": 1,
        "paragraphs": (
            '出来事が終わってから、遅れて本当の気持ちが追いついてくる状態。',
            'その場では平然と対応できるため、帰り道や入浴中に感情の本体が到着する。',
            '言いたかったことも一緒に届くが、会話の受付時間はすでに終わっている。',
        ),
    },
    {
        "id": 'GMG0164',
        "word": 'ぼんやりめ',
        "category": '状態・感情',
        "rarity": 1,
        "paragraphs": (
            '集中できていないほどではないが、物事の輪郭を少し甘く見ている状態。',
            '簡単な用事はこなせるものの、置いた物の場所や返事の細部が薄く残る。',
            '休めば治る程度なのに、休む判断だけがぼんやりしている。',
        ),
    },
    {
        "id": 'GMG0165',
        "word": 'ためいきち',
        "category": '状態・感情',
        "rarity": 1,
        "paragraphs": (
            'ため息が一度で終わらず、胸のあたりに次の一回分を残している状態。',
            '大きな不満がなくても起こり、座り直した時や画面を閉じた時に続きが出る。',
            '深呼吸に切り替えれば収まるが、見た目がほぼ同じなので周囲には伝わらない。',
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
        "id": 'GMG0292',
        "word": 'すみねずみ',
        "category": '生物',
        "rarity": 2,
        "paragraphs": (
            '部屋の隅から隅へ移り、中央をできるだけ使わずに暮らす小さなねずみ。',
            '壁際に沿って進むため動きは慎重に見えるが、本人は最短距離のつもりでいる。',
            '家具を動かすと新しい隅を探し始めるので、掃除のたびに住所が変わる。',
        ),
    },
    {
        "id": 'GMG0293',
        "word": 'ぬくもぐら',
        "category": '生物',
        "rarity": 2,
        "paragraphs": (
            '地中ではなく、家の中の温かい場所を掘り当てることに長けたもぐら。',
            '日なた、毛布の下、充電中の機器のそばを順に巡り、温度が下がると黙って移動する。',
            '穴は掘らないため被害は少ないが、最も快適な席だけは先に取られる。',
        ),
    },
    {
        "id": 'GMG0294',
        "word": 'まどすずめ',
        "category": '生物',
        "rarity": 3,
        "paragraphs": (
            '窓の外から室内をのぞき、誰かと目が合うまで小さく跳ねるすずめ。',
            '餌を待っているのかと思えば、与えると少し離れて食べ、また同じ位置へ戻ってくる。',
            '用事は最後まで分からないものの、こちらが席を立つと満足して飛び去る。',
        ),
    },
    {
        "id": 'GMG0295',
        "word": 'こたつむり',
        "category": '生物',
        "rarity": 3,
        "paragraphs": (
            'こたつの中へ体の大半を収め、必要な時だけ上半身を出す冬の生物。',
            'みかん、飲み物、充電器を手の届く範囲へ集めることで、移動回数を極端に減らしている。',
            '春になると自然に姿を消すが、抜け殻として座布団が残る。',
        ),
    },
    {
        "id": 'GMG0296',
        "word": 'つきたぬき',
        "category": '生物',
        "rarity": 2,
        "paragraphs": (
            '月明かりのある夜だけ、水面に映った自分を長く眺めるたぬき。',
            '月を眺めているのかと思えば、雲で顔が隠れると水面へ少し近づく。',
            '風で像が崩れるたびに姿勢を直すため、観月より身だしなみに忙しい。',
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
        "id": 'GMG0401',
        "word": 'もちあわせ',
        "category": '食べ物',
        "rarity": 1,
        "paragraphs": (
            '形や味の違う餅を少しずつ盛り、一皿で迷えるようにした取り合わせ。',
            '最初は全種類を均等に食べる予定でも、好みの餅だけ先になくなり、最後に責任のような一個が残る。',
            '持ち合わせがない時でも作れるが、餅の持ち合わせは必要である。',
        ),
    },
    {
        "id": 'GMG0402',
        "word": 'ぱんしみる',
        "category": '食べ物',
        "rarity": 1,
        "paragraphs": (
            '焼いたパンへ温かい汁を吸わせ、外側の香ばしさと内側の柔らかさを同時に楽しむ料理。',
            '浸す時間が短いと味が届かず、長いと持ち上げる前に形がほどける。',
            'ちょうどよい瞬間は数秒しかないため、会話を始める前に食べたほうがよい。',
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
        "id": 'GMG0404',
        "word": 'まめごろも',
        "category": '食べ物',
        "rarity": 3,
        "paragraphs": (
            '煎った豆を薄い衣で包み、噛んだ時に二段階の音が出るよう仕上げた菓子。',
            '外側は軽く割れ、少し遅れて豆が砕けるため、一粒でも食べた感じが長く続く。',
            '静かな場所では食感より所在がよく分かる。',
        ),
    },
    {
        "id": 'GMG0405',
        "word": 'いもひとや',
        "category": '食べ物',
        "rarity": 2,
        "paragraphs": (
            '蒸した芋を一晩休ませ、甘さと落ち着きを引き出した素朴な食べ物。',
            '出来たてより冷めた頃のほうが味がまとまるため、急いで食べないことも調理に含まれる。',
            '翌朝まで残すつもりで作られるが、夜の確認作業で量が減りやすい。',
        ),
    },
    {
        "id": 'GMG0406',
        "word": 'くりしずく',
        "category": '食べ物',
        "rarity": 2,
        "paragraphs": (
            '栗を裏ごしした餡へ蜜を一滴ずつ落とし、口当たりを軽くした小さな甘味。',
            '蜜が多いと栗の香りが隠れ、少ないと名前ほどしずく感が出ない。',
            '調整中の味見が最も完成に近いという、作り手には不便な菓子である。',
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
        "id": 'GMG0502',
        "word": 'あとまわし',
        "category": '技・動作',
        "rarity": 1,
        "paragraphs": (
            '今すぐできる用事を、未来の自分へ丁寧に引き渡す技。',
            '期限と難しさを確認してから送るため、実行中は計画的な判断に見える。',
            '未来の自分も同じ技を使えるので、引き渡し先だけが少しずつ追い詰められる。',
        ),
    },
    {
        "id": 'GMG0503',
        "word": 'しれっとめ',
        "category": '技・動作',
        "rarity": 4,
        "paragraphs": (
            '騒ぎを大きくせず、話題や動作を自然な顔で止める技。',
            '急に制止すると目立つ場面で使われ、別の物を手に取る、窓を見る、飲み物を勧めるなどの動きと組み合わせる。',
            '止められた側が気づかなければ成功だが、気づいても確認しにくい点が強い。',
        ),
    },
    {
        "id": 'GMG0504',
        "word": 'すっとぼけ',
        "category": '技・動作',
        "rarity": 1,
        "paragraphs": (
            '事情を知っている状態のまま、知らない人の速度で会話へ戻る技。',
            '驚きすぎず、理解もしすぎない表情を保ち、必要な部分だけ質問に変える。',
            '技量が高いほど自然だが、使い慣れている事実まで自然に伝わる。',
        ),
    },
    {
        "id": 'GMG0505',
        "word": 'ゆびすべり',
        "category": '技・動作',
        "rarity": 1,
        "paragraphs": (
            '画面上で狙った場所の隣を押し、予定外の操作へ移る技。',
            '指先の乾きや画面の大きさが原因とされるが、慌てて戻ろうとすると二手目もずれやすい。',
            '一度なら事故、三度続けばその操作に詳しくなったと考えてよい。',
        ),
    },
    {
        "id": 'GMG0506',
        "word": 'ひとまかせ',
        "category": '技・動作',
        "rarity": 2,
        "paragraphs": (
            '得意そうな人へ仕事を渡し、自分は邪魔をしないことで全体を進める技。',
            '適切に使えば分担になるが、説明を省きすぎると相手が仕事の発見から担当することになる。',
            '任せた後も結果だけ細かく見ると、技ではなく観客席になる。',
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
        "id": 'GMG0602',
        "word": 'ひもまとめ',
        "category": '道具',
        "rarity": 3,
        "paragraphs": (
            '充電ケーブルや細い紐を、一つの輪にまとめてほどけにくくする道具。',
            '巻く向きをそろえると美しく収まるが、急いで外す時ほど結び目のように抵抗する。',
            '机は整うものの、必要な一本を選ぶ作業までまとめてはくれない。',
        ),
    },
    {
        "id": 'GMG0603',
        "word": 'ふたおこし',
        "category": '道具',
        "rarity": 1,
        "paragraphs": (
            '固く閉じた蓋の縁へ差し込み、最初のわずかな隙間を作る道具。',
            '隙間さえできれば手で開けられるため、働く時間は短いが役割ははっきりしている。',
            '使い終える頃には、蓋より先に見失われている。',
        ),
    },
    {
        "id": 'GMG0604',
        "word": 'くつそろえ',
        "category": '道具',
        "rarity": 2,
        "paragraphs": (
            '玄関で向きのばらついた靴を、つま先が同じ方向へ向くよう静かに押す道具。',
            '左右の小さな板が一足ずつ位置を直すため、手を使わずに見た目だけ整えられる。',
            '靴底の泥や脱ぎ方までは直せないので、玄関の礼儀は半分ほど本人に残る。',
        ),
    },
    {
        "id": 'GMG0605',
        "word": 'ものさがし',
        "category": '道具',
        "rarity": 1,
        "paragraphs": (
            '探している物の特徴を入力すると、最後に見た可能性の高い場所を示す小型端末。',
            '机、鞄、上着の順に候補を出すが、使用者がそこを探したと言い張ると次へ進む。',
            '正解が手の中だった場合だけ、画面を暗くして配慮する。',
        ),
    },
    {
        "id": 'GMG0606',
        "word": 'まよいばこ',
        "category": '道具',
        "rarity": 2,
        "paragraphs": (
            '置き場所が決まっていない小物を、ひとまず受け入れるための箱。',
            '片づけの流れを止めない利点があり、鍵、部品、説明書などが一時的に集まる。',
            '一時的という言葉を守らないと、箱そのものが大きな迷い物になる。',
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
        "id": 'GMG0702',
        "word": 'あとでやる',
        "category": '習慣・制度',
        "rarity": 3,
        "paragraphs": (
            '今は行わない用事について、忘れていないことだけを確認する小さな宣言。',
            '口に出すことで一度安心できるため、実行の代わりとして使われやすい。',
            '後での時刻を決めないまま繰り返すと、用事より宣言のほうが習慣になる。',
        ),
    },
    {
        "id": 'GMG0703',
        "word": 'おやつわけ',
        "category": '習慣・制度',
        "rarity": 3,
        "paragraphs": (
            '人数より少し多い菓子を開け、欲しい量を互いに探りながら分ける習慣。',
            '最初の一人が遠慮すると全体の基準が下がり、最後に一個だけ判断の難しい菓子が残る。',
            '誰も取らない時間が長いほど、その一個への関心は高い。',
        ),
    },
    {
        "id": 'GMG0704',
        "word": 'せきゆずり',
        "category": '習慣・制度',
        "rarity": 1,
        "paragraphs": (
            '座席を必要としていそうな人へ、相手が気まずくならない形で場所を渡す作法。',
            '立ち上がってから声をかけると断りにくく、先に尋ねると互いに遠慮が始まる。',
            '譲った後に平気な顔で立っているところまで含めて、一連の作法とされる。',
        ),
    },
    {
        "id": 'GMG0705',
        "word": 'ひとやすみ',
        "category": '習慣・制度',
        "rarity": 1,
        "paragraphs": (
            '作業を完全にやめず、再開できる姿勢だけ残して短く休む習慣。',
            '飲み物を取る、窓の外を見る、椅子へ深く座るなど、終了時刻を決めやすい動作が選ばれる。',
            '横になると別の制度へ移行するため、ひとやすみの範囲から外れる。',
        ),
    },
    {
        "id": 'GMG0706',
        "word": 'ねるまえに',
        "category": '習慣・制度',
        "rarity": 1,
        "paragraphs": (
            '就寝の直前になって、日中は気にならなかった用事を一つだけ始める習慣。',
            '机の整理や返信の確認など短く終わる作業が選ばれるが、その途中で別の用事も見つかる。',
            '眠る準備が整うほど活動的になるため、開始条件と目的がかみ合っていない。',
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
        "id": 'GMG0801',
        "word": 'まよいみち',
        "category": '場所',
        "rarity": 1,
        "paragraphs": (
            '目的地へ向かっている人だけが、同じ角を二度通った気になる細い道。',
            '景色は少しずつ変わるため戻ってはいないが、目印にした物だけが先回りして現れる。',
            '急がず歩けば普通の近道で、迷っていると認めた瞬間に出口が近くなる。',
        ),
    },
    {
        "id": 'GMG0802',
        "word": 'ひるねばし',
        "category": '場所',
        "rarity": 1,
        "paragraphs": (
            '昼過ぎに渡ると、川音と揺れがちょうど眠気を誘う小さな橋。',
            '立ち止まる場所はないものの、欄干へ手を置くと数分だけ用事を忘れやすい。',
            '橋を渡り終える頃には目が覚めるので、昼寝としては移動が多い。',
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
        "id": 'GMG0804',
        "word": 'こえのへや',
        "category": '場所',
        "rarity": 3,
        "paragraphs": (
            '話した声がすぐ消えず、壁の近くに薄く残る部屋。',
            '同じ場所で別の言葉を重ねると前の声が押し出され、入口付近で小さく聞こえる。',
            '秘密の相談には向かないが、言い直しには少しだけ親切である。',
        ),
    },
    {
        "id": 'GMG0805',
        "word": 'すみっこや',
        "category": '場所',
        "rarity": 3,
        "paragraphs": (
            '部屋や店の端に生まれる、一人分だけ落ち着ける小さな場所。',
            '正式な席ではなくても、壁と家具の角度が合うと自然に荷物と人が収まる。',
            '人気が出ると誰かが椅子を置き、すみっこではなくなる。',
        ),
    },
    {
        "id": 'GMG0806',
        "word": 'あめのうら',
        "category": '場所',
        "rarity": 3,
        "paragraphs": (
            '強い雨の向こう側に、一瞬だけ見える明るく乾いた場所。',
            '建物や木の輪郭は分かるが、雨脚が動くたび位置も変わるため近づけない。',
            '雨が止むと普通の景色に戻り、乾いていた理由だけが残らない。',
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
        "id": 'GMG0882',
        "word": 'へんじまち',
        "category": 'インターネット',
        "rarity": 1,
        "paragraphs": (
            '送ったメッセージへの返事を待ちながら、別のことへ集中できなくなる時間。',
            '通知を確認するたび待ち時間が最初から意識され、画面を伏せると音がした気がする。',
            '返事が来た瞬間だけ、何を書いたか思い出す時間が必要になる。',
        ),
    },
    {
        "id": 'GMG0883',
        "word": 'いいねだけ',
        "category": 'インターネット',
        "rarity": 2,
        "paragraphs": (
            '内容には強く同意しているが、文章で返すほどの言葉が見つからない時に行う反応。',
            '短くても意思は伝わる一方、深刻な話題では押した側が少し不安になる。',
            '相手もいいねだけで返すと、会話は静かに成立したことになる。',
        ),
    },
    {
        "id": 'GMG0884',
        "word": 'きじよまず',
        "category": 'インターネット',
        "rarity": 1,
        "paragraphs": (
            '見出しと添えられた一文だけで記事の内容を理解した気になる読み方。',
            '話題へ早く参加できるが、本文にある条件や例外を後から教えられることが多い。',
            '記事を開けば解決するものの、その頃には別の見出しが来ている。',
        ),
    },
    {
        "id": 'GMG0885',
        "word": 'あとでよむ',
        "category": 'インターネット',
        "rarity": 3,
        "paragraphs": (
            '気になる記事や投稿を保存し、未来の自分へ読む役目を渡す行為。',
            '保存した時点で少し理解した気持ちになるため、一覧は増えるが消化は進みにくい。',
            '数か月後に見返すと、内容より保存した当時の関心がよく分かる。',
        ),
    },
    {
        "id": 'GMG0886',
        "word": 'かきなおし',
        "category": 'インターネット',
        "rarity": 1,
        "paragraphs": (
            '送信前の文章を何度も直し、最初の勢いと最後の礼儀を両立させようとする作業。',
            '語尾を柔らかくすると本文が強く見え、本文を削ると挨拶だけが立派になる。',
            '最終稿が最初の一文へ戻った時は、考えた時間だけが丁寧さとして残る。',
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
        "id": 'GMG0952',
        "word": 'かげふたり',
        "category": '怪異',
        "rarity": 2,
        "paragraphs": (
            '一人で歩いているのに、足元へ二人分の影が並ぶ怪異。',
            '片方は本人と同じ動きをするが、もう片方は半歩遅れて角を曲がる。',
            '立ち止まると二つとも重なるため、数え直す機会だけは与えられない。',
        ),
    },
    {
        "id": 'GMG0953',
        "word": 'まどのあと',
        "category": '怪異',
        "rarity": 3,
        "paragraphs": (
            '誰も触れていない窓に、内側から指でなぞったような跡が残る現象。',
            '跡は外の景色を指す形だが、確認するたび少しだけ向きが変わる。',
            '拭けば消えるものの、布には何も付かないので掃除の達成感がない。',
        ),
    },
    {
        "id": 'GMG0954',
        "word": 'こえのぬし',
        "category": '怪異',
        "rarity": 1,
        "paragraphs": (
            '夜の家で一度だけ名前を呼び、返事を待たずに黙る正体不明の声。',
            '家族に似て聞こえるが、誰の声か考えるほど細部が曖昧になる。',
            '翌朝に尋ねると全員が違うと言うため、声だけが家族構成に詳しい。',
        ),
    },
    {
        "id": 'GMG0955',
        "word": 'みちのさき',
        "category": '怪異',
        "rarity": 1,
        "paragraphs": (
            '何度曲がっても同じ景色が続き、先へ進んだ距離だけが分からなくなる場所。',
            '後ろを振り返れば来た道は普通に見えるため、戻る判断だけが難しくなる。',
            '立ち止まって地図を開くと現在地は合っており、地図のほうが少し困っている。',
        ),
    },
    {
        "id": 'GMG0956',
        "word": 'よるのしみ',
        "category": '怪異',
        "rarity": 1,
        "paragraphs": (
            '夜になると壁や天井の一部へ現れ、朝には消える薄い影。',
            '湿気の跡に似ているが、照明を変えると形だけがゆっくり別の場所へ移る。',
            '毎晩少しずつ近づいてくるが、家具を動かすと元の位置へ戻る。',
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
