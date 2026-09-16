import subprocess
import uuid
from typing import Any, Dict

from personal_ai.workers import Worker, WorkerJob


class SSHWorker(Worker):
    """Remote Linux/GPU worker using persistent background jobs over SSH."""

    name = "ssh_gpu"

    def __init__(self, host: str, user: str, workdir: str):
        self.host = host
        self.user = user
        self.workdir = workdir

    def _ssh(self, command: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["ssh", f"{self.user}@{self.host}", command],
            capture_output=True,
            text=True,
            timeout=30,
        )

    def submit(self, job: WorkerJob) -> str:
        command = job.payload["command"]
        job_id = job.job_id or str(uuid.uuid4())

        job_dir = f"{self.workdir}/.personal_ai_jobs/{job_id}"

        remote = (
            f"mkdir -p {job_dir} && "
            f"cd {self.workdir} && "
            f"nohup bash -lc {command!r} "
            f"> {job_dir}/stdout.log "
            f"2> {job_dir}/stderr.log "
            f"< /dev/null & "
            f"echo $! > {job_dir}/pid"
        )

        result = self._ssh(remote)

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return job_id

    def status(self, job_id: str) -> Dict[str, Any]:
        job_dir = f"{self.workdir}/.personal_ai_jobs/{job_id}"

        result = self._ssh(
            f"if kill -0 $(cat {job_dir}/pid) 2>/dev/null; "
            f"then echo RUNNING; "
            f"else echo STOPPED; fi"
        )

        if result.returncode != 0:
            return {"job_id": job_id, "status": "UNKNOWN"}

        return {
            "job_id": job_id,
            "status": result.stdout.strip(),
        }

    def collect(self, job_id: str) -> Any:
        job_dir = f"{self.workdir}/.personal_ai_jobs/{job_id}"

        result = self._ssh(
            f"cat {job_dir}/stdout.log 2>/dev/null; "
            f"echo '__STDERR__'; "
            f"cat {job_dir}/stderr.log 2>/dev/null"
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return {
            "job_id": job_id,
            "output": result.stdout,
        }

    def cancel(self, job_id: str) -> bool:
        job_dir = f"{self.workdir}/.personal_ai_jobs/{job_id}"

        result = self._ssh(
            f"kill $(cat {job_dir}/pid) 2>/dev/null"
        )

        return result.returncode == 0