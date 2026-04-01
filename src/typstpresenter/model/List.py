from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from typstpresenter.model.Element import Element
from typstpresenter.model.text.Text import Text


@dataclass(frozen=True)
class List(Element):
    items: Sequence[Text | List]
