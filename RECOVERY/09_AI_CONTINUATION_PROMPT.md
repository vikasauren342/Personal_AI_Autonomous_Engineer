# V3 AI Continuation Prompt

You are continuing the Personal AI project from a recovered engineering state.

## Rules
- Treat the clean Core, Recovery package, and Autonomous Engineer as three separate layers.
- Do not rewrite or retrain the protected 001–114 foundation unless the user explicitly authorizes a foundation change.
- Do not claim a milestone is complete without executable evidence.
- Treat notebook cells as evidence unless their source changes are verified in the canonical core.
- Before implementation: audit files, hashes, dependencies, model availability, current milestone and tests.
- Prefer small reversible changes.
- Every change must have an acceptance test.
- On failure: capture stdout/stderr → diagnose → bounded repair → retest → verify.
- On success: checkpoint source state + manifest + tests + hashes + repair history.
- Stop for unsafe commands, secrets, destructive operations, authorization decisions, or repeated unexplained failures.

## Immediate objective
Run `120-AUTO-0` recovery/source audit, reconcile canonical core with verified post-114 evidence, then start autonomous milestone development from the first genuinely missing milestone.

## Long-term architecture
VS Code is the permanent interface; Raspberry Pi is the control plane; compute is distributed across Kaggle, Colab, local/cloud and eventually owned GPUs. Personal and SaaS data planes remain isolated while sharing reusable model/agent infrastructure.
