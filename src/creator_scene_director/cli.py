from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import ApprovalLedger, CreatorReference
from .openai_images import OpenAIImageGenerator
from .pipeline import SceneDirector


def _load_references(path: str | Path) -> list[CreatorReference]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [CreatorReference(**item) for item in data]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="creator-scene-director")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a scene project from one real room image")
    init.add_argument("image")
    init.add_argument("--out", required=True)
    init.add_argument("--lane", default="AI / tech talking head")
    init.add_argument("--note", action="append", default=[])
    init.add_argument("--approve", action="append", default=[])
    init.add_argument("--reject", action="append", default=[])

    refs = sub.add_parser("references", help="Attach exactly three verified A-roll references")
    refs.add_argument("project")
    refs.add_argument("references_json")

    ledger = sub.add_parser("ledger", help="Record new approvals/rejections and invalidate stale mockups")
    ledger.add_argument("project")
    ledger.add_argument("--approve", action="append", default=[])
    ledger.add_argument("--reject", action="append", default=[])
    ledger.add_argument("--fix", action="append", default=[])
    ledger.add_argument("--vary", action="append", default=[])

    prepare = sub.add_parser("prepare", help="Create A/B/C direction prompts")
    prepare.add_argument("project")

    mockups = sub.add_parser("mockups", help="Generate all three room-specific mockups")
    mockups.add_argument("project")
    mockups.add_argument("--provider", choices=("openai",), default="openai")
    mockups.add_argument("--model", default="gpt-image-2")
    mockups.add_argument("--quality", choices=("low", "medium", "high", "auto"), default="medium")
    mockups.add_argument("--size", default="auto")

    attach = sub.add_parser("attach", help="Attach an externally generated mockup")
    attach.add_argument("project")
    attach.add_argument("label", choices=("A", "B", "C"))
    attach.add_argument("image")

    select = sub.add_parser("select", help="Select A, B or C")
    select.add_argument("project")
    select.add_argument("label", choices=("A", "B", "C"))

    deliver = sub.add_parser("deliver", help="Write the executable lighting and set plan")
    deliver.add_argument("project")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init":
        ledger = ApprovalLedger(approved=args.approve, rejected=args.reject)
        director = SceneDirector.create(
            args.image,
            args.out,
            creator_lane=args.lane,
            scene_notes=args.note,
            ledger=ledger,
        )
        print(director.project.state_path)
        return 0

    director = SceneDirector.load(args.project)
    if args.command == "references":
        director.set_references(_load_references(args.references_json))
        print(director.project.state_path)
    elif args.command == "ledger":
        updated = director.update_ledger(
            approved=args.approve,
            rejected=args.reject,
            fixed=args.fix,
            variable=args.vary,
        )
        print(json.dumps({"approved": updated.approved, "rejected": updated.rejected}, ensure_ascii=False))
    elif args.command == "prepare":
        director.prepare_directions()
        print(Path(director.project.output_dir) / "prompts")
    elif args.command == "mockups":
        generator = OpenAIImageGenerator(model=args.model, quality=args.quality, size=args.size)
        for path in director.generate_mockups(generator):
            print(path)
    elif args.command == "attach":
        print(director.attach_mockup(args.label, args.image))
    elif args.command == "select":
        director.select(args.label)
        print(f"selected {args.label}")
    elif args.command == "deliver":
        print(director.deliver())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
