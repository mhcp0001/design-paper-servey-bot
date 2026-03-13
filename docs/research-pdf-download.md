# PDF自動ダウンロード 調査結果

**調査日:** 2026-03-13

## 結論

OA論文のPDF自動ダウンロードは可能だが、成功率は約50%。リポジトリ直接格納は非推奨。

---

## 1. OpenAlex の OA PDF URL の実態

### open_access フィールド構造

```json
"open_access": {
    "is_oa": true,
    "oa_status": "gold",       // "gold", "green", "hybrid", "bronze", "diamond", "closed"
    "oa_url": "https://...",   // string or null
    "any_repository_has_fulltext": true
}
```

### PDF URL の優先順位

1. `primary_location.pdf_url` — 設定されている場合は最も信頼性が高い直リンク
2. `open_access.oa_url` — フォールバック。ランディングページの場合もある
3. `primary_location.landing_page_url` — DOIランディングページ（人間向け）

### 実際のアクセス検証結果

| 出版社 | OAステータス | Content-Type | 結果 |
|--------|-------------|-------------|------|
| Frontiers | gold | `application/pdf` | **DL成功** |
| Cambridge UP | bronze | `application/pdf` | **DL成功** |
| anil.recoil.org | gold | `application/pdf` | **DL成功** |
| Nature | gold | `text/html` (303) | **失敗** - 認証リダイレクト |
| JAMA Network | gold | `text/html` (403) | **失敗** - Cloudflare ブロック |
| Taylor & Francis | hybrid | `text/html` (403) | **失敗** - Cloudflare ブロック |
| OJS/Lattice | bronze | `text/html` (403) | **失敗** - Cloudflare ブロック |

### OA比率（2026-03-06〜2026-03-13 の実測値）

| ステータス | 件数 | 割合 |
|-----------|------|------|
| green | 29,895 | 37.2% |
| closed | 19,558 | 24.3% |
| gold | 14,803 | 18.4% |
| diamond | 8,318 | 10.4% |
| hybrid | 6,952 | 8.7% |
| bronze | 819 | 1.0% |

全体の約76%がOAだが、プログラムでPDF取得できるのは約半分。

---

## 2. ストレージ選択肢の比較

| 方式 | 容量 | コスト | 推奨度 | 備考 |
|------|------|--------|--------|------|
| **Git直接格納** | 100MB/ファイル上限、リポジトリ推奨1GB | 無料 | 非推奨 | 履歴が永久に肥大化 |
| **Git LFS** | 1GB storage + 1GB/月帯域 | 無料枠小、$5/50GB | 微妙 | 帯域制限がきつい |
| **GitHub Actions Artifact** | 500MB (Free)、2GB (Pro) | 無料 | 一時保存向き | 90日保持、ワークフロー間で共有可 |
| **GitHub Releases** | 2GB/ファイル、総量無制限 | 無料 | 配布向き | エグレス無料 |
| **Cloudflare R2** | 10GB無料、エグレス無料 | 無料〜$0.015/GB | 長期アーカイブ最適 | S3互換API |
| **AWS S3** | 5GB (12ヶ月のみ) | $0.023/GB + エグレス$0.09/GB | 高コスト | エグレス費用が高い |

---

## 3. 想定ボリューム

- 週10本選定 → うちOA精読推奨3-5本 → DL成功2-3本
- 論文PDF平均サイズ: 0.5〜2MB（図表多めのデザイン系は2-5MB）
- 年間: 約100-150本、100-300MB程度

---

## 4. 推奨アーキテクチャ

```
weekly-survey.yml
  → reports/YYYY-MM-DD.md   (Markdown、Git管理)
  → reports/YYYY-MM-DD.json (JSON、Git管理)

deep-review.yml (Phase 2)
  → PDFダウンロード (curl + Content-Type検証 + magic bytes検証)
  → GitHub Actions Artifact として保存 (90日保持)
  → Discord通知にArtifactリンクを含める
  → 長期保存が必要になったらR2 or Releasesへ移行
```

---

## 5. 実装時の注意点

### バリデーション

```python
response = requests.get(url, timeout=30, allow_redirects=True)
content_type = response.headers.get('Content-Type', '')

# Content-Type検証
if 'application/pdf' not in content_type:
    raise ValueError(f"Not a PDF: {content_type}")

# Magic bytes検証
if not response.content[:5] == b'%PDF-':
    raise ValueError("File does not start with PDF magic bytes")

# ファイルサイズ検証
if len(response.content) < 10000:
    raise ValueError(f"Suspiciously small: {len(response.content)} bytes")
if len(response.content) > 50 * 1024 * 1024:
    raise ValueError("File too large (>50MB)")
```

### レート制限

- ダウンロード間に1-2秒スリープ
- 指数バックオフで最大3回リトライ
- User-Agent にボット名+連絡先を明記
- 出版社サイトへの並列アクセスは避ける

### 法的考慮事項

- OA論文（CC-BY等）のダウンロードは合法
- Unpaywall経由のURLは合法なソースのみを指す
- PubMed Centralのバルクダウンロードは専用FTP/APIを使用
- arXivは `export.arxiv.org` または S3バケットを使用
- 出版社サイトのスクレイピングはTDM API契約が必要

---

## 6. 関連ツール・ライブラリ

| ツール | 用途 | 備考 |
|--------|------|------|
| unpywall | Unpaywall Pythonクライアント | `download_pdf_file(doi)` メソッド |
| pyalex | OpenAlex Pythonクライアント | `open_access` フィールドアクセス |
| paperscraper | マルチソース論文スクレイパー | PubMed, arXiv, bioRxiv対応 |
| puremagic | ファイルタイプ検証 | 依存なし、純Python |

---

## 7. 参考リンク

- [OpenAlex Work Object - open_access](https://developers.openalex.org/api-entities/works/work-object)
- [Unpaywall API](https://unpaywall.org/products/api)
- [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- [GitHub Docs - About Large Files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [GitHub Docs - Git LFS Billing](https://docs.github.com/billing/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage)
- [Cloudflare R2 Pricing](https://developers.cloudflare.com/r2/pricing/)
- [Programmatically Downloading Open Access Papers](https://brainsteam.co.uk/2018/04/13/programmatically-downloading-open-access-papers/)
