# Design Paper Survey Bot

GitHub Actions + Claude Code によるビジネスデザイン・イノベーション領域の論文自動収集・日本語要約システム。

毎週月曜に主要デザイン・経営学ジャーナルおよびOpenAlexから論文を選定し、日本語要約を生成してリポジトリに蓄積する。

## 対象領域
- ビジネスデザイン / ビジネスモデルイノベーション
- サービスデザイン / サービスイノベーション
- デザイン思考 / デザインマネジメント
- イノベーションマネジメント / オープンイノベーション
- 戦略経営 / ダイナミックケイパビリティ
- スペキュラティブデザイン / フューチャーズスタディーズ
- システム思考 / トランジション研究

## データソース
- **メイン:** OpenAlex API（2.5億+論文、無料、APIキー必須）
- **補助:** Semantic Scholar（関連論文推薦、AI要約）

## セットアップ

### 1. OpenAlex APIキー取得
1. https://openalex.org でアカウント作成
2. https://openalex.org/settings/api でAPIキーを取得

### 2. GitHub Secrets 設定
| Secret名 | 説明 |
|----------|------|
| `OPENALEX_API_KEY` | OpenAlexのAPIキー |
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code用OAuthトークン |
| `DISCORD_WEBHOOK_URL` | Discord通知用URL（任意） |

### 3. Topic ID 探索（初回のみ）
```bash
# GitHub Actions から手動実行
# Actions > "Discover Topic IDs" > Run workflow
```
結果は `config/topics.json` にコミットされる。

### 4. 週次サーベイ
毎週月曜 9:00 JST に自動実行。手動実行も可能。
