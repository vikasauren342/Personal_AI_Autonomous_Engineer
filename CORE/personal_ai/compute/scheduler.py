from dataclasses import dataclass, field
from typing import Any, Dict, List

from .registry import WorkerRegistry
from personal_ai.workers import WorkerJob

@dataclass
class ComputeRequirements:
    gpu: bool = True
    min_vram_gb: float = 0.0
    job_type: str = "inference"
    preferred_workers: List[str] = field(default_factory=list)

class ComputeScheduler:
    def __init__(self, registry: WorkerRegistry):
        self.registry = registry

    def select(self, requirements: ComputeRequirements) -> str:
        workers = self.registry.all()
        if requirements.preferred_workers:
            for name in requirements.preferred_workers:
                if name in workers:
                    return name
        if workers:
            return next(iter(workers))
        raise RuntimeError("No compute workers registered")

    def submit(self, payload: Dict[str, Any], requirements: ComputeRequirements) -> str:
        worker_name = self.select(requirements)
        worker = self.registry.get(worker_name)
        job = WorkerJob(job_id=payload["job_id"], payload=payload)
        return worker.submit(job)
        job = WorkerJob(job_id=payload["job_id"], payload=payload)
        return worker.submit(job)
