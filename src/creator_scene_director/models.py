from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class Stage(str, Enum):
    INTAKE = "intake"
    REFERENCES = "references"
    DIRECTIONS = "directions"
    MOCKUPS = "mockups"
    SELECTED = "selected"
    DELIVERED = "delivered"


@dataclass(slots=True)
class ApprovalLedger:
    """User decisions that must survive every later generation step."""

    approved: list[str] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)
    fixed: list[str] = field(default_factory=list)
    variable: list[str] = field(default_factory=list)

    def validate(self) -> None:
        approved = {item.casefold() for item in self.approved}
        rejected = {item.casefold() for item in self.rejected}
        overlap = approved & rejected
        if overlap:
            raise ValueError(f"Approval ledger conflict: {sorted(overlap)}")


@dataclass(slots=True)
class CreatorReference:
    creator: str
    platform: str
    source_url: str
    frame_url: str
    lane: str
    match_score: int
    why_match: list[str]
    borrow: list[str]
    do_not_borrow: list[str]
    lighting_read: str
    verified_aroll: bool = False

    def validate(self) -> None:
        if not self.verified_aroll:
            raise ValueError(f"{self.creator}: reference is not verified A-roll")
        if not self.source_url.startswith(("https://", "http://")):
            raise ValueError(f"{self.creator}: source_url must be an HTTP URL")
        if not self.frame_url.startswith(("https://", "http://", "file://")):
            raise ValueError(f"{self.creator}: frame_url must be an HTTP or file URL")
        if not 0 <= self.match_score <= 100:
            raise ValueError(f"{self.creator}: match_score must be between 0 and 100")


@dataclass(slots=True)
class Direction:
    label: str
    name: str
    objective: str
    composition: list[str]
    set_moves: list[str]
    lighting: list[str]
    prompt: str
    reference_creator: str
    mockup_path: str | None = None


@dataclass(slots=True)
class Project:
    source_image: str
    creator_lane: str
    output_dir: str
    scene_notes: list[str]
    ledger: ApprovalLedger
    coordinate_system: str = (
        "画面左/右 = viewer; 人物左/右 = creator; 相机左/右 = behind camera"
    )
    stage: Stage = Stage.INTAKE
    references: list[CreatorReference] = field(default_factory=list)
    directions: list[Direction] = field(default_factory=list)
    selected_label: str | None = None
    deliverable_path: str | None = None

    @property
    def state_path(self) -> Path:
        return Path(self.output_dir) / "scene-project.json"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["stage"] = self.stage.value
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Project":
        ledger = ApprovalLedger(**data["ledger"])
        references = [CreatorReference(**item) for item in data.get("references", [])]
        directions = [Direction(**item) for item in data.get("directions", [])]
        return cls(
            source_image=data["source_image"],
            creator_lane=data["creator_lane"],
            output_dir=data["output_dir"],
            scene_notes=list(data.get("scene_notes", [])),
            ledger=ledger,
            coordinate_system=data.get(
                "coordinate_system",
                "画面左/右 = viewer; 人物左/右 = creator; 相机左/右 = behind camera",
            ),
            stage=Stage(data.get("stage", Stage.INTAKE.value)),
            references=references,
            directions=directions,
            selected_label=data.get("selected_label"),
            deliverable_path=data.get("deliverable_path"),
        )

