# SENTAN AX LAB ／ LP

豊田を、AIで、もっと面白く。
AlphaDrive REGION が運営する AI 学習コミュニティ「SENTAN AX LAB」の身内検証用ランディングページ。

- 初回開催：2026.06.10 (WED) 18:00 - 20:00
- 場所：ものづくり創造拠点 SENTAN（愛知県豊田市）
- 主催：石川 真之 ／ 村本（AlphaDrive REGION）

## ローカルプレビュー

```
python3 -m http.server 5273
```

ブラウザで http://localhost:5273 を開く。

## ファイル構成

```
sentan-ax-lab/
├── index.html        # 単一HTML
├── styles.css        # 全スタイル
├── assets/
│   └── noise.svg     # R4 ノイズ素材
└── docs/             # 社内資料（gitignore対象）
```

## デザイン

- R3（Dark + Neon Single）ベース × R2（Brutalist）ヒーロー × R4（Noise）局所
- 配色：#0E0E10 / #F2EFE6 / #E8FF3A
- フォント：Zen Kaku Gothic New / Bricolage Grotesque / JetBrains Mono
- 依存JSなし、純粋なHTML/CSS。
