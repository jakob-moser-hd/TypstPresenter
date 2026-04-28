from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element
from typstpresenter.model.Grid import Grid


class GridExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, Grid)

    def __call__(self, element: Any, express: Callable[[Element | str | None], str], context: Any) -> str:
        items = ",\n".join(f"  [{express(item)}]" for item in element.items)
        cols = ", ".join(["1fr"] * element.columns)
        columns_value = f"({cols})" if element.columns > 1 else "1fr"
        return f"#grid(\n  columns: {columns_value},\n  gutter: 1em,\n{items}\n)"
