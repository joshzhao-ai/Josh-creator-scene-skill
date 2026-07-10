from __future__ import annotations

from collections.abc import Iterable

from .models import ApprovalLedger, CreatorReference, Direction


REQUIRED_LABELS = ("A", "B", "C")


def validate_references(references: list[CreatorReference]) -> None:
    if len(references) != 3:
        raise ValueError("Exactly three creator references are required")
    creators = {item.creator.casefold() for item in references}
    if len(creators) != 3:
        raise ValueError("References must come from three different creators")
    for reference in references:
        reference.validate()
        if reference.match_score < 70:
            raise ValueError(f"{reference.creator}: match_score must be at least 70")


def validate_directions(directions: list[Direction]) -> None:
    labels = tuple(item.label for item in directions)
    if labels != REQUIRED_LABELS:
        raise ValueError(f"Directions must be ordered A/B/C, received {labels}")
    prompts = {item.prompt for item in directions}
    if len(prompts) != 3:
        raise ValueError("The three mockup prompts must be meaningfully distinct")


def assert_rejected_terms_absent(texts: Iterable[str], ledger: ApprovalLedger) -> None:
    haystack = "\n".join(texts).casefold()
    violations = [term for term in ledger.rejected if term.casefold() in haystack]
    if violations:
        raise ValueError(f"Rejected elements returned: {violations}")


def assert_dual_coordinates(text: str) -> None:
    if "画面" not in text or "人物" not in text:
        raise ValueError("Lighting instructions must use both frame-side and subject-side coordinates")
