# Architecture Specification

## Permanent layers

### 1. Interface
VS Code is the permanent primary interface/workspace.

### 2. Control Plane
Raspberry Pi is the permanent control plane/gateway. It stores or coordinates persistent state and routes work.

### 3. Platform Core
Conversation, memory, task lifecycle, planning, tools, execution, observation, verification, recovery, learning, security.

### 4. Agent Layer
Research, coding, firmware, LifeOS, vision, creative, IoT, and future agents.

### 5. Compute Layer
Interchangeable workers:
- Kaggle
- Colab
- local machine
- cloud GPU
- future owned GPU

### 6. Business Layer
SaaS API, authentication, tenant isolation, subscriptions, quotas, usage, billing integration, IoT.

## Distributed GPU principle
Use job-level distribution first:

Task -> Pi -> scheduler -> one capable worker -> result -> Pi

Do not initially depend on network model-parallelism.

## Worker contract
A worker should expose at least:
- worker_id
- status
- GPU/CPU resources
- VRAM
- model availability
- capabilities
- load
- endpoint/transport
- heartbeat
- authorization state
- version
- health

## Scheduling policy
Prefer:
1. authorized worker
2. capable worker
3. least risky/appropriate execution path
4. sufficient VRAM/resources
5. acceptable latency/cost
6. healthy worker
7. priority/tenant policy

## Failure behavior
Worker failure must be observable. The scheduler should mark the worker unhealthy and requeue/failover according to policy without corrupting persistent task state.

## Model abstraction
Qwen3-8B-AWQ is the current model target, but model identity must remain replaceable. Future models may include larger text models and VLMs.

## Data boundary
Personal and SaaS data are logically separate namespaces/tenants, even if they temporarily share the Raspberry Pi.
