from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element


class StringExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, str)

    def __call__(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        # TODO Improve escaping logic
        escaped = element.replace("*", r"\*").replace("~", r"\~")
        escaped = escaped.replace("[", r"\[").replace("]", r"\]")
        return escaped
