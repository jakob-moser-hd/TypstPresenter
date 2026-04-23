from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element
from typstpresenter.model.PresentationTitle import PresentationTitle
from typstpresenter.model.Title import Title


class TitleExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, Title) or isinstance(element, PresentationTitle)

    def __call__(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return dispatcher(element.text)
