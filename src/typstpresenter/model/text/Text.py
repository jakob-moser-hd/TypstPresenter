from collections.abc import Sequence
from dataclasses import dataclass

from typstpresenter.model.Element import Element
from typstpresenter.model.text.Atom import Atom


@dataclass(frozen=True)
class Text(Element):
    value: Sequence[Atom]

    def __str__(self) -> str:
        return "".join(str(v) for v in self.value)
