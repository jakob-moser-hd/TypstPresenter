from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element
from typstpresenter.model.List import List
from typstpresenter.typst.express import _indent_or_add_dash


class ListExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, List)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return "\n".join(_indent_or_add_dash(isinstance(item, List), dispatcher(item)) for item in element.items)
