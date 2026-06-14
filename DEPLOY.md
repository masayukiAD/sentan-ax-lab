# デプロイ手順 — Cloudflare 1社完結（登録＋DNS＋Pages）

公開URL（予定）: **https://ax-lab.masayukiishikawa.com**
個人サイト（ルート）: **https://masayukiishikawa.com**（Astro）
このサイトは純粋な静的（HTML/CSS/画像）。**ビルド不要**、フォルダをそのまま上げるだけ。

---

## 1. Cloudflareでドメイン取得（at-cost・1社完結）
1. Cloudflare 無料アカウント作成
2. ダッシュボード →「Domain Registration」→ `masayukiishikawa` を検索
3. `.com` を購入（卸値・WHOIS代行無料）。**ゾーン（DNS）は自動作成**＝ネームサーバー作業なし

> Cloudflareは `.jp` を扱わないため `.com` を採用。`.com` は最安・万能。

## 2. 個人サイト（Astro）をPagesへ ※順番は前後どちらでも可
- Pagesプロジェクト作成（Git連携 or 直接アップロード）
- ビルドコマンド: `astro build` ／ 出力ディレクトリ: `dist`
- カスタムドメイン: `masayukiishikawa.com`（ルート）
- ※ astro.config の `site:` は `https://masayukiishikawa.com` に更新済み

## 3. SENTAN AX LAB をPagesへ（サブドメイン）
**方法A（CLI・最短）**
```
cd ~/projects/sentan-ax-lab
npx wrangler login            # 初回のみ Cloudflare 認証（ブラウザで承認）
npx wrangler pages deploy . --project-name sentan-ax-lab
```
**方法B（GUI）**: Pages →「直接アップロード」→ このフォルダ（index.html のある階層）をドラッグ

その後：
- プロジェクトの「カスタムドメイン」→ `ax-lab.masayukiishikawa.com` を追加
- 同じCloudflare内なので CNAME と SSL は**自動** → 数分で https 公開

## 4. 公開後チェック
- [ ] `https://ax-lab.masayukiishikawa.com` が表示される
- [ ] OGPカード（X / Slack 等にURLを貼って確認）
- [ ] スマホ表示

---

## デプロイ前の任意クリーンアップ（軽量化）
- `assets/images/` に**未使用の元PNG**（`*-ax-lab.png` `*-arrival.png` `concept-*.png` `why-*.png`）が残存。実使用は `*.jpg` の2枚のみ。
  → 未使用PNGを削除 or `docs/`（公開フォルダ外）へ退避すると 14MB→1MB未満。
- `og:image`（sns 16x9 PNG 〜2.6MB）は大きめ。気になれば <1MB に圧縮。
- `_archive/` `docs/` は公開不要。アップロード対象から外す（or 事前退避）。

## 公開前に差し込み推奨
- 申込導線（`#join` のCTA）のURL（connpass / Googleフォーム / LINE 等）
- vol.01 の実コンテンツ（成果・写真・参加者の声）→ git-log の vol.01 へ

## 更新（2回目以降）
同じ `wrangler pages deploy .` を再実行、or GUIで再アップロードするだけ。
