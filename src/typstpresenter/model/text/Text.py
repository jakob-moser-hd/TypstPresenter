from dataclasses import dataclass

from typstpresenter.model.Element import Element


@dataclass(frozen=True)
class Text(Element):
    value: str

    def __str__(self) -> str:
        return self.value
