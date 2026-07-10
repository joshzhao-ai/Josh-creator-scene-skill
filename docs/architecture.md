# Architecture

```text
room photo/video
      ↓
SceneDirector.create() ── approval ledger + fixed geometry
      ↓
ReferenceResearcher ───── exactly 3 verified A-roll cases
      ↓
prepare_directions() ──── A/B/C prompt pack + constraint checks
      ↓
MockupGenerator ───────── 3 separate edits in the real room
      ↓
select(A|B|C)
      ↓
deliver() ─────────────── camera, light, set and correction plan
```

## Why providers are separate

Web research and image generation change quickly. The state machine and quality rules should not. `ReferenceResearcher` and `MockupGenerator` are protocols, so Agent Reach, a browser agent, OpenAI Images, or another service can be swapped without rewriting the workflow.

## Non-negotiable invariants

1. The room image is the geometry source of truth.
2. The user approval ledger outranks a new inspiration image.
3. Exactly three different verified creators seed three different directions.
4. Every light position pairs frame-side and subject-side coordinates.
5. A generated image is a concept preview, followed by a physical execution plan.

