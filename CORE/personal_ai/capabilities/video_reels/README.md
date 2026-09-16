# AI Video & Reel Creator

Persistent Personal AI module for short-form video generation.

## Core pipeline

Prompt
→ Reel Director
→ Story / Script
→ Scene Plan
→ Video / Image Generation
→ Voice
→ Music / SFX
→ Captions
→ FFmpeg
→ 9:16 MP4

## Design principles

- Local-first where practical
- Pluggable generation backends
- Heavy models loaded on demand
- One heavy model at a time
- Generated assets stored persistently
- FFmpeg used for deterministic composition
- Hindi / English / Hinglish supported
- Instagram Reels and YouTube Shorts supported

## Current status

Foundation created.

Generation backends are intentionally not selected yet.
