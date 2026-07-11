# Mockup prompting

## Inputs and invariants

Use the user's room photo as the **edit target**. Use creator images only as **style/composition references**. If the user approved an earlier render, use it as an **approved visual reference** and give it higher priority for set dressing and overall feel. Preserve:

- identity, skin texture, hair, body, pose, chair, camera view, and aspect ratio;
- fixed room geometry, desk direction, curtain/window/door/wall positions, and real background depth;
- existing objects unless the plan explicitly removes, hides, or replaces them.

Before prompting, write an approval ledger:

- `Approved`: elements explicitly liked or requested; keep them unless a version intentionally varies one as an `Unknown`.
- `Rejected`: elements explicitly disliked; exclude them from every version.
- `Fixed`: identity, camera, desk, curtain, wall, openings, and real depth path.
- `Variable`: one or two controlled choices that distinguish A/B/C.

## Prompt skeleton

```text
Use case: identity-preserve
Asset type: realistic creator A-roll visual mockup
Edit target: the user's current room photo
Style reference: creator A-roll, used only for lighting mood and visual grammar
Approved visual reference: prior user-liked render, used for approved set dressing and overall feel (optional)
Primary request: [main room-specific plan]
Composition: preserve camera angle, crop, desk orientation, and the actual background depth path.
Lighting: [key in dual coordinate language], [color temperature], [background practical], [rim/negative fill].
Set: [only validated additions, placed against real planes].
Identity and geometry locks: preserve the creator's identity and all fixed room architecture exactly.
Approval ledger: Approved [items]; Rejected [items]; Fixed [items]; Variable [items].
Avoid: rejected elements, active monitor/screen unless approved, fictional architecture, foreground table protrusion, impossible shelves, heavy RGB/neon, clutter, fake text, logos, watermark, face beautification.
```

## Three-version system

Issue three separate prompts and keep identity/geometry locks identical:

- **A — Warm creator studio:** emphasize warm practical, organic plant shape, books/creator proof, and a flush midground unit when physically plausible.
- **B — Minimal product designer:** reduce object count, preserve one anchor plus one practical, and retain enough midground to avoid an empty-wall result.
- **C — Dark professional tech:** deepen background contrast, keep the face dominant, and use restrained warm/cool separation without gaming RGB.

Each version must change at least two of: object density, background anchor, practical-light placement, contrast ratio, or creator-tool presence. Do not create three near-duplicates.

## Validate before presenting

Compare each output to the original and any approved render. Confirm:

1. desk and camera orientation are unchanged;
2. the depth path is real, not a fabricated room extension;
3. each added object has a plausible support and scale;
4. the face is the brightest attention point;
5. a user can tell which parts are lights, movable set dressing, and existing architecture.
6. approved elements remain unless deliberately varied, and rejected elements do not return.
7. the version has a readable midground and is meaningfully distinct from the other two.

If one invariant breaks, issue one focused correction rather than changing the whole concept.
