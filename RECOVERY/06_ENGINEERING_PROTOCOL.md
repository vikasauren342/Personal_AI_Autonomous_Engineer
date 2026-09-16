# Engineering Protocol for Any Future AI

## Mandatory workflow
For every milestone:
1. State milestone ID and purpose.
2. Identify exact existing APIs/classes/files to reuse.
3. Make the smallest required change.
4. Provide runnable code.
5. User executes it.
6. Capture real output.
7. Evaluate PASS/FAIL from evidence.
8. If FAIL, diagnose before continuing.
9. Persist artifact/report.
10. Update project state.

## No blind PASS
A milestone is PASS only when its stated checks are actually demonstrated.

## No architecture churn
Do not replace working foundation components merely because a different design seems elegant.

## Correct V3 imports
ExecutionEngine:
`from personal_ai.execution.engine import ExecutionEngine`

Contracts:
`from personal_ai.core.contracts import Task, Plan, Observation, Evaluation`

Bootstrap:
`from personal_ai.bootstrap import Bootstrap`

Runtime:
`runtime = Bootstrap(PROJECT_ROOT).start()`

Execution:
`engine = ExecutionEngine(runtime.tools, runtime.evaluator, runtime.learning, max_steps=5)`

ToolRegistry is directly `runtime.tools`; do not assume `.registry`.

## Important execution semantics
`runtime.tools.python(code)` runs a fresh subprocess, so variables do not persist between calls unless a shared execution mechanism is deliberately used.

`Observation.ok` means an observation was captured. Underlying Python success/failure is reflected by `observation.output["returncode"]`.

## Persistence
Kaggle `/kaggle/working` is temporary. Persistent source should be recovered from the Kaggle Dataset or other durable project storage.

## Qwen3
Current model target:
`Qwen/Qwen3-8B-AWQ`

Structured output should use chat template with thinking disabled when a strict JSON response is required:
`enable_thinking=False`

## Coding style
Prefer robust, explicit code. Avoid indentation-sensitive tricks and fragile assumptions. Use deterministic verification where possible.
