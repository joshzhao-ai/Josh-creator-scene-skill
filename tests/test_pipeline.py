from pathlib import Path

import pytest

from creator_scene_director import ApprovalLedger, CreatorReference, SceneDirector, Stage


def references() -> list[CreatorReference]:
    return [
        CreatorReference(
            creator=f"Creator {index}",
            platform="YouTube",
            source_url=f"https://example.com/video-{index}",
            frame_url=f"https://example.com/frame-{index}.jpg",
            lane="technology",
            match_score=80 + index,
            why_match=["small-room depth"],
            borrow=["soft key", "warm practical"],
            do_not_borrow=["large monitor wall"],
            lighting_read="soft side key and restrained practical",
            verified_aroll=True,
        )
        for index in range(1, 4)
    ]


def test_full_state_flow(tmp_path: Path) -> None:
    source = tmp_path / "room.jpg"
    source.write_bytes(b"not-decoded-by-core")
    director = SceneDirector.create(
        source,
        tmp_path / "project",
        creator_lane="AI / tech",
        scene_notes=["straight desk", "real depth behind the chair"],
        ledger=ApprovalLedger(
            approved=["warm practical"],
            rejected=["active display"],
            fixed=["desk direction", "camera angle"],
        ),
    )
    assert director.project.stage is Stage.INTAKE
    director.set_references(references())
    assert director.project.stage is Stage.REFERENCES
    directions = director.prepare_directions()
    assert [item.label for item in directions] == ["A", "B", "C"]
    assert all("画面右（人物左）" in " ".join(item.lighting) for item in directions)
    for label in ("A", "B", "C"):
        mockup = tmp_path / f"{label}.png"
        mockup.write_bytes(label.encode())
        director.attach_mockup(label, mockup)
    director.select("A")
    plan = director.deliver()
    assert plan.exists()
    assert "画面右（人物左）" in plan.read_text(encoding="utf-8")
    assert director.project.stage is Stage.DELIVERED


def test_requires_three_unique_verified_references(tmp_path: Path) -> None:
    source = tmp_path / "room.jpg"
    source.write_bytes(b"x")
    director = SceneDirector.create(source, tmp_path / "project", creator_lane="tech")
    with pytest.raises(ValueError, match="Exactly three"):
        director.set_references(references()[:2])


def test_cannot_select_before_all_three_mockups(tmp_path: Path) -> None:
    source = tmp_path / "room.jpg"
    source.write_bytes(b"x")
    director = SceneDirector.create(source, tmp_path / "project", creator_lane="tech")
    director.set_references(references())
    director.prepare_directions()
    with pytest.raises(ValueError, match="all three"):
        director.select("A")


def test_new_feedback_invalidates_stale_directions(tmp_path: Path) -> None:
    source = tmp_path / "room.jpg"
    source.write_bytes(b"x")
    director = SceneDirector.create(source, tmp_path / "project", creator_lane="tech")
    director.set_references(references())
    director.prepare_directions()
    director.update_ledger(rejected=["invented screen"])
    assert director.project.stage is Stage.REFERENCES
    assert director.project.directions == []
