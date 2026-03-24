from pathlib import Path
import re
import subprocess
import markdown
import json
from datetime import datetime
from collections import Counter, defaultdict

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="QE Director Agent Web")
templates = Jinja2Templates(directory="web/templates")

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_FILE = ROOT / "feedback" / "feedback.jsonl"

SKILLS = [
    {"key": "quality_gate", "label": "发版评审", "desc": "填写版本关键信息，生成质量门结论与放行建议。"},
    {"key": "pilot_diagnosis", "label": "项目诊断", "desc": "评估试点项目成熟度、瓶颈和下一步动作。"},
    {"key": "incident_review", "label": "事故复盘", "desc": "把事故转成结构化问题、分析与改进行动。"},
    {"key": "weekly_report", "label": "周报生成", "desc": "生成质量负责人视角的周报或阶段性汇报。"},
    {"key": "ai_radar", "label": "AI 影响判断", "desc": "判断新的 AI 技术或产品变化对质量工程的影响。"},
]

SECTION_PATTERNS = [
    ("结论", r"(?:^|\n)(?:#+\s*)?(?:1\.\s*)?(?:Conclusion|结论)\s*\n?"),
    ("关键点", r"(?:^|\n)(?:#+\s*)?(?:2\.\s*)?(?:Key points|Key Points|Key risks|Key Risks|关键点|关键风险)\s*\n?"),
    ("分析", r"(?:^|\n)(?:#+\s*)?(?:3\.\s*)?(?:Analysis|分析)\s*\n?"),
    ("建议动作", r"(?:^|\n)(?:#+\s*)?(?:4\.\s*)?(?:Recommended actions|Actions|建议动作)\s*\n?"),
    ("优先级", r"(?:^|\n)(?:#+\s*)?(?:5\.\s*)?(?:Priority|优先级)\s*\n?"),
    ("负责人提醒", r"(?:^|\n)(?:#+\s*)?(?:6\.\s*)?(?:Director reminder|Reminder|负责人提醒)\s*\n?"),
]

def split_sections(text: str):
    matches = []
    for label, pattern in SECTION_PATTERNS:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            matches.append((m.start(), m.end(), label))
    matches.sort(key=lambda x: x[0])
    if not matches:
        return []
    sections = []
    for i, (_, end_pos, label) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        content = text[end_pos:next_start].strip()
        sections.append({
            "label": label,
            "raw": content,
            "html": markdown.markdown(content, extensions=["tables", "fenced_code"]),
        })
    return sections

def detect_decision(sections):
    conclusion = next((s for s in sections if s["label"] == "结论"), None)
    if not conclusion:
        return None, "unknown"
    raw = conclusion["raw"].lower()
    if "no go" in raw or "不通过" in raw:
        return "No Go", "no-go"
    if "conditional go" in raw or "有条件通过" in raw:
        return "Conditional Go", "conditional"
    if re.search(r"\bgo\b", raw) or "通过" in raw:
        return "Go", "go"
    return None, "unknown"

def save_feedback(payload: dict):
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with FEEDBACK_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

def load_feedback():
    if not FEEDBACK_FILE.exists():
        return []
    rows = []
    with FEEDBACK_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows

def feedback_summary(rows):
    by_skill = defaultdict(list)
    for row in rows:
        by_skill[row.get("skill", "unknown")].append(row)

    summary = []
    for skill, items in sorted(by_skill.items()):
        ratings = Counter(x.get("rating", "") for x in items)
        issues = Counter(x.get("issue_type", "") for x in items)
        summary.append({
            "skill": skill,
            "count": len(items),
            "ratings": dict(ratings),
            "top_issues": issues.most_common(3),
        })
    return summary

def render_run_error(request: Request, title: str, message: str, detail: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="run_error.html",
        context={"title": title, "message": message, "detail": detail},
        status_code=500,
    )

def handle_runtime_failure(request: Request, result: subprocess.CompletedProcess):
    detail = (result.stderr or result.stdout or "").strip()
    if "429" in detail or "engine_overloaded_error" in detail or "RateLimitError" in detail:
        return render_run_error(request, "模型服务繁忙", "当前模型服务繁忙，请稍后重试。", "建议等待 10~30 秒后再次提交。")
    if "401" in detail or "AuthenticationError" in detail or "Invalid Authentication" in detail:
        return render_run_error(request, "模型认证失败", "当前模型认证信息不可用，请检查 KIMI_API_KEY 配置。", "请先检查 .env 或运行环境中的 KIMI_API_KEY 是否有效。")
    return render_run_error(request, "运行失败", "当前任务执行失败，请稍后重试或联系维护者排查。", detail[-1200:] if detail else "")

@app.get("/favicon.ico")
def favicon():
    return FileResponse(ROOT / "web" / "static" / "favicon.png", media_type="image/png")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"skills": SKILLS})

@app.get("/feedback/list", response_class=HTMLResponse)
def feedback_list(request: Request):
    rows = list(reversed(load_feedback()))
    return templates.TemplateResponse(
        request=request,
        name="feedback_list.html",
        context={"rows": rows[:50]},
    )

