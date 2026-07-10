from __future__ import annotations

from .models import ApprovalLedger, CreatorReference, Direction


TERRITORIES = (
    {
        "label": "A",
        "name": "Warm creator studio",
        "objective": "Warm practical depth with a calm, credible AI-creator identity.",
        "composition": [
            "Preserve the original camera angle, crop, desk direction, chair and real depth path.",
            "Keep the creator dominant; use one readable background anchor on the real wall plane.",
        ],
        "set_moves": [
            "Use one plausible flush shelf or existing support plane, one plant and restrained books/tools.",
            "Keep the midground screen-free and physically supported by the existing wall plane.",
        ],
        "lighting": [
            "Soft neutral key from 画面右（人物左）前方 35–45°, slightly above eye line.",
            "One 2700–3000K practical behind the subject; background stays below face exposure.",
        ],
    },
    {
        "label": "B",
        "name": "Minimal product designer",
        "objective": "Cleaner negative space and fewer objects without losing the real midground.",
        "composition": [
            "Lock the source geometry and retain the curtain-to-wall depth transition.",
            "Leave deliberate negative space for captions and product callouts.",
        ],
        "set_moves": [
            "Keep one art/plant anchor and one creator tool; remove low-value surface clutter.",
            "Do not add a screen or furniture that is unsupported by the source room.",
        ],
        "lighting": [
            "Large soft key from 画面右（人物左）前方, with subtle negative fill on the opposite side.",
            "Use a low-output warm practical or wall bounce for depth, not as the face key.",
        ],
    },
    {
        "label": "C",
        "name": "Dark professional tech",
        "objective": "Deeper controlled contrast and black-shirt separation without gaming RGB.",
        "composition": [
            "Keep the original architecture and camera relationship; darken, do not rebuild, the room.",
            "Preserve a readable shoulder edge and one warm destination in the background.",
        ],
        "set_moves": [
            "Use dark neutral textiles and one warm practical; keep tools sparse and purposeful.",
            "No neon strips, fake monitors, logos, floating shelves or invented construction.",
        ],
        "lighting": [
            "Controlled soft key from 画面右（人物左）前方 with stronger negative fill.",
            "Add a restrained rim only if required to separate hair and a black shirt.",
        ],
    },
)


def build_prompt(
    territory: dict[str, object],
    reference: CreatorReference,
    ledger: ApprovalLedger,
    scene_notes: list[str],
) -> str:
    approved = "; ".join(ledger.approved) or "none specified"
    rejected = "; ".join(ledger.rejected) or "none specified"
    fixed = "; ".join(ledger.fixed) or "source identity and architecture"
    variable = "; ".join(ledger.variable) or "background density and contrast"
    notes = "; ".join(scene_notes) or "read directly from the source image"
    composition = " ".join(territory["composition"])  # type: ignore[arg-type]
    set_moves = " ".join(territory["set_moves"])  # type: ignore[arg-type]
    lighting = " ".join(territory["lighting"])  # type: ignore[arg-type]
    return f"""Use case: identity-preserving realistic A-roll room edit.
Edit target: the first supplied image is the user's actual room and geometry source of truth.
Reference grammar: {reference.creator} ({reference.source_url}), used only for transferable lighting and composition ideas: {', '.join(reference.borrow)}.
Direction: {territory['label']} — {territory['name']}. {territory['objective']}
Room read: {notes}
Composition: {composition}
Set: {set_moves}
Lighting: {lighting}
Approval ledger — Approved: {approved}. Rejected: {rejected}. Fixed: {fixed}. Variable: {variable}.
Hard locks: preserve identity, skin texture, hair, pose, body, chair, desk orientation, camera position, crop, aspect ratio, curtain/window/wall/opening positions and the real background depth path.
Avoid: face beautification, fictional architecture, changed desk angle, active monitor unless explicitly approved, foreground table protrusion, unsupported furniture, impossible shelf, fake text, logo, watermark, heavy RGB, clutter.
Output: one photorealistic concept preview that a person could physically reproduce in this exact room."""


def build_directions(
    references: list[CreatorReference],
    ledger: ApprovalLedger,
    scene_notes: list[str],
) -> list[Direction]:
    directions: list[Direction] = []
    for territory, reference in zip(TERRITORIES, references, strict=True):
        directions.append(
            Direction(
                label=str(territory["label"]),
                name=str(territory["name"]),
                objective=str(territory["objective"]),
                composition=list(territory["composition"]),  # type: ignore[arg-type]
                set_moves=list(territory["set_moves"]),  # type: ignore[arg-type]
                lighting=list(territory["lighting"]),  # type: ignore[arg-type]
                prompt=build_prompt(territory, reference, ledger, scene_notes),
                reference_creator=reference.creator,
            )
        )
    return directions
