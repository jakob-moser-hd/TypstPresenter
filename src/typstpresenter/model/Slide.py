from dataclasses import dataclass
from typing import Self, Any


@dataclass
class Slide:
    @classmethod
    def from_pptx_slide(cls, pptx_slide: Any) -> Self:
        return cls()
