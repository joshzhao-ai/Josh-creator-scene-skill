from __future__ import annotations

import base64
from pathlib import Path

from .models import Direction, Project


class OpenAIImageGenerator:
    """GPT Image adapter. The workflow engine remains usable without this dependency."""

    def __init__(
        self,
        *,
        model: str = "gpt-image-2",
        quality: str = "medium",
        size: str = "auto",
        input_fidelity: str = "high",
        client: object | None = None,
    ) -> None:
        if client is None:
            try:
                from openai import OpenAI
            except ImportError as exc:  # pragma: no cover - depends on optional package
                raise RuntimeError(
                    "Install the OpenAI adapter with: pip install 'creator-scene-director[openai]'"
                ) from exc
            client = OpenAI()
        self.client = client
        self.model = model
        self.quality = quality
        self.size = size
        self.input_fidelity = input_fidelity

    def generate(self, project: Project, direction: Direction, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with Path(project.source_image).open("rb") as source:
            response = self.client.images.edit(  # type: ignore[attr-defined]
                model=self.model,
                image=source,
                prompt=direction.prompt,
                quality=self.quality,
                size=self.size,
                input_fidelity=self.input_fidelity,
                output_format="png",
            )
        encoded = response.data[0].b64_json
        if not encoded:
            raise RuntimeError("Image provider returned no base64 image data")
        output_path.write_bytes(base64.b64decode(encoded))
        return output_path
