from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class Task:
    id: str
    goal: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Plan:
    task_id: str
    steps: List[Dict[str, Any]]
    assumptions: List[str] = field(default_factory=list)

@dataclass
class Observation:
    ok: bool
    output: Any = None
    error: str | None = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Evaluation:
    done: bool
    passed: bool
    issues: List[str] = field(default_factory=list)
    feedback: Dict[str, Any] = field(default_factory=dict)
