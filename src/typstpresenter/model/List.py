from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import overload

from typstpresenter.model.Element import Element
from typstpresenter.model.text.Text import Text


@dataclass(frozen=True)
class List(Element, Sequence):
    items: Sequence[Text | List]

    def append(self, *items: Text | List) -> List:
        return List(items=tuple(self.items) + tuple(items))

    def __len__(self) -> int:
        return len(self.items)

    @overload
    def __getitem__(self, index: int) -> Text | List: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[Text | List]: ...

    def __getitem__(self, index):
        return self.items[index]
