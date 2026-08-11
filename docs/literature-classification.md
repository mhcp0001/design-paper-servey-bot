# DL済み文献の分類とカテゴリ体系・要約検証レポート

**作成日**: 2026-08-11
**対象**: `reports/` 配下にPDFがダウンロード済みの全20文献（2026-03-13 〜 2026-08-03）
**方法**: 全20本のPDF本文（計約178万字）を抽出し、`survey.json` / `report.md` の記載と本文を突合

---

## 1. サマリー

| 項目 | 結果 |
|---|---|
| 検証対象文献 | 20本（自動DL 18本 + 手動命名 2本） |
| PDF本文抽出 | 20/20 成功（総ページ数 453p） |
| 作成したカテゴリ | 6大カテゴリ + 3横断タグ |
| 要約の問題検出 | **13件**（レベルA 事実誤り 4件 / レベルB 過剰一般化 4件 / レベルC 軽微 5件） |
| 構造的問題 | `abstract` 欄が仕様（原文復元）に反しLLM再記述になっている（20本中7本で原文一致率60%未満） |

> **最重要**: レベルAの4件は、社内共有やクライアント提案にそのまま使うと事実誤認を招く。特に W7168377411（Demir）と W7140141462（Gërdoçi）は**サンプル数・調査対象・主要知見が論文と一致していない**。

---

## 2. カテゴリ体系

対象ユーザー（ビジョンデザイン／戦略デザイン／ビジネスデザイン）の業務軸に沿って6カテゴリを設計した。
各文献は**主カテゴリ1つ**に配置し、またがるものは横断タグで補足する。

```
C1. デザイン実践の方法論          … 手法・ツール・ワークショップ設計       5本
C2. 問題定義とデザインの認知基盤    … リフレーミング／デザイン行為の理論     2本
C3. 未来洞察・フォーサイト         … 未来の描き方と制度的機能              3本
C4. 組織デザインと両利き           … 組織構造・リーダーシップ・移行期        3本
C5. ビジネスモデル・共創エコシステム … BMI・境界マネジメント・共創           5本
C6. システム思考・社会転換         … システム的実践・トランジション研究      2本
```

**横断タグ**: `#AI` `#サステナビリティ` `#SME・中小企業`

---

### C1. デザイン実践の方法論（5本）

手法そのものの設計・実装・評価を扱う。**明日の現場で使える**度合いが最も高い群。

| ID | 論文 | 誌 | 手法 | 実務での使いどころ |
|---|---|---|---|---|
| W7167048822 | ADT: a digital card-based toolkit for AI-augmented design thinking `#AI` | Proc. Design Society | 調査(n=204)+ツール開発+評価(n=61) | DTの5段階×4職能ロールにAI活用を割り付けるカード。社内DT研修のAI対応アップデートに直接転用可 |
| W7151799517 | Strategy Jams: using design thinking to charter teams | Frontiers in Psychology | 混合手法パイロット(5チーム) | 新規事業チーム立ち上げ時のチャーター策定ワークショップ設計 |
| W7168377411 | Design Thinking in Practice: Lessons from Context-Sensitive Implementation in SMEs `#SME` | J. of Innovation Management | 専門家インタビュー(7名)/Gioia法 | 短時間ワークショップを数週に分散、低コストプロトタイプ等、リソース制約下のDT実装パターン |
| W7135085837 | Investigating the use of design thinking in identifying wicked problems of startups | J. of Innovation & Entrepreneurship | Research through Design(5社/18ヶ月) | 「問題定義のショートカット」という失敗モードの診断視点 |
| W7163025447 | Trends and Challenges in Service Design Methods | IJARBSS | 63手法の主題分析 | サービスデザイン手法の見取り図（※誌の査読品質に留意、後述） |

---

### C2. 問題定義とデザインの認知基盤（2本）

**「なぜデザインが効くのか」を説明する層。**社内でデザインの価値を語る際の理論的裏付けになる。

