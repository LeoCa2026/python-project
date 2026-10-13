"""Run local phishing detection on a CSV dataset."""

import argparse
import csv
import json
from pathlib import Path
import time

from ollama import Client, ResponseError

from .detector import SYSTEM_PROMPT, analyze_email

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_emails(path: Path) -> list[dict[str, str]]:
    csv.field_size_limit(100_000_000)
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not {"email_text", "label"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV must contain email_text and label columns.")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV has no email records.")
    for number, row in enumerate(rows, 1):
        if row.get("label") not in ("0", "1") or not row.get("email_text", "").strip():
            raise ValueError(f"Invalid label or empty email_text in record {number}.")
    return rows


def save_results(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def save_report(path: Path, payload: dict) -> None:
    """Write a readable summary alongside the machine-readable results."""
    labels = {0: "正常邮件", 1: "钓鱼邮件", None: "分析失败"}
    summary = payload["summary"]
    quote_count = sum(len(item.get("evidence", [])) for item in payload["results"])
    invalid_quote_count = summary["invalid_evidence_quotes"]
    lines = [
        "# 本地邮件识别结果", "",
        f"模型：{payload['model']}", "",
        f"成功分析 {summary['successful']}/{payload['total_records']} 条；"
        f"与数据集标签一致 {summary['correct']} 条。", "",
        f"原文引用共 {quote_count} 条；"
        f"其中 {invalid_quote_count} 条未通过逐字匹配检查。", "",
        "未通过检查的引用不能作为已验证原文证据；可能涉及换行、改写或编造。", "",
        "引用出现在原文中，也不代表它足以支持模型的判断。", "",
        "这些邮件用于试跑，不能据此推断正式测试集上的效果。", "",
        "| 序号 | 主题 | 模型判断 | 数据集标签 | 是否一致 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in payload["results"]:
        subject = item["subject"].replace("|", "&#124;").replace("\n", " ")
        match = "是" if item["correct"] is True else "否" if item["correct"] is False else "失败"
        lines.append(
            f"| {item['row']} | {subject} | {labels[item['predicted_label']]} | "
            f"{labels[item['true_label']]} | {match} |"
        )
    for item in payload["results"]:
        lines.extend(["", f"## 第 {item['row']} 条", ""])
        if item["status"] != "ok":
            lines.append("分析失败：" + item["error"])
            continue
        lines.extend(["判断：" + labels[item["predicted_label"]], "", "理由：" + item["reason"], ""])
        if not item["evidence"]:
            lines.append("模型没有提供原文引用。")
        for quote in item["evidence"]:
            found = "能在原文中逐字找到" if quote["found_in_email"] else "未能在原文中逐字找到"
            lines.extend(["原文证据（" + found + "）：", ""])
            lines.extend("    " + line for line in quote["quote"].splitlines())
            lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze CSV emails with local Ollama.")
    parser.add_argument("--input", type=Path, default=PROJECT_ROOT / "data/raw/train.csv")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "outputs/train_results.json")
    parser.add_argument("--model", default="qwen3:1.7b")
    args = parser.parse_args()
    if args.output.resolve() == args.input.resolve():
        parser.error("Output must not overwrite the input CSV.")
    try:
        rows = load_emails(args.input)
        client = Client(host="http://localhost:11434", timeout=180.0)
        models = {item.model for item in client.list().models}
        if args.model not in models:
            raise ValueError(f"Model {args.model} is not installed in local Ollama.")
    except (OSError, ValueError, ConnectionError, ResponseError) as error:
        print(f"Cannot start: {error}. Check the input file and running Ollama.", flush=True)
        return 1

    payload = {
        "input_file": str(args.input.resolve()),
        "model": args.model,
        "system_prompt": SYSTEM_PROMPT,
        "options": {"temperature": 0, "num_ctx": 4096, "num_predict": 600, "think": False},
        "total_records": len(rows),
        "results": [],
    }
    save_results(args.output, payload)
    for number, row in enumerate(rows, 1):
        print(f"Analyzing {number}/{len(rows)}...", flush=True)
        started = time.perf_counter()
        result = {"row": number, "subject": row.get("subject", ""), "true_label": int(row["label"])}
        try:
            analysis = analyze_email(client, row["email_text"], args.model)
            result.update(
                status="ok", predicted_label=analysis.label, reason=analysis.reason,
                evidence=analysis.evidence, correct=analysis.label == result["true_label"],
            )
            print(f"  prediction={analysis.label}, actual={result['true_label']}, correct={result['correct']}", flush=True)
        except Exception as error:
            # A failed request is recorded as an error, never as a normal email.
            result.update(status="error", predicted_label=None, error=str(error), correct=None)
            print(f"  error: {error}", flush=True)
        result["elapsed_seconds"] = round(time.perf_counter() - started, 2)
        payload["results"].append(result)
        save_results(args.output, payload)

    successful = [item for item in payload["results"] if item["status"] == "ok"]
    correct = sum(item["correct"] for item in successful)
    payload["summary"] = {
        "successful": len(successful), "failed": len(rows) - len(successful),
        "correct": correct,
        "accuracy_on_successful": correct / len(successful) if successful else None,
        "invalid_evidence_quotes": sum(
            not quote["found_in_email"] for item in successful for quote in item["evidence"]
        ),
    }
    save_results(args.output, payload)
    save_report(args.output.with_suffix(".md"), payload)
    print(f"Finished: {len(successful)}/{len(rows)} analyzed; {correct} correct.", flush=True)
    print(f"Results: {args.output.resolve()}", flush=True)
    return 0 if len(successful) == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
