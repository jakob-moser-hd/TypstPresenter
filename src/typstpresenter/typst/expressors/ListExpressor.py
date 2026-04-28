from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element
from typstpresenter.model.List import List


class ListExpressor:

    def __indent(self, string: str) -> str:
        return "\n".join(f"  {line}" for line in string.split("\n"))

    def __indent_or_add_dash(self, criterion: bool, string: str) -> str:
        return self.__indent(string) if criterion else f"- {string}"

    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, List)

    def __call__(self, element: Any, express: Callable[[Element | str | None], str], context: Any) -> str:
        return "\n".join(self.__indent_or_add_dash(isinstance(item, List), express(item)) for item in element.items)
