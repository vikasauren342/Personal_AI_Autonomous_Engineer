# Personal AI Autonomous Development System

## Purpose

This package replaces the repetitive workflow:

`copy code -> paste into Kaggle -> run -> send error -> receive fix -> paste again`

with:

`AUDIT -> PLAN -> GENERATE -> STATIC CHECK -> EXECUTE -> TEST -> VERIFY -> REPAIR -> CHECKPOINT -> NEXT`

The local Qwen model is used as a planning/diagnosis engine when available. Deterministic Python tests and filesystem checks remain the authority for PASS/FAIL.

## What you do

1. Upload this package as a Kaggle Dataset (or unzip it into `/kaggle/working`).
2. Open one Kaggle notebook.
3. Run only `autonomous_runner/launcher.py`.
4. The runner restores the V3 project, audits the current state, discovers the next unfinished milestone, and starts the autonomous loop.
5. If a milestone fails, it attempts bounded diagnosis/repair/retest.
6. State, logs, patches and checkpoints are saved under `autonomous_runner/`.
7. If the runner reaches a manual-stop condition, it writes a `MANUAL_INTERVENTION_REQUIRED.json` report.

## Important reality

Kaggle sessions can terminate, so this is not an infinite-server guarantee. The runner is designed to resume from disk/checkpoints after a new session. It also does NOT magically create an AGI in one click: it automates the engineering loop so the user no longer has to manually shuttle code between ChatGPT and Kaggle.

## Safety model

The runner will not automatically:
- expose credentials or secrets,
- make paid purchases,
- modify external accounts,
- claim PASS without verification,
- rewrite the protected foundation merely because a generated repair failed,
- continue indefinitely after repeated unresolved failures.

## Architecture

- `launcher.py`: one entry point
- `orchestrator.py`: state machine
- `model_agent.py`: local Qwen planning/diagnosis
- `executor.py`: isolated command execution
- `verifier.py`: deterministic checks
- `repair_engine.py`: bounded repair loop
- `checkpoint.py`: resumable state
- `milestone_manager.py`: next-step planning
- `safety.py`: stop gates
- `goal.json`: long-term project goal
- `config.json`: runtime policy
