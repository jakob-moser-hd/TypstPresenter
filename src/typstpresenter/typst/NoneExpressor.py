from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element


class NoneExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return element is None

    def __call__(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return ""
