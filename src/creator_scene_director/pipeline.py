from __future__ import annotations

import json
from pathlib import Path

from .constraints import (
    assert_dual_coordinates,
    assert_rejected_terms_absent,
    validate_directions,
    validate_references,
)
from .models import ApprovalLedger, CreatorReference, Project, Stage
from .prompting import build_directions
from .providers import MockupGenerator, ReferenceResearcher


class SceneDirector:
    """Stateful workflow kernel for room-specific creator scene design."""

    def __init__(self, project: Project) -> None:
        self.project = project

    @classmethod
    def create(
        cls,
        source_image: str | Path,
        output_dir: str | Path,
        *,
        creator_lane: str,
        scene_notes: list[str] | None = None,
        ledger: ApprovalLedger | None = None,
    ) -> "SceneDirector":
        source = Path(source_image).expanduser().resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        out = Path(output_dir).expanduser().resolve()
        out.mkdir(parents=True, exist_ok=True)
        ledger = ledger or ApprovalLedger()
        mandatory_locks = [
            "creator identity and pose",
            "camera angle and crop",
            "desk direction",
            "curtain, wall and opening positions",
            "real background depth path",
        ]
        ledger.fixed = list(dict.fromkeys([*ledger.fixed, *mandatory_locks]))
        ledger.validate()
        director = cls(
            Project(
                source_image=str(source),
                creator_lane=creator_lane,
                output_dir=str(out),
                scene_notes=scene_notes or [],
                ledger=ledger,
            )
        )
        director.save()
        return director

    @classmethod
    def load(cls, state_path: str | Path) -> "SceneDirector":
        path = Path(state_path).expanduser().resolve()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(Project.from_dict(data))

    def save(self) -> Path:
        self.project.ledger.validate()
        self.project.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.project.state_path.write_text(
            json.dumps(self.project.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return self.project.state_path

    def research(self, researcher: ReferenceResearcher) -> list[CreatorReference]:
        return self.set_references(researcher.research(self.project))

    def update_ledger(
        self,
        *,
        approved: list[str] | None = None,
        rejected: list[str] | None = None,
        fixed: list[str] | None = None,
        variable: list[str] | None = None,
    ) -> ApprovalLedger:
        """Persist user feedback and invalidate downstream work that used older decisions."""

        ledger = self.project.ledger
        ledger.approved = list(dict.fromkeys([*ledger.approved, *(approved or [])]))
        ledger.rejected = list(dict.fromkeys([*ledger.rejected, *(rejected or [])]))
        ledger.fixed = list(dict.fromkeys([*ledger.fixed, *(fixed or [])]))
        ledger.variable = list(dict.fromkeys([*ledger.variable, *(variable or [])]))
        ledger.validate()
        if self.project.references:
            self.project.stage = Stage.REFERENCES
        else:
            self.project.stage = Stage.INTAKE
        self.project.directions = []
        self.project.selected_label = None
        self.project.deliverable_path = None
        self.save()
        return ledger

    def set_references(self, references: list[CreatorReference]) -> list[CreatorReference]:
        validate_references(references)
        self.project.references = references
        self.project.stage = Stage.REFERENCES
        self.save()
        return references

    def prepare_directions(self) -> list:
        validate_references(self.project.references)
        directions = build_directions(
            self.project.references,
            self.project.ledger,
            self.project.scene_notes,
        )
        validate_directions(directions)
        assert_rejected_terms_absent(
            ("\n".join(item.set_moves) for item in directions), self.project.ledger
        )
        for direction in directions:
            assert_dual_coordinates("\n".join(direction.lighting))
        self.project.directions = directions
        self.project.stage = Stage.DIRECTIONS
        prompt_dir = Path(self.project.output_dir) / "prompts"
        prompt_dir.mkdir(parents=True, exist_ok=True)
        for direction in directions:
            (prompt_dir / f"{direction.label}-{direction.name.lower().replace(' ', '-')}.txt").write_text(
                direction.prompt + "\n", encoding="utf-8"
            )
        self.save()
        return directions

    def generate_mockups(self, generator: MockupGenerator) -> list[Path]:
        if not self.project.directions:
            self.prepare_directions()
        output_paths: list[Path] = []
        mockup_dir = Path(self.project.output_dir) / "mockups"
        for direction in self.project.directions:
            target = mockup_dir / f"{direction.label}-{direction.name.lower().replace(' ', '-')}.png"
            result = generator.generate(self.project, direction, target)
            direction.mockup_path = str(result.resolve())
            output_paths.append(result)
            self.save()
        self.project.stage = Stage.MOCKUPS
        self.save()
        return output_paths

    def attach_mockup(self, label: str, image_path: str | Path) -> Path:
        direction = self._direction(label)
        path = Path(image_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        direction.mockup_path = str(path)
        if all(item.mockup_path for item in self.project.directions):
            self.project.stage = Stage.MOCKUPS
        self.save()
        return path

    def select(self, label: str) -> None:
        self._direction(label)
        if len(self.project.directions) != 3 or not all(
            direction.mockup_path for direction in self.project.directions
        ):
            raise ValueError("Review all three A/B/C mockups before selecting a direction")
        self.project.selected_label = label.upper()
        self.project.stage = Stage.SELECTED
        self.save()

    def deliver(self) -> Path:
        if not self.project.selected_label:
            raise ValueError("Select A, B or C before creating the execution plan")
        selected = self._direction(self.project.selected_label)
        plan_path = Path(self.project.output_dir) / "execution-plan.md"
        plan_path.write_text(self._render_plan(selected), encoding="utf-8")
        self.project.deliverable_path = str(plan_path.resolve())
        self.project.stage = Stage.DELIVERED
        self.save()
        return plan_path

    def _direction(self, label: str):
        normalized = label.upper()
        for direction in self.project.directions:
            if direction.label == normalized:
                return direction
        raise ValueError(f"Unknown direction {label!r}; expected A, B or C")

    def _render_plan(self, selected) -> str:
        lighting_rows = "\n".join(
            f"| {index + 1} | {instruction} | Start low; raise until face leads |"
            for index, instruction in enumerate(selected.lighting)
        )
        set_items = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(selected.set_moves))
        return f"""# {selected.label} — {selected.name}

> {selected.objective}

## Coordinate system

{self.project.coordinate_system}

## What stays fixed

{chr(10).join(f'- {item}' for item in self.project.ledger.fixed)}

## Camera

- Preserve the approved camera position, desk direction and real background depth path.
- Start at eye level with a chest-up crop; tune focal length before moving furniture.
- Lock white balance after the key light is placed.

## Lighting

| Order | Placement | Starting test |
| --- | --- | --- |
{lighting_rows}

## Set map

{set_items}

## 10-minute setup

1. Clear rejected objects and lock camera/crop.
2. Turn off decorative lights; expose only for the face key.
3. Place the key from 画面右（人物左） and shape the shadow side.
4. Add the background practical below face brightness.
5. Add set objects one by one; stop when the eye returns to the face.
6. Record a 10-second test clip and correct face, background, then crop—in that order.

## Correction loop

- Flat face: move the key farther toward 画面右（人物左）, not simply brighter.
- Dark shirt disappears: add a subtle rim or brighten the background edge behind the shoulder.
- Practical clips: lower it until texture returns; do not lower the face key first.
- Background competes: remove one object before buying another light.
"""
