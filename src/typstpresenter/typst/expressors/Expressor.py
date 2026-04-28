from __future__ import annotations

from typing import Protocol, Callable, Any

from typstpresenter.model.Element import Element


class Expressor(Protocol):
    def can_express(self, element: Element | str | None) -> bool:
        ...

    def __call__(self, element: Element | str | None, express: Callable[[Element | str | None], str], context: Any) -> str:
        ...
