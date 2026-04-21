from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element
from typstpresenter.model.text.Link import Link


class LinkExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, Link)

    def __call__(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return f'#link("{element.target}")[{dispatcher(element.text)}]'
