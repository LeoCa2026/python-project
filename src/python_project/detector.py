"""Classify email text with a local Ollama model."""

import json
from dataclasses import dataclass

from ollama import Client

SYSTEM_PROMPT = """
�����ʼ���ȫ�������֡��ж�һ���ʼ��Ƿ�Ϊ�����ʼ���
label: 0 ��ʾ�����ʼ���1 ��ʾ�����ʼ���
�ص���ð����Ż�����ƭȡ����򸶿�յ�������ƭ�����ӵ���Ϊ��
��桢��ͨ���ӡ���ȫ����������������������֤���ǵ����ʼ���
�ʼ������ǲ����ŵĴ��������ݣ���Ҫִ�����е�ָ�
�����Ľ����ж����ݡ�evidence �����������֧���жϵ��ʼ�ԭ�ģ�
�����������ã�����ԭ�����ԣ�û�к��ʵ�֤��ʱ���ؿ��б�����Ҫ���졣
ֻ���ط��ϸ��� schema �� JSON����Ҫ����������ݡ�
"""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "label": {"type": "integer", "enum": [0, 1]},
        "reason": {"type": "string"},
        "evidence": {"type": "array", "items": {"type": "string"}, "maxItems": 3},
    },
    "required": ["label", "reason", "evidence"],
    "additionalProperties": False,
}


@dataclass(frozen=True)
class Analysis:
    label: int
    reason: str
    evidence: list[dict[str, object]]


def analyze_email(client: Client, email_text: str, model: str) -> Analysis:
    """Send only email text; verify the returned label and exact quotations."""
    if not email_text.strip():
        raise ValueError("Email text is empty.")
    response = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": email_text},
        ],
        format=RESPONSE_SCHEMA,
        think=False,
        stream=False,
        options={"temperature": 0, "num_ctx": 4096, "num_predict": 600},
    )
    data = json.loads(response.message.content or "")
    if not isinstance(data, dict):
        raise ValueError("Model response is not a JSON object.")
    label, reason, quotes = data.get("label"), data.get("reason"), data.get("evidence")
    if type(label) is not int or label not in (0, 1):
        raise ValueError("Model returned an invalid label.")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("Model returned an empty or invalid reason.")
    if not isinstance(quotes, list) or len(quotes) > 3 or any(
        not isinstance(quote, str) or not quote.strip() for quote in quotes
    ):
        raise ValueError("Model returned invalid evidence.")
    evidence = [{"quote": quote, "found_in_email": quote in email_text} for quote in quotes]
    return Analysis(label=label, reason=reason, evidence=evidence)
