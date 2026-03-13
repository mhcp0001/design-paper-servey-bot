# Design Paper Survey Bot

このリポジトリはビジネスデザイン・イノベーション領域の論文週次自動サーベイシステムです。

## 動作ルール
- OpenAlex REST API（https://api.openalex.org/）を使って論文を検索する
- 検索は3層構造で行う:
  1. Topic IDフィルタ（config/topics.json に定義）
  2. キーワード検索（prompts/survey-prompt.md に定義）
  3. ジャーナルISSN指定（config/sources.json に定義）
- 結果は `reports/YYYY-MM-DD/` フォルダに保存する（report.md, survey.json, OA論文PDF）
- 既存レポートと重複する論文（DOI またはOpenAlex Work IDで判定）は除外する
- 出力は全て日本語（論文タイトル・ジャーナル名は英語原文のまま）

## API仕様メモ
- 認証: `api_key` パラメータで渡す（GitHub Secrets: `OPENALEX_API_KEY`）
- 日付フィルタ: `from_publication_date:YYYY-MM-DD,to_publication_date:YYYY-MM-DD`
- トピックフィルタ: `topics.id:T12345`
- ジャーナルフィルタ: `primary_location.source.id:S12345678`（ISSNからSource IDを事前取得）
- ソート: `sort=cited_by_count:desc` または `sort=publication_date:desc`
- ページング: `per_page=25`（最大200）
- アブストラクトは `abstract_inverted_index` 形式で返される → 復元処理が必要
- OA情報: `open_access.is_oa`（bool）, `open_access.oa_status`（gold/green/hybrid/bronze/diamond/closed）, `open_access.oa_url`（PDF/原文URL or null）
- PDF直リンク: `primary_location.pdf_url`（設定時は `oa_url` より信頼性が高い）
- ランディングページ: `primary_location.landing_page_url`（DOIページ、フォールバック用）

### アブストラクト復元方法
```python
import json
def restore_abstract(inverted_index):
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(w for _, w in word_positions)
```

## ディレクトリ構成
- `prompts/` — サーベイプロンプト（検索クエリ・選定基準）
- `reports/YYYY-MM-DD/` — 週次レポート出力先（report.md, survey.json, *.pdf）
- `docs/` — 調査・設計ドキュメント
- `config/` — Topic ID、Source ID 等の設定ファイル
- `scripts/` — セットアップ・ユーティリティスクリプト
