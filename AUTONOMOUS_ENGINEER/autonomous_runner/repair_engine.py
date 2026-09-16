
import json, time
from pathlib import Path
from .model_agent import local_qwen, extract_json

SYSTEM = """You are the repair planner for a software project.
Return JSON only. Never claim success without evidence.
Prefer minimal reversible changes. Never touch protected foundation files unless the
human explicitly approves. Give a diagnosis and a concrete repair plan."""

def diagnose(goal, failure, project_summary):
    prompt = f"""
Goal:
{goal}

Observed failure:
{failure}

Project summary:
{json.dumps(project_summary, indent=2)}

Return:
{{
  "diagnosis": "...",
  "root_cause": "...",
  "repair_plan": ["..."],
  "files_to_change": ["..."],
  "verification": ["..."]
}}
"""
    raw = local_qwen([
        {"role":"system","content":SYSTEM},
        {"role":"user","content":prompt}
    ])
    return extract_json(raw)
