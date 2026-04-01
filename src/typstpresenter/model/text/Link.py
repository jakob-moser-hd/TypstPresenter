from dataclasses import dataclass

from typstpresenter.model.Element import Element
from typstpresenter.model.text.Text import Text


@dataclass(frozen=True)
class Link(Element):
    text: Text
    target: str

    def __str__(self) -> str:
        return str(self.text)