@app.get("/feedback/summary", response_class=HTMLResponse)
def feedback_summary_page(request: Request):
    rows = load_feedback()
    summary = feedback_summary(rows)
    return templates.TemplateResponse(
        request=request,
        name="feedback_summary.html",
        context={"summary": summary, "total": len(rows)},
    )

@app.get("/skill/{skill_key}", response_class=HTMLResponse)
def skill_page(request: Request, skill_key: str):
    skill = next((s for s in SKILLS if s["key"] == skill_key), None)
    if not skill:
        return HTMLResponse("Skill not found", status_code=404)
    if skill_key == "quality_gate":
        return templates.TemplateResponse(request=request, name="quality_gate_form.html", context={"skill": skill})
    if skill_key == "weekly_report":
        return templates.TemplateResponse(request=request, name="weekly_report_form.html", context={"skill": skill})
    return templates.TemplateResponse(request=request, name="skill.html", context={"skill": skill})

@app.post("/run/quality_gate", response_class=HTMLResponse)
def run_quality_gate(
    request: Request,
    case_name: str = Form(...),
    project_name: str = Form(...),
    release_name: str = Form(...),
    change_scope: str = Form(...),
    open_high_risk_issues: str = Form(...),
    regression_result: str = Form(...),
    monitoring_and_rollback_readiness: str = Form(...),
):
    input_file = ROOT / "06_inputs" / f"{case_name}.md"
    output_file = ROOT / "03_templates" / f"{case_name}_result.md"
    input_text = f"""# Real Case Quality Gate Input

## Project name
{project_name}

## Release name
{release_name}

## Change scope
{change_scope}

## Open high-risk issues
{open_high_risk_issues}

## Regression result
{regression_result}

## Monitoring and rollback readiness
{monitoring_and_rollback_readiness}
"""
    input_file.write_text(input_text, encoding="utf-8")
    cmd = ["./scripts/agent", "--skill", "quality_gate", "--input", str(input_file), "--output", str(output_file)]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        return handle_runtime_failure(request, result)

    output_text = output_file.read_text(encoding="utf-8")
    sections = split_sections(output_text)
    output_html = markdown.markdown(output_text, extensions=["tables", "fenced_code"])
    decision_text, decision_class = detect_decision(sections)
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "title": "发版评审结果",
            "skill_key": "quality_gate",
            "case_name": case_name,
            "meta_1_label": "项目",
            "meta_1_value": project_name,
            "meta_2_label": "版本",
            "meta_2_value": release_name,
            "output_text": output_text,
            "output_html": output_html,
            "sections": sections,
            "decision_text": decision_text,
            "decision_class": decision_class,
        },
    )

@app.post("/run/weekly_report", response_class=HTMLResponse)
def run_weekly_report(
    request: Request,
    case_name: str = Form(...),
    reporting_period: str = Form(...),
    key_progress: str = Form(...),
    core_metrics: str = Form(...),
    key_problems: str = Form(...),
    risks: str = Form(...),
    actions_completed: str = Form(...),
    next_step_plan: str = Form(...),
    audience: str = Form(...),
):
    input_file = ROOT / "06_inputs" / f"{case_name}.md"
    output_file = ROOT / "03_templates" / f"{case_name}_result.md"
    input_text = f"""# Real Case Report Input

## Reporting period
{reporting_period}

## Key progress
{key_progress}

## Core metrics
{core_metrics}

## Key problems
{key_problems}

## Risks
{risks}

## Actions completed
{actions_completed}

## Next-step plan
{next_step_plan}

## Audience
{audience}
"""
    input_file.write_text(input_text, encoding="utf-8")
    cmd = ["./scripts/agent", "--skill", "weekly_report", "--input", str(input_file), "--output", str(output_file)]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        return handle_runtime_failure(request, result)

    output_text = output_file.read_text(encoding="utf-8")
    sections = split_sections(output_text)
    output_html = markdown.markdown(output_text, extensions=["tables", "fenced_code"])
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "title": "周报生成结果",
            "skill_key": "weekly_report",
            "case_name": case_name,
            "meta_1_label": "汇报对象",
            "meta_1_value": audience,
            "meta_2_label": "周期",
            "meta_2_value": reporting_period,
            "output_text": output_text,
            "output_html": output_html,
            "sections": sections,
            "decision_text": None,
            "decision_class": "unknown",
        },
    )

@app.post("/feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    skill_key: str = Form(...),
    case_name: str = Form(...),
    rating: str = Form(...),
    issue_type: str = Form(...),
    suggestion: str = Form(""),
):
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "skill": skill_key,
        "case_name": case_name,
        "rating": rating,
        "issue_type": issue_type,
        "suggestion": suggestion.strip(),
    }
    save_feedback(payload)
    return templates.TemplateResponse(
        request=request,
        name="feedback_saved.html",
        context={"payload": payload},
    )
