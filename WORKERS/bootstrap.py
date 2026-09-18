import os
import platform
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    print(f"\n>>> {command}")
    subprocess.run(command, shell=True, check=True, cwd=ROOT)


def detect_provider():
    if os.environ.get("KAGGLE_KERNEL_RUN_TYPE"):
        return "kaggle"

    if os.environ.get("COLAB_GPU") or Path("/content").exists():
        return "colab"

    if os.environ.get("LIGHTNING_CLOUD_PROJECT_ID"):
        return "lightning"

    if os.environ.get("RUNPOD_POD_ID"):
        return "runpod"

    return "local"


def detect_gpu():
    try:
        import torch

        if torch.cuda.is_available():
            return {
                "cuda": True,
                "gpu": torch.cuda.get_device_name(0),
                "vram_gb": round(
                    torch.cuda.get_device_properties(0).total_memory
                    / (1024 ** 3),
                    2,
                ),
            }
    except Exception:
        pass

    return {
        "cuda": False,
        "gpu": None,
        "vram_gb": 0,
    }


def main():
    provider = detect_provider()
    gpu = detect_gpu()

    print("=" * 60)
    print("PERSONAL AI UNIVERSAL WORKER BOOTSTRAP")
    print("=" * 60)

    print(f"Provider : {provider}")
    print(f"Platform : {platform.platform()}")
    print(f"Python   : {sys.version.split()[0]}")
    print(f"CUDA     : {gpu['cuda']}")
    print(f"GPU      : {gpu['gpu']}")
    print(f"VRAM     : {gpu['vram_gb']} GB")

    os.environ["WORKER_NAME"] = provider

    provider_dir = ROOT / "WORKERS" / provider

    if not provider_dir.exists():
        raise RuntimeError(
            f"Provider directory missing: {provider_dir}"
        )

    print(f"Provider directory: {provider_dir}")

    print("\nBootstrap environment ready.")
    print("Provider-specific setup will be handled by:")
    print(f"WORKERS/{provider}/")

    print("\nSTATUS: READY")


if __name__ == "__main__":
    main()