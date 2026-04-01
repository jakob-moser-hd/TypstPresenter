from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Self, overload

import pptx

from typstpresenter.model.Slide import Slide
from typstpresenter.typst.express import express


@dataclass
class Presentation(Sequence[Slide]):
    slides: Sequence[Slide]

    # The path to the source file (if sourced from a file)
    source_path: Path | None = None

    @classmethod
    def from_file(cls, path: Path) -> Self:
        """
        Load a presentation from the file at the given path.

        Currently assumes that the path points to a *.pptx file, no other file types can be handled.
        Will fail if other files are presented, possibly in curious ways.
        """
        prs = pptx.Presentation(str(path))
        return cls(
            slides=tuple(
                Slide.from_pptx_slide(pptx_slide) for pptx_slide in prs.slides
            ),
            source_path=path,
        )

    def to_typst_str(self) -> str:
        """
        Convert the presentation to a string in Typst format and return it.
        """
        return express(self)

    def to_file(self, path: Path) -> None:
        """
        Save a presentation to the given path.

        Will output the file in *.typ (Typst) format, no matter the extension.
        """
        with path.open("w", encoding="utf-8") as f:
            f.write(self.to_typst_str())

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> Slide: ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence[Slide]: ...

    def __getitem__(self, index):
        return self.slides[index]

    def __len__(self) -> int:
        return len(self.slides)
