from typing import Dict

from personal_ai.workers import Worker


class WorkerRegistry:
    """Provider-neutral registry for compute workers."""

    def __init__(self):
        self._workers: Dict[str, Worker] = {}

    def register(self, worker: Worker) -> None:
        self._workers[worker.name] = worker

    def get(self, name: str) -> Worker:
        return self._workers[name]

    def all(self) -> Dict[str, Worker]:
        return dict(self._workers)
