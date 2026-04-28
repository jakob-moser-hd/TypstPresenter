from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element
from typstpresenter.model.text.Superscript import Superscript


class SuperscriptExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, Superscript)

    def __call__(self, element: Any, express: Callable[[Element | str | None], str], context: Any) -> str:
        return f"#super[{express(element.text)}]"