| ID | 論文 | 誌 | 手法 | 実務での使いどころ |
|---|---|---|---|---|
| W7134858137 | Reframing Through New Minds: How External Experts Unlock Problem Reframing Through Reasoning Logics | JPIM | エスノグラフィ(4プロジェクト) | 外部専門家を招く際の「何を期待するか」の設計論。5つの推論ロジックはワークショップ設計の骨格に使える |
| W7142215350 | Functional pretence: what makes humans designers | Int. J. Technology & Design Education | 理論的統合（人類学×認知科学×発達心理学） | ビジョニング／プロトタイピング／スペキュラティブデザインを一つの認知能力で統一的に説明できる |

---

### C3. 未来洞察・フォーサイト（3本）

**ビジョンデザインの中核。**手法論だけでなく「フォーサイトが組織の中で何をしているか」を扱う点が実務的に効く。

| ID | 論文 | 誌 | 手法 | 実務での使いどころ |
|---|---|---|---|---|
| W7167783984 | Governance logics and foresight functions: European strategic foresight | European J. of Futures Research | 対比事例（EU/日本/韓国）+文献計量 | 「同じ手法でもガバナンス文脈で機能が変わる」——提案時に手法選定の理由づけができる |
| W7134962924 | Unknowing the future: Speculative foresight in international institutions | Review of International Studies | 系譜学的分析 | 未来を「未知・複数・偶発的」と置く立場の正統性を語る材料 |
| W7171813780 | Colours within planetary boundaries? Three Horizons framework applied to natural dyes `#サステナビリティ` | European J. of Futures Research | 批判的レビュー+再帰的主題分析 | Three Horizons を実産業分析に落とした具体例（対象は天然染料に限定） |

---

### C4. 組織デザインと両利き（3本）

**戦略デザインの受け皿。**「良い戦略を作っても組織が動かない」問題に対応する層。

| ID | 論文 | 誌 | 手法 | 実務での使いどころ |
|---|---|---|---|---|
| W7171791157 | Strategic leadership and organizational design: a review and research agenda | J. of Organization Design | 系統的文献レビュー | リーダー特性→組織設計→業績のメカニズム整理。組織設計提案の理論的土台 |
| W7166885660 | Liminal Ambidexterity: Organizing Between Executional Simplicity and Adaptive Complexity | Transformations in Business & Economics | 概念論文 | 「既存事業は回るが将来の方向が見えない」移行期の言語化。SDI/CCI/CLIの3指標と translational governance |
| W7140141462 | Organisational culture, business model design and performance `#SME` | Entrepreneurial Business & Economics Review | SEM(n=175, アルバニア) | 組織文化→両利き→新規BM設計→業績の連鎖。文化変革とBMIを繋ぐ論拠 |

---

### C5. ビジネスモデル・共創エコシステム（5本）

**ビジネスデザインの本丸。**社外との境界をどう設計するかが共通テーマ。

| ID | 論文 | 誌 | 手法 | 実務での使いどころ |
|---|---|---|---|---|
| W7134249052 | Co-Design at the Boundary: Open Innovation Between Companies and Communities | JPIM | エスノグラフィ(5年) | コデザイン3類型×境界ワーク3類型。共創プログラムの設計と撤退判断の枠組み |
| W7134073515 | Enhancing collaboration and knowledge sharing through intra-organizational platforms | Review of Managerial Science | デザインサイエンス研究(1事例) | 「プラットフォーム思考」を社内に適用。マッチメイキングを儀式（ritual）として設計する発想 |
| W7152685614 | Leveraging commitment- and collaboration-oriented HRM for BMI in SMEs `#SME` | Asia Pacific J. of Management | 質問票調査(192社/中国) | BMIを支える人事制度の設計要件。BMI提案時の「組織的前提条件」チェックリスト |
| W7147671246 | Dynamic capabilities for co-innovation in timber construction `#サステナビリティ` | Frontiers in Built Environment | 探索的事例研究(スウェーデンCLT) | エコシステム型共創のケイパビリティを3層（運用/動的×2）で整理 |
| W7165159730 | Circular Business Model Innovation in a Collaborative Rural Hub `#サステナビリティ` | J. of Circular Economy | 質的事例研究 | 複数中小企業が協働する循環型BMの実例。地域文脈の事業設計 |

---

### C6. システム思考・社会転換（2本）

**長期ロードマップ／社会インフラ文脈に効く層。**

