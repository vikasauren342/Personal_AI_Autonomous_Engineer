# Personal AI Core Architecture

```text
                     USER / APPLICATION
                            │
                            ▼
                    PersonalAI / App
                            │
                            ▼
                       Orchestrator
                 ┌──────────┼──────────┐
                 ▼          ▼          ▼
              Memory      Router      Planner
                 │          │          │
                 │     ┌────┼────┐     │
                 │     ▼    ▼    ▼     │
                 │  General Research Coding
                 │     Agents / Capabilities
                 │          │
                 └──────────┼──────────┘
                            ▼
                       Tool Registry
                            │
                            ▼
                    Execution Engine
                            │
                            ▼
                     Evaluation Gate
                            │
                            ▼
                     Learning Ledger
                            │
                            └── bounded feedback loop

Model Layer
  ├── Qwen/local Transformers backend (optional, external weights)
  ├── deterministic fallback
  └── future local/API backends

Storage Layer
  ├── persistent memory
  ├── learning ledger
  ├── adapters/datasets/checkpoints
  └── capability-specific state
```

## Separation of concerns

**Core** is the runtime and source of truth.

**Recovery/Reconstruction** is historical evidence/specification used to recover missing development state. It is not silently merged into the core.

**Autonomous Development** is the engineering controller that can inspect, patch, test, verify and checkpoint the core under explicit safety limits. It is not part of the runtime core.

## Expansion interfaces

1. Conversation/context management
2. Semantic long-term memory and retrieval
3. Dynamic capability/module registry
4. Remote worker protocol
5. Kaggle/Colab/local/cloud GPU adapters
6. VS Code client
7. Multimodal perception and generation
8. Multi-agent coordination
9. Formal evaluation/benchmark suite
10. IoT/robotics adapters

The architecture is designed to expand without requiring the foundation layer to be retrained or replaced.
