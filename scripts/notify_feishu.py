#!/usr/bin/env python3
"""Send eval result summary to Feishu group."""
import json, os, sys, urllib.request, urllib.error
from pathlib import Path

APP_ID = os.environ.get("FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
CHAT_ID = os.environ.get("FEISHU_CHAT_ID", "")
RUN_DIR = os.environ.get("RUN_DIR", "")
RUN_URL = os.environ.get("RUN_URL", "")
WORKFLOW = os.environ.get("WORKFLOW_NAME", "Skill Eval")

if not all([APP_ID, APP_SECRET, CHAT_ID]):
    print("Feishu credentials not set, skipping")
    sys.exit(0)

def api_post(url, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

resp = api_post(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    {"app_id": APP_ID, "app_secret": APP_SECRET}
)
if resp.get("code") != 0:
    print(f"Token error: {resp}")
    sys.exit(1)
token = resp["tenant_access_token"]

# Find report file
report_path = None
if RUN_DIR:
    p = Path(RUN_DIR) / "report.md"
    if p.exists():
        report_path = p
if not report_path:
    for candidate in ["skill-judge-report.md", "report.md"]:
        if Path(candidate).exists():
            report_path = Path(candidate)
            break

# Detect if this is a judge workflow (different format)
is_judge = "judge" in WORKFLOW.lower() or "quality" in WORKFLOW.lower()

if is_judge:
    # Simple notification for judge — just link
    found = report_path and report_path.exists()
    card = {
        "header": {
            "title": {"tag": "plain_text", "content": f"📋 {WORKFLOW} {'完成' if found else '未生成报告'}"},
            "template": "blue" if found else "orange"
        },
        "elements": [
            {"tag": "action", "actions": [
                {"tag": "button", "text": {"tag": "plain_text", "content": "查看详情"},
                 "url": RUN_URL, "type": "primary"}
            ]}
        ]
    }
else:
    # Eval workflow — extract summary + timing
    status = "⚠️ No report"
    cases_summary = ""
    timing = ""

    if report_path and report_path.exists():
        lines = report_path.read_text().splitlines()
        # Try multiple patterns to find the summary line
        for line in lines:
            l = line.strip().lstrip("- ")
            if ("pass" in l and "fail" in l) or ("cases:" in l) or ("pass:" in l):
                cases_summary = l
                break
        for i, line in enumerate(lines):
            if "task_execution" in line or "Timing" in line:
                for j in range(i+1, min(i+10, len(lines))):
                    l = lines[j].strip()
                    if l.startswith("|") and "---" not in l and "task_execution" not in l and "case_id" not in l:
                        parts = [p.strip() for p in l.split("|") if p.strip()]
                        if len(parts) >= 4:
                            timing = f"{parts[0]}: 执行 {parts[1]}, 验收 {parts[2]}, 总计 {parts[3]}"
                        break
                break
        if cases_summary:
            if "0 fail" in cases_summary and "0 blocked" in cases_summary:
                status = "✅ PASS"
            elif "fail" in cases_summary and "0 fail" not in cases_summary:
                status = "❌ FAIL"
            elif "blocked" in cases_summary and "0 blocked" not in cases_summary:
                status = "⚠️ BLOCKED"
            else:
                status = "✅ PASS"
        else:
            status = "📊 完成"
            cases_summary = "报告已生成"

    card = {
        "header": {
            "title": {"tag": "plain_text", "content": WORKFLOW},
            "template": "blue"
        },
        "elements": []
    }
    if cases_summary:
        card["elements"].append({"tag": "markdown", "content": cases_summary})
    if timing:
        card["elements"].append({"tag": "markdown", "content": f"**耗时:** {timing}"})
    card["elements"].append({
        "tag": "action", "actions": [
            {"tag": "button", "text": {"tag": "plain_text", "content": "查看详情"},
             "url": RUN_URL, "type": "primary"}
        ]
    })

result = api_post(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
    {"receive_id": CHAT_ID, "msg_type": "interactive",
     "content": json.dumps(card, ensure_ascii=False)},
    token
)
print("Sent" if result.get("code") == 0 else f"Error: {result}")
