# Reconstruction Playbook

## If uploaded to another AI
Tell the AI:
"Read 00_START_HERE.md first, then CURRENT_STATE, COMPLETED_STATUS, ARCHITECTURE and ROADMAP. Preserve the foundation. Ask for or inspect the actual project ZIP/source if code execution is required."

## If source ZIP is also available
1. Extract it.
2. Locate project root.
3. Verify `personal_ai/` and storage.
4. Verify critical imports.
5. Run health check.
6. Verify milestone reports.
7. Continue from the highest verified PASS milestone.

## If only this handoff package is available
This package is a reconstruction specification, not the complete source repository. It contains the project's architecture/state/roadmap and enough API facts to avoid common mistakes, but actual source files/model weights may still need to be recovered from durable storage.

## Restoration priorities
1. source code
2. milestone artifacts
3. configuration
4. dependency lock
5. model mapping
6. worker configuration
7. personal/business data boundaries
8. runtime health test

## Never claim source restoration from documentation alone.
