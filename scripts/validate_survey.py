#!/usr/bin/env python3
"""survey.json の記述品質を検証する。

prompts/survey-prompt.md の「記述の正確性ルール」(R1〜R6) を機械的にチェックする。
過去に「N=175 を 287社」「専門家7名へのインタビューを12社のSME」「AIに一切言及しない
論文の要約に "AI時代の〜"」といった事故が起きたため、その再発を検出する。

使い方:
    python3 scripts/validate_survey.py reports/2026-08-03/survey.json
    python3 scripts/validate_survey.py                 # reports/ 配下を全件検証
    python3 scripts/validate_survey.py --pdf           # PDF本文とも突合（要 pypdf）

終了コード: ERROR が1件でもあれば 1、なければ 0。
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

# summary_ja から数値クレームを拾うパターン。
# 「3層」「5つの段階」のような概念的な数え上げではなく、標本規模に関わる単位のみを対象にする。
SAMPLE_UNIT_RE = re.compile(
    r"(?<![0-9])([0-9][0-9,]*)\s*(社|名|人|チーム|件|カ国|ヶ国|か国|事例|プロジェクト|大学|機関)"
)
# 「n=175」「N = 175」形式
N_EQUALS_RE = re.compile(r"[nN]\s*=\s*([0-9][0-9,]*)")

# 論文が言及していないのに要約へ持ち込まれやすい流行語 (R5)
BUZZWORDS = {
    "AI": [r"\bAI\b", r"artificial intelligence"],
    "DX": [r"\bDX\b", r"digital transformation"],
    "生成AI": [r"generative ai", r"\bLLM\b", r"large language model"],
    "機械学習": [r"machine learning", r"\bML\b"],
}

# 研究デザイン別の禁止表現 (R3)
STRONG_CLAIMS = ["実証した", "実証", "証明した", "検証した"]
WEAK_DESIGN_TYPES = {"conceptual", "review", "case study"}
# type だけでは足りないため、要約側の語からも弱いデザインを推定する。
# 「インタビュー」「エスノグラフィ」等は単独では弱さを意味しない（大規模質的研究もある）ため、
# 明確に弱いデザインを指す語だけを列挙する。
WEAK_DESIGN_HINTS = [
    "パイロット", "予備調査", "試行", "単一事例", "1事例", "一事例",
    "概念論文", "文献レビュー", "文献研究", "デザインサイエンス", "専門家インタビュー",
]

REQUIRED_FIELDS = [
    "rank", "title", "authors", "journal", "publication_date", "type",
    "doi", "openalex_id", "is_oa", "oa_status", "abstract", "summary_ja",
    "practical_relevance", "search_layer", "pdf_downloaded",
]
# 新仕様で追加されたフィールド。既存レポートには無いのでファイル単位で1回だけ WARN する。
NEW_FIELDS = ["analysis_unit", "source_strength", "author_count"]

VALID_OA = {"gold", "green", "hybrid", "bronze", "diamond", "closed"}
VALID_STRENGTH = {"high", "medium", "low"}


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warns: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warns.append(msg)


def ngrams(text: str, n: int = 3) -> set[tuple[str, ...]]:
    words = re.findall(r"[a-z]+", text.lower())
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def load_pdf_text(report_dir: str, work_id: str) -> str | None:
    """同じフォルダにある {WorkID}.pdf からテキストを抽出する。無ければ None。"""
    path = os.path.join(report_dir, f"{work_id}.pdf")
    if not os.path.exists(path):
        return None
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception:
        return None


def normalize_num(raw: str) -> str:
    return raw.replace(",", "")


# 論文アブストラクトは "five European countries" のように数を英単語で書くことが多いため、
# 数字表記だけで突合すると誤検知になる。小さい数は単語表記も数値として拾う。
NUMBER_WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
    "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
    "nineteen": "19", "twenty": "20", "thirty": "30", "forty": "40",
    "fifty": "50", "sixty": "60", "seventy": "70", "eighty": "80",
    "ninety": "90", "hundred": "100", "thousand": "1000",
}


def collect_numbers(text: str) -> set[str]:
    """テキスト中に現れる数値の集合（カンマ区切りを正規化し、英単語表記も含む）。"""
    found = set()
    for m in re.finditer(r"[0-9][0-9,]*", text):
        found.add(normalize_num(m.group(0)))
    lowered = text.lower()
    # "forty-one" のような複合数詞を先に展開する（"forty" と "one" に分けると 41 を取り逃す）
    tens = "twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"
    ones = "one|two|three|four|five|six|seven|eight|nine"
    for m in re.finditer(rf"\b({tens})[- ]({ones})\b", lowered):
        found.add(str(int(NUMBER_WORDS[m.group(1)]) + int(NUMBER_WORDS[m.group(2)])))
    for word, digit in NUMBER_WORDS.items():
        if re.search(rf"\b{word}\b", lowered):
            found.add(digit)
    return found


def check_paper(paper: dict, report_dir: str, use_pdf: bool, f: Findings) -> None:
    rank = paper.get("rank", "?")
    wid = str(paper.get("openalex_id", "")).rstrip("/").split("/")[-1]
    tag = f"rank {rank} ({wid})"

    # --- 必須フィールド ---
    for field in REQUIRED_FIELDS:
        if field not in paper:
            f.error(f"{tag}: 必須フィールド '{field}' が無い")

    if paper.get("oa_status") not in VALID_OA:
        f.error(f"{tag}: oa_status が不正 -> {paper.get('oa_status')!r}")
    if "source_strength" in paper and paper["source_strength"] not in VALID_STRENGTH:
        f.error(f"{tag}: source_strength が不正 -> {paper['source_strength']!r}")

    abstract = paper.get("abstract") or ""
    summary = paper.get("summary_ja") or ""
    authors = paper.get("authors") or ""
    ptype = (paper.get("type") or "").lower()

    if not abstract.strip():
        f.warn(f"{tag}: abstract が空（原文取得不能なら仕様どおり）")

    # --- R4: 単著への et al. ---
    # author_count が無いと著者数を判定できないため、ある場合のみ検査する。
    count = paper.get("author_count")
    if isinstance(count, int) and "et al" in authors.lower():
        if count == 1:
            f.error(f"{tag}: 単著論文 '{authors}' に et al. が付いている（R4）")
        elif count == 2:
            f.warn(f"{tag}: 著者2名なら 'A and B' 表記が正しい -> '{authors}'（R4）")

    # --- R2: 数値クレームの照合 ---
    claims: set[str] = set()
    for m in SAMPLE_UNIT_RE.finditer(summary):
        claims.add(normalize_num(m.group(1)))
    for m in N_EQUALS_RE.finditer(summary):
        claims.add(normalize_num(m.group(1)))

    # PDF本文は3つのチェックで使い回すため一度だけ読む
    pdf_text = load_pdf_text(report_dir, wid) if use_pdf else None

    # 突合の主軸はアブストラクト原文。要約を書く時点で参照できるのはアブストラクトであり、
    # PDF本文まで同列に扱うとページ番号や引用年に偶然一致して検出漏れが起きる
    # （実際に「287社」の誤記が本文中の無関係な "287" に一致して素通りした）。
    # 本文にだけ現れる数値は「捏造ではないが生成時に根拠が無かった」ので WARN に留める。
    if claims:
        evidence = collect_numbers(abstract)
        body_evidence = collect_numbers(pdf_text) if pdf_text else set()
        for c in sorted(claims, key=lambda x: -len(x)):
            if c in evidence:
                continue
            if c in body_evidence:
                f.warn(
                    f"{tag}: 要約の数値 '{c}' はabstractに無くPDF本文にのみ存在（R2）"
                    f" — 本文確認済みなら可"
                )
            else:
                f.error(
                    f"{tag}: 要約の数値 '{c}' がabstract原文に見つからない（R2）"
                    f" — summary: {summary[:60]}…"
                )

    # --- R5: 論文に無い流行語 ---
    # 照合先はタイトル+アブストラクト（+あればPDF本文）。アブストラクトは要約であり
    # 本文の語を網羅しないため、PDFが無い場合は ERROR ではなく WARN に留める。
    haystack = f"{paper.get('title', '')}\n{abstract}"
    if pdf_text:
        haystack += "\n" + pdf_text
    if haystack.strip():
        for label, patterns in BUZZWORDS.items():
            if label not in summary:
                continue
            if any(re.search(p, haystack, re.I) for p in patterns):
                continue
            msg = (f"{tag}: 要約に '{label}' があるが"
                   f"{'論文本文' if pdf_text else 'タイトル/アブストラクト'}に該当語が無い（R5）")
            if pdf_text:
                f.error(msg + " — 解釈なら実務メモ欄へ")
            else:
                f.warn(msg + " — PDF未取得のため要目視確認")

    # --- R3: 弱いデザインへの断定語 ---
    hint_source = f"{summary} {paper.get('analysis_unit', '')}"
    is_weak = ptype in WEAK_DESIGN_TYPES or any(h in hint_source for h in WEAK_DESIGN_HINTS)
    if is_weak:
        for claim in STRONG_CLAIMS:
            if claim in summary:
                f.warn(
                    f"{tag}: type='{ptype}' で断定語 '{claim}' を使用（R3）"
                    f" — 「示唆を得た」「質的に明らかにした」等が適切か要確認"
                )
                break

    # --- R1: abstract が原文かどうか（PDFがある場合のみ） ---
    if abstract.strip():
        if pdf_text:
            a = ngrams(abstract)
            if a:
                overlap = len(a & ngrams(pdf_text)) / len(a)
                if overlap < 0.60:
                    f.error(
                        f"{tag}: abstract のPDF本文一致率 {overlap * 100:.1f}% "
                        f"— 原文でなくLLM再記述の疑い（R1）"
                    )
                elif overlap < 0.80:
                    f.warn(f"{tag}: abstract のPDF本文一致率 {overlap * 100:.1f}%（R1）")


def validate_file(path: str, use_pdf: bool) -> Findings:
    f = Findings()
    report_dir = os.path.dirname(path)
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as e:
        f.error(f"JSONとして読めない: {e}")
        return f

    if "papers" not in data or not isinstance(data["papers"], list):
        f.error("'papers' 配列が無い")
        return f

    ranks = [p.get("rank") for p in data["papers"]]
    if len(set(ranks)) != len(ranks):
        f.error(f"rank が重複している: {ranks}")

    # 新仕様フィールドの欠落は論文ごとに出すと冗長なのでファイル単位で1回だけ報告する
    for field in NEW_FIELDS:
        missing = sum(1 for p in data["papers"] if field not in p)
        if missing:
            f.warn(f"新仕様フィールド '{field}' が {missing}/{len(data['papers'])} 件で欠落"
                   f"（旧仕様で生成されたレポート）")

    for paper in data["papers"]:
        check_paper(paper, report_dir, use_pdf, f)
    return f


def main() -> int:
    ap = argparse.ArgumentParser(description="survey.json の記述品質を検証する")
    ap.add_argument("paths", nargs="*", help="survey.json のパス（省略時は reports/ 全件）")
    ap.add_argument("--pdf", action="store_true",
                    help="同フォルダのPDF本文とも突合する（要 pypdf、低速）")
    args = ap.parse_args()

    paths = args.paths or sorted(glob.glob("reports/*/survey.json"))
    if not paths:
        print("検証対象が見つかりません", file=sys.stderr)
        return 1

    total_err = total_warn = 0
    for path in paths:
        f = validate_file(path, args.pdf)
        total_err += len(f.errors)
        total_warn += len(f.warns)
        if f.errors or f.warns:
            print(f"\n=== {path} ===")
            for msg in f.errors:
                print(f"  ERROR  {msg}")
            for msg in f.warns:
                print(f"  WARN   {msg}")

    print(f"\n検証対象 {len(paths)} ファイル / ERROR {total_err} 件 / WARN {total_warn} 件")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
