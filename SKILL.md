---
name: josh-creator-scene-skill
description: >-
  Use when a creator says their talking-head background looks bad, asks how to light or stage a real bedroom/home office, wants three achievable A-roll scene previews from one room photo, or needs exact camera, lighting, set and shopping instructions for YouTube, Bilibili, Xiaohongshu, courses, livestreams, AI/tech content or a personal brand. The skill researches verified creator references, edits the user's actual room into three distinct options, preserves real geometry and user corrections, then turns the selected option into a setup they can reproduce.
---

# Josh Creator Scene Skill

Build three scenes that are credible in the user's actual room, not generic pretty renders. The product promise is: **upload one real room image, see three achievable ideal A-roll outcomes, choose one, then receive exact setup instructions.** The user should not need to understand prompts, CLI, SDKs, lighting theory or set-design terminology.

## Core rules

- Treat the user's photo/video as the source of truth for room geometry, fixed openings, desk orientation, and usable depth. State assumptions instead of inventing architecture.
- Never say only "left" or "right". Use `画面右（人物左）`, `画面左（人物右）`, or `相机右` as appropriate. Define the coordinate system once in every practical plan.
- Use only genuine A-roll examples: the creator is visibly speaking to camera in the featured setup. Do not substitute B-roll, course slides, product photos, studio tours, stock interiors, or unrelated screenshots.
- Present generated visual effects as a concept preview, not as proof that the proposed objects fit or that lighting values are exact.
- Keep the creator visually dominant. Background is for depth, identity, and proof of work—not clutter.
- Preserve a supplied person’s identity, pose, room planes, camera angle, and architectural constraints when generating a mockup. Do not beautify the face or alter body, room dimensions, windows, doors, or desk direction.
- Maintain an **approval ledger** throughout the conversation. Record elements the user explicitly liked, rejected, or corrected. Approved elements outrank a newly selected inspiration image; rejected elements must not reappear.
- Distinguish `existing architecture`, `plausible movable additions`, and `imagined construction`. The user may approve a flush shelf, plant, practical lamp, art, or microphone even when these are not in the source photo. Do not interpret "preserve the room" as "leave the room empty."

## 0. Intake and spatial read

Accept one scene photo as the minimum viable input. If available, also collect a sweep video, intended platform and aspect ratio, content lane, budget, existing gear, rental/installation constraints, and anything that must stay.

Do not block on missing details. Make a best-effort spatial read, mark uncertain assumptions, and request only the one extra input that materially changes the solution—for example, a 10-second room sweep when depth behind the chair cannot be seen.

Before researching, summarize:

1. camera position and likely framing;
2. subject position, eyeline, desk edge, and any real depth path;
3. foreground/midground/background planes, fixed visual noise, practical power locations, and daylight control;
4. the scene's suitable brand direction in one sentence.

Create the approval ledger from the whole task context:

- **Keep/approved:** room geometry and any prior visual elements the user explicitly endorsed.
- **Avoid/rejected:** screens, furniture, layouts, colors, or lighting treatments the user disliked.
- **Unknown:** choices that may vary across the three versions.

Read [spatial-reading.md](references/spatial-reading.md) for the checklist and coordinate convention.

## 1. Find three reference creators

Use `agent-reach` for online discovery and follow `web-access` requirements for any live web or browser operation. Announce the research capability before using it. Before research, run `agent-reach doctor --json`; if the command is not on `PATH`, also try `$HOME/.agent-reach-venv/bin/agent-reach doctor --json`. Prefer direct creator/video/profile sources over reposts.

If Agent Reach is genuinely unavailable, use the environment's official web/search/browser capability as a declared fallback. Never fabricate creator names, URLs, or A-roll frames. If no live network path exists, finish only the spatial read and explain the missing dependency instead of pretending Stage 1 is complete.

Read [reference-research.md](references/reference-research.md). Find exactly three candidates before making the room-specific designs. Every candidate must include:

- creator name, primary platform/profile or source-video URL, lane, and a captured/linked A-roll frame;
- the exact visual elements that match the user's room;
- a match score with reasons, plus what must *not* be copied;
- a one-line lighting read: key direction/softness, background practical, separation, and contrast.

Choose three different creators. Optimize for physical applicability rather than follower count or aesthetic novelty. If no source has a reliable public A-roll frame, say so and replace it with a better-evidenced candidate.

Use the references as design evidence. Unless the user explicitly asks to stop at raw references, do **not** make them choose yet; users cannot reliably judge a reference until they see it translated into their own room.

## 2. Convert references into three room-specific directions

Read [set-design.md](references/set-design.md). Create three distinct but equally credible directions. Each may map to one reference or combine a reference's lighting grammar with approved elements from a prior user-liked render. Translate each direction through these layers:

1. **Composition:** final crop, camera height, subject offset, visible depth path, and negative space.
2. **Set:** retain/use/remove/add; use only objects that fit real planes and do not create a fake floating desk or display.
3. **Lighting:** key, negative fill, practical/background light, optional rim; specify direction in both coordinate systems.
4. **Brand:** color/material hierarchy for the creator lane. For an AI/tech creator, favor controlled contrast, restrained warm practicals, dark neutral clothing options, purposeful tools, and a quiet proof-of-work background.
5. **Approval ledger:** retain approved elements and exclude rejected ones in all three directions.

The three versions must differ in a meaningful visual decision, not merely color temperature. Recommended territories:

- **A — Warm creator studio:** strongest lifestyle depth and practical-light warmth.
- **B — Minimal product designer:** fewer objects and cleaner negative space, while retaining a real midground.
- **C — Dark professional tech:** deeper contrast and stronger separation, without RGB/gaming cues.

Do not label one as the cheap or inferior version. All three should be desirable and physically achievable.

## 3. Show the visual effect

Use the `imagegen` skill and its built-in image tool to edit the supplied scene image. Read [mockup-prompting.md](references/mockup-prompting.md) before prompting.

Generate **three visual mockups** using separate image-generation calls. Preserve the source room’s actual geometry and the person's identity in every version. Use references for mood and visual grammar, not literal copying. If the user supplies a previously approved render, include it as an `approved visual reference` with higher priority than the creator inspiration.

Inspect all three results against the source and approval ledger. Regenerate a version once if it changes room structure/camera orientation, loses the approved midground, reintroduces a rejected element, or is not meaningfully different from the other versions. Present A/B/C together with a short legend distinguishing existing items, movable additions, and lighting-only changes.

Only after the user sees their own room in all three versions, ask them to choose `A`, `B`, or `C`.

## 4. Deliver the executable setup

Read [execution-deliverable.md](references/execution-deliverable.md). Give an implementation-ready plan containing:

- top-down placement with camera, subject, desk, all light positions, and the real background/depth path;
- camera recipe: lens/field of view, height, distance, crop, eyeline, and exposure/WB starting point;
- lighting recipe: modifier, relative position, height, angle, distance, color temperature, starting output, what it illuminates, and the adjustment test;
- staging list: exact objects, positions, scale, color/material role, plus items to remove/hide;
- budget tiers and a purchase list limited to missing necessities;
- a 10-minute setup sequence and a phone-preview correction loop.

Use relative brightness first (`face`, `background`, `practical`) rather than false precision. Add absolute power/lux only when the fixture or meter is known. Explain every visual move in terms of the user's content identity and the chosen reference.

## Finish condition

The task is complete only when the user has: three verified references, three room-specific visual mockups, one selected direction, and specific instructions they can set up alone. Offer a final calibration pass from one test frame after they build it.
