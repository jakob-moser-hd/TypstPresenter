from dataclasses import dataclass
from typing import Self
from pathlib import Path
from collections.abc import Sequence

from typstpresenter.model.Slide import Slide

import pptx


@dataclass
class Presentation:
    slides: Sequence[Slide]

    # The path to the source file (if sourced from a file)
    source_path: Path | None = None

    @classmethod
    def from_file(cls, path: Path) -> Self:
        prs = pptx.Presentation(str(path))
        return cls(
            slides=tuple(
                Slide.from_pptx_slide(pptx_slide) for pptx_slide in prs.slides
            ),
            source_path=path,
        )
