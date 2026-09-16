# Migration map

The old `kaggle_export/personal_ai_core` tree and the v2 Autonomous Core contained repeated copies of the same config, memory, runtime, and video-reel assets. v3 keeps one canonical implementation in `personal_ai/` and moves legacy artifacts under `legacy_archive/` for reference.

Excluded from the canonical runtime: Python bytecode caches, Hugging Face lock files, duplicated Kaggle export trees, and incomplete local model cache structure. Model/tokenizer assets are stored separately and are optional.
