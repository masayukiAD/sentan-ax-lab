# SENTAN AX LAB ／ Web サイト

豊田を、AIで、もっと面白く。／ AIではなく、AX。
AI学習コミュニティ「SENTAN AX LAB」の公式サイト（自主活動）。

- vol.01：2026.06.10（WED）／ ものづくり創造拠点 SENTAN（愛知県豊田市）
- vol.02：2026.07.16（THU）18:00–20:00 ／ 同所（募集中）
- 主催：石川 真之 ／ 協力：一般社団法人ものづくりアベンジャーズ（村本 梓）

## ローカルプレビュー

```
python3 -m http.server 5276
```
→ http://localhost:5276

## ファイル構成

```
sentan-ax-lab/
├── index.html             # 単一HTML（思想→学び合い→アーカイブ→参加 のハイブリッド構成）
├── styles.css             # ブランド＋レイアウト（ダーク×蛍光ライム／ターミナル・git log 風の意匠）
├── wabun-typography.css   # 和文組版の基本CSS（和欧混植・約物・禁則・行間）
├── assets/                # 画像（圧縮済 .jpg）・OG画像・noise.svg
└── docs/                  # 内部資料・画像の元データ（gitignore）
```

## デザイン

- 配色：ダーク `#0E0E10` × 生成り `#F2EFE6` × 蛍光ライム `#E8FF3A`
- フォント：Zen Kaku Gothic New（和文）／ Bricolage Grotesque（欧文）／ JetBrains Mono（日付・データ）
- 横組みの数字は算用数字、ターミナル / git log 風のUIで「コーディングAIの場」らしさを出す
- 依存JSなし、純粋な HTML/CSS

## 申込

参加・見学は Googleフォームから：https://forms.gle/ZtqrqUnayRDzntV27

## デプロイ

`DEPLOY.md` 参照（Cloudflare Pages、公開URL予定 `ax-lab.masayukiishikawa.com`）。
```
更新：master ではなく作業ブランチで編集 → レビュー → main にマージ
```
