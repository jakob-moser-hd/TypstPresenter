from __future__ import annotations

from typing import Protocol, Callable, Any, Generic

from typstpresenter.model.Element import Element


class Expressor[T: Element | str | None](Protocol):
    def can_express(self, element: Element | str | None) -> bool:
        ...

    def __call__(self, element: T, express: Callable[[Element | str | None], str], context: Any) -> str:
        ...
