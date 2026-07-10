# Creator Scene Director SDK

**Upload one real room photo → see three achievable A-roll setups → choose one → receive an exact lighting and set plan.**

Most “AI room redesign” tools make a prettier room. This SDK is narrower: it protects the creator’s real camera geometry, remembers user corrections, and turns visual references into three filmable talking-head setups.

## Real result

| Input room | A — Warm creator studio |
| --- | --- |
| ![Original room](examples/josh-ai-tech/input-room.jpg) | ![Selected warm creator studio](examples/josh-ai-tech/A-warm-creator-studio.png) |

| B — Minimal product designer | C — Dark professional tech |
| --- | --- |
| ![Minimal product designer](examples/josh-ai-tech/B-minimal-product-designer.png) | ![Dark professional tech](examples/josh-ai-tech/C-dark-professional-tech.png) |

The images are concept previews generated from the same real room. The SDK then creates the physical setup instructions.

## What it locks

- identity, pose, camera angle, crop and desk direction;
- curtain, wall, window/door planes and the real background depth path;
- explicit user approvals and rejections across every generation;
- dual coordinates such as `画面右（人物左）`, so lighting plans do not flip left/right;
- exactly three verified, different A-roll creator references—not B-roll or generic interiors.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[openai]'
```

Set `OPENAI_API_KEY` only when using the included GPT Image adapter. The core package has zero runtime dependencies.

The bundled adapter uses OpenAI's current [`gpt-image-2`](https://developers.openai.com/api/docs/models/gpt-image-2) image-edit endpoint with high input fidelity by default.

## CLI workflow

```bash
# 1. Intake: one real room image is enough
creator-scene-director init room.jpg \
  --out scene-project \
  --lane "AI / tech talking head" \
  --note "The desk is straight; only the person turns" \
  --note "There is real depth behind the chair" \
  --approve "warm practical and restrained creator tools" \
  --reject "active display and invented side table"

# 2. Attach three reviewed, verified A-roll references
creator-scene-director references \
  scene-project/scene-project.json references.json

# Record later feedback at any time; stale prompts/mockups are invalidated
creator-scene-director ledger scene-project/scene-project.json \
  --approve "warm practical" \
  --reject "active display"

# 3. Build three room-specific prompt directions
creator-scene-director prepare scene-project/scene-project.json

# 4. Generate all three edits with GPT Image 2
creator-scene-director mockups scene-project/scene-project.json

# 5. Choose only after seeing A/B/C
creator-scene-director select scene-project/scene-project.json A

# 6. Deliver the physical setup plan
creator-scene-director deliver scene-project/scene-project.json
```

## Python SDK

```python
from creator_scene_director import ApprovalLedger, SceneDirector
from creator_scene_director.openai_images import OpenAIImageGenerator

director = SceneDirector.create(
    "room.jpg",
    "scene-project",
    creator_lane="AI / tech talking head",
    scene_notes=[
        "The desk is straight; only the person turns.",
        "Preserve the real depth path behind the chair.",
    ],
    ledger=ApprovalLedger(
        approved=["warm practical", "dark neutral clothing"],
        rejected=["active display", "invented side table", "gaming RGB"],
        fixed=["identity", "camera angle", "desk direction", "room geometry"],
    ),
)

# Use a ReferenceResearcher adapter, or attach three manually reviewed references.
director.set_references(my_three_verified_references)
director.prepare_directions()
director.generate_mockups(OpenAIImageGenerator(model="gpt-image-2", input_fidelity="high"))
director.select("A")
print(director.deliver())
```

## Provider interfaces

```python
class ReferenceResearcher(Protocol):
    def research(self, project: Project) -> list[CreatorReference]: ...

class MockupGenerator(Protocol):
    def generate(self, project: Project, direction: Direction, output_path: Path) -> Path: ...
```

Use Agent Reach, browser automation, or a custom search service for research. Use OpenAI Images or another identity-preserving image editor for mockups. See [architecture](docs/architecture.md).

## Current boundary

This v0.1 SDK is the workflow kernel, not a furniture-fit simulator. It validates the process and produces visual concepts plus setup instructions; exact measurements still require room dimensions or a sweep video.

## License

MIT