| ID | 論文 | 誌 | 手法 | 実務での使いどころ |
|---|---|---|---|---|
| W7171600316 | Systems Thinking in Practice (STiP): A Praxeology for Our Times | Systemic Practice & Action Research | レビュー/概念 | システム思考を「ツール」でなく「実践者の身体化された実践」として捉え直す。SSMのハード/ソフト二元論への批判を含む |
| W7167831573 | Epistemological and methodological contributions of design research labs to transformation research `#サステナビリティ` | Urban Transformations | 比較横断分析 | デザイン研究ラボと実世界ラボの比較。社内デザインラボの位置づけを語る材料 |

---

## 3. 要約の検証結果

### レベルA — 事実誤り（そのまま使うと誤情報になる／要修正）

#### A-1. W7168377411 Demir "Design Thinking in Practice" — **調査対象と主要知見の双方が不一致**

| 項目 | レポート記載 | 論文の実際 |
|---|---|---|
| 調査対象 | 「欧州**12社のSME**を対象に」 | **DTコンサルタント7名**への半構造化専門家インタビュー（"The final sample consisted of seven experts"） |
| 主要知見 | 「組織開放性・経営陣の支持・チームの多様性・反復学習文化の**4要因**」 | Gioia法による**6つの集約ディメンション**。鍵となるのは leadership commitment / early managerial involvement / cross-functional collaboration |
| 限界（report.md） | 「12社という小規模サンプル、欧州限定」 | 12社という単位自体が存在しない |

`survey.json` の `abstract` 欄も「12 SMEs ... facilitated by a regional innovation support programme」「four contextual factors: organizational openness, top management support, team diversity, and iterative learning culture」と記載されているが、**この記述は論文中に存在しない**。分析単位が「企業」ではなく「コンサルタント」である点は、知見の一般化可能性の評価を大きく変える。

#### A-2. W7140141462 Gërdoçi "Organisational culture, business model design and performance" — **サンプル数が誤り**

- レポート: 「**287社**のSEMデータ」（`survey.json` 要約 / `report.md` 3箇所に伝播）
- 論文: 「a sample of **175** Albanian companies」「The resulting final sample comprised 175 firms」「(N = 175)」
- あわせて **アルバニア（移行経済）の知識集約産業**という文脈が要約から欠落。日本のB2B文脈への適用可能性を判断するうえで重要な情報。

#### A-3. W7163025447 Ouyang "Trends and Challenges in Service Design Methods" — **課題リストが論文と別物**

- レポート: 課題は「AIツール統合、**スケーリング、インパクト測定**」
- 論文の実際の課題（6項目）: ユーザー関与の持続 / 暗黙的ユーザー要求の抽出 / 学際的共創の支援 / モジュール型マルチインタフェースシステム / 価値共創の自動化 / 反復評価による持続可能性
- `abstract` 欄の「navigating **ethical dimensions** of AI in service design」も要検証だった——本文中に "ethic" の語は**0件**。

#### A-4. W7142215350 Kiani "Functional pretence" — **AIへの言及は論文に存在しない**

- レポート要約: 「**AI時代**のデザイン教育・人間固有の価値再定義にも示唆を持つ」
- `abstract` 欄: 「Implications for design education and **AI-assisted design** are discussed」
- 論文本文の "AI" / "artificial intelligence" 出現回数: **0件**。論文が扱うのは人間と非ヒト霊長類（チンパンジー等）の対比であり、AI論ではない。
- ※「人間固有の能力を定義する議論はAI時代に転用できる」という**読み手側の解釈**としては妥当。ただし論文の主張として書くのは不適切。

---

### レベルB — 過剰一般化・断定が強すぎる

#### B-1. W7151799517 Laursen "Strategy Jams" — パイロット研究を「実証」と表現

- レポート: 「5チームで試行し、目的の明確化・役割構造・協働コミットメントの改善効果を**実証**」
- 論文: パイロット研究（著者自身が "As a pilot, this study has several limitations that limit reliability" と明記）。構造スコアは定量測定した4チーム中**3チームで平均8%改善、1チームは11%低下**。対照群なし。
- → 「示唆を得た」程度が妥当。

#### B-2. W7135085837 Amirkhizi "wicked problems of startups" — 効果の向きが逆

