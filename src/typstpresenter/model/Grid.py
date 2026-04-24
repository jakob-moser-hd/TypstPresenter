from dataclasses import dataclass
from collections.abc import Sequence
from typstpresenter.model.Element import Element

@dataclass(frozen=True)
class Grid(Element):
    """
    A logical grid formatting structure to be utilized by Typst templates.
    """
    columns: int
    items: Sequence[Element]
