# Research & Release Notes — 2026-09-14

## Evidence used

1. The project's reconstruction/development record was used to preserve the distinction between the canonical V3 source, historical recovery evidence, and the autonomous development runner.
2. The latest 219-cell Kaggle notebook was treated as an evidence/development overlay, not as proof that every experiment had been merged into the canonical source.
3. The official Qwen3-8B-AWQ model card was checked for current Transformers usage and 4-bit AWQ packaging.
4. Kaggle's current dataset documentation was checked for ZIP handling and the read-only `/kaggle/input` / writable working-directory workflow.

## Engineering decisions

- Keep model weights outside the core ZIP.
- Do not merge the autonomous runner into the runtime core.
- Do not claim AGI completion.
- Keep the four protected V3 foundation files byte-identical.
- Harden model discovery so tokenizer/config-only assets are not mistaken for a runnable model.
- Prefer explicit `PERSONAL_AI_MODEL_DIR` for reproducible model selection.
- Keep fallback operation available for architecture tests without GPU/model weights.

## Known boundaries

The current core does not itself provide a production-grade semantic memory system, unrestricted autonomous software engineering, a full multimodal stack, distributed worker orchestration, or AGI. Those are future milestones and/or separate engineering layers.