- レポート: 「デザイン思考（DDF）がウィキッドプロブレムの同定・リファインに**有効な一方**、問題定義の誤りが事業失敗の主因となる」
- 論文: 市場ニーズとのミスマッチは「**predominantly due to the misdefinition of problems applying design thinking**」。スタートアップは複雑な問題を単純化し、問題空間の探索をショートカットする傾向。
- → 論文の主眼は「DTは有効」ではなく「**DTを掲げていても問題定義を誤る**」という警告。示唆の方向が反転している。

#### B-3. W7134073515 Gadola "intra-organizational platforms" — 単一事例からの一般化

- レポート: 「**既存企業**が社内ユニット間の知識共有と協働を加速できることを…**実証**」
- 論文: 事例はイタリアの**事業者団体** Confcooperative Lombardia（協同組合を支援する business association）1件のデザインサイエンス研究。
- ※あわせて `survey.json` の `abstract` 欄「identifying **six design principles**」は論文と不一致。本文で "design principle" は**単数形で2箇所**のみ出現し、6原則という提示はない。

#### B-4. W7171813780 Virta "Colours within planetary boundaries?" — 対象範囲の膨張

- レポート要約: 「**ファッション・テキスタイル産業の持続可能性転換**をThree Horizonsで分析する批判的レビュー」
- 論文: 対象は**天然染料・天然色材（natural colourants）**という限定的な素材ニッチ。産業全体の転換分析ではなく、素材を通したレンズ。
- → タイトルには "natural dyes" があるが要約から落ちているため、実際より汎用性が高く見える。

---

### レベルC — 軽微な不正確・重要情報の欠落

| # | 文献 | 内容 |
|---|---|---|
| C-1 | W7134962924 Pantzerhielm | **単著論文**なのに著者欄が「Laura Pantzerhielm **et al.**」。また要約は権威づけの4要素（innovation / imagination / pluralism / methodological correctness）のうち「方法論的」のみを抽出しており、範囲が狭い |
| C-2 | W7134249052 Brubaker | 「環境・**組織**要因により動態的に移行」→ 論文は "characteristics of the environment and **open community**"（コミュニティ特性）。また中核の理論貢献である**境界ワーク3類型**（協働的/配置的/競争的）が要約・abstract双方から欠落 |
| C-3 | W7166885660 Skučaitė | `abstract` 欄の「**routine theory**」は論文に無い（実際は resilience と management control）。中核概念である**SDI/CCI/CLIの3指標**と **translational governance** が欠落。タイトルも誌面は "Liminal ambidexterity: **operating** between…"（記録は "Organizing Between…"） |
| C-4 | W7167048822 Yin | 採用障壁は実際「prompting / trust / **ethics** / training gaps」の4つ（要約は2つ）。ADTの構造である「**4つの職能ロール×5段階**」が欠落 |
| C-5 | W7171600316 Ison | 「ChecklandのSSMを**継承しつつ**」→ 論文はSSMの「ハード/ソフト二元論の罠」を明確に批判し再枠組み化する立場。批判的側面が伝わらない |

---

## 4. 構造的な原因と再発防止

### 原因: `abstract` 欄が「原文復元」でなく「LLM再記述」になっている

`prompts/survey-prompt.md` の仕様では `abstract` は **「復元済みアブストラクト全文」**（OpenAlex の `abstract_inverted_index` を復元したもの）と定められている。しかし実際には多くがLLMによる書き直しになっており、**そこに創作が混入している**。

PDF本文との3-gram一致率（低いほど原文から離れている）:

| 一致率 | 文献 | 検出された問題 |
|---|---|---|
| 12.3% | W7142215350 Kiani | **A-4**（AI言及の創作） |
| 27.2% | W7163025447 Ouyang | **A-3**（課題リストの創作） |
| 29.7% | W7168377411 Demir | **A-1**（調査対象・知見の創作） |
| 36.2% | W7140141462 Gërdoçi | **A-2**（サンプル数の誤り） |
| 50.0% | W7166885660 Skučaitė | C-3（理論的道具立ての置換） |
| 51.5% | W7134249052 Brubaker | C-2（中核類型の欠落） |
| 56.6% | W7167048822 Yin | C-4（障壁の欠落） |
| 62.7〜100% | 残り13本 | 重大な問題なし |

