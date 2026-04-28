from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element
from typstpresenter.model.text.Text import Text


class TextExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, Text)

    def __call__(self, element: Any, express: Callable[[Element | str | None], str], context: Any) -> str:
        return "".join(express(x) for x in element.value)
