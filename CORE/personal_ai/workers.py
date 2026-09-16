from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class WorkerJob:
    job_id: str
    payload: Dict[str, Any]


class Worker(ABC):
    name: str

    @abstractmethod
    def submit(self, job: WorkerJob) -> str:
        raise NotImplementedError

    @abstractmethod
    def status(self, job_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def collect(self, job_id: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def cancel(self, job_id: str) -> bool:
        raise NotImplementedError