**一致率60%未満の7本すべてに問題が見つかり、レベルAの4件は一致率ワースト4と完全に一致した。** 一致率は不正確な要約の実用的な検出指標として機能する。

### 推奨する改善（優先順）

1. **`abstract` は復元原文をそのまま格納し、加工しない**（仕様どおりに戻す）。LLMの再記述が必要なら `abstract_paraphrase` 等の別フィールドに分離する。→ レベルAの4件はこれだけで全て防げた。
2. **数値クレームの自動照合**。要約中の「n=◯◯」「◯社」「◯名」を復元アブストラクト／PDF本文と機械的に突合し、根拠が見つからない数値は要約に書かせない。
3. **研究デザインのラベル統一**。パイロット・単一事例・専門家インタビューには「実証」を使わず、「示唆」「探索的知見」を使う。要約テンプレートに分析単位（企業／個人／プロジェクト）を必ず含める。
4. **著者数のチェック**。単著論文への "et al." を防ぐ（C-1）。
5. **掲載誌の品質フラグ**。W7163025447 の掲載誌 IJARBSS（HRMARS）は査読品質に懸念があり、社内共有の出典としては弱い。★評価とは別に出典強度の注記欄を設けるとよい。

---

## 5. 全20文献 一覧（カテゴリ・検証結果つき）

| # | ID | 短縮タイトル | カテゴリ | タイプ | 検証 |
|---|---|---|---|---|---|
| 1 | W7134858137 | Reframing Through New Minds | C2 | 実証(エスノグラフィ) | ✅ 問題なし |
| 2 | W7134249052 | Co-Design at the Boundary | C5 | 実証(エスノグラフィ5年) | ⚠️ C-2 |
| 3 | W7134073515 | Intra-organizational platforms | C5 | DSR(単一事例) | ⚠️ B-3 |
| 4 | W7135085837 | Wicked problems of startups | C1 | RtD(5社/18ヶ月) | ⚠️ B-2 |
| 5 | W7134962924 | Unknowing the future | C3 | 概念/系譜学 | ⚠️ C-1 |
| 6 | W7140141462 | Organisational culture & BM design | C4 | 実証(SEM n=175) | 🔴 **A-2** |
| 7 | W7142215350 | Functional pretence | C2 | 理論的統合 | 🔴 **A-4** |
| 8 | W7147671246 | Dynamic capabilities in timber | C5 | 事例研究 | ✅ 問題なし |
| 9 | W7152685614 | HRM for BMI in SMEs | C5 | 実証(調査 n=192) | ✅ 問題なし |
| 10 | W7151799517 | Strategy Jams | C1 | パイロット(5チーム) | ⚠️ B-1 |
| 11 | W7163025447 | Service Design Methods | C1 | 主題分析(63手法) | 🔴 **A-3** |
| 12 | W7165159730 | Circular BMI in Rural Hub | C5 | 質的事例研究 | ✅ 問題なし |
| 13 | W7166885660 | Liminal Ambidexterity | C4 | 概念 | ⚠️ C-3 |
| 14 | W7167048822 | ADT toolkit | C1 | 調査+開発+評価 | ⚠️ C-4 |
| 15 | W7167783984 | Governance logics & foresight | C3 | 対比事例+文献計量 | ✅ 問題なし |
| 16 | W7167831573 | Design research labs | C6 | 比較横断分析 | ✅ 問題なし |
| 17 | W7168377411 | DT in Practice (SMEs) | C1 | 専門家IV(7名) | 🔴 **A-1** |
| 18 | W7171791157 | Strategic leadership & org design | C4 | 系統的文献レビュー | ✅ 問題なし |
| 19 | W7171600316 | Systems Thinking in Practice | C6 | レビュー/概念 | ⚠️ C-5 |
| 20 | W7171813780 | Three Horizons & natural dyes | C3 | 批判的レビュー | ⚠️ B-4 |

**凡例**: 🔴 事実誤り（要修正） / ⚠️ 要注意（過剰一般化・欠落） / ✅ 本文と整合

**内訳**: 問題なし 7本 / 軽微〜過剰一般化 9本 / 事実誤り 4本
