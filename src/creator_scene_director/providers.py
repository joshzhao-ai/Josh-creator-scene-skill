from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .models import CreatorReference, Direction, Project


class ReferenceResearcher(Protocol):
    """Adapter for Agent Reach, a browser agent, a custom search API, or manual review."""

    def research(self, project: Project) -> list[CreatorReference]: ...


class MockupGenerator(Protocol):
    """Adapter for any identity-preserving image editing provider."""

    def generate(self, project: Project, direction: Direction, output_path: Path) -> Path: ...

