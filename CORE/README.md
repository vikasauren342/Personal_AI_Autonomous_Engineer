# Personal AI — AGI-Ready Core v3.0.1 SUPREME CORE

This is the **clean core package** of the Personal AI project. It intentionally does **not** bundle the autonomous-development runner or the recovery/reconstruction package. Those are separate engineering layers.

## Three-layer project model

```text
YOU / GOAL
   ↓
AUTONOMOUS DEVELOPMENT SYSTEM   (separate package)
   ↓
RECOVERY / RECONSTRUCTION       (separate evidence/spec package)
   ↓
PERSONAL AI CORE                (this package)
```

The core is the canonical runtime/source layer: agents, routing, planning, memory, model abstraction, tools, execution, evaluation, learning ledger, configuration, launchers and tests.

## Design principles

- Preserve the four locked V3 foundation files unchanged.
- Model-agnostic and local-first.
- External model weights; no multi-GB model is hidden inside the source ZIP.
- Lazy model loading with deterministic fallback.
- Bounded autonomous execution and evaluation gates.
- Persistent storage separated from source code.
- Capability modules kept separable from the core.
- Explicit verification and integrity tooling.
- Portable across local Python, Kaggle and Colab with environment-specific model paths.

## Qwen3 runtime

The current preferred external model is `Qwen/Qwen3-8B-AWQ` when the hardware/runtime supports it. The official Qwen model card documents Transformers loading and 4-bit AWQ packaging. The core does not download or bundle those weights.

Supply a complete local model directory with:

```text
config.json
 tokenizer_config.json / tokenizer.json
*.safetensors or another supported weight format
```

and set:

```bash
export PERSONAL_AI_MODEL_DIR=/path/to/model
```

The backend is lazy: architecture tests can run without a model.

## Kaggle rule

Kaggle `/kaggle/input` is treated as read-only. Copy this core into `/kaggle/working` before applying development changes.

## Verification

Run:

```bash
python scripts/verify_core.py
python -m pytest -q
```

## Claim boundary

This package is **AGI-ready by architecture, not AGI itself**. The current verified implementation is a foundation for future conversation, memory, tool, multimodal, remote-worker, agentic and research capabilities.
