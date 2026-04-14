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

status = "⚠️ No report"
cases_summary = ""
timing = ""
report_path = Path(RUN_DIR) / "report.md" if RUN_DIR else None

if report_path and report_path.exists():
    lines = report_path.read_text().splitlines()
    for line in lines:
        if "pass" in line and "fail" in line and "cases" in line:
            cases_summary = line.strip().lstrip("- ")
            break
    for i, line in enumerate(lines):
        if "task_execution" in line or "Timing" in line:
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip().startswith("|") and "---" not in lines[j]:
                    timing = lines[j].strip()
                    break
            break
    if "0 fail" in cases_summary and "0 blocked" in cases_summary:
        status = "✅ PASS"
    elif "fail" in cases_summary:
        status = "❌ FAIL"
    else:
        status = "⚠️ BLOCKED"

card = {
    "header": {
        "title": {"tag": "plain_text", "content": f"{status} {WORKFLOW}"},
        "template": "green" if "PASS" in status else ("red" if "FAIL" in status else "orange")
    },
    "elements": [
        {"tag": "markdown", "content": f"**结果:** {cases_summary}"},
    ]
}
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
