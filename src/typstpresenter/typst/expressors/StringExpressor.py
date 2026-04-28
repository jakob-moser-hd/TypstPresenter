from __future__ import annotations

from functools import reduce
from typing import Any, Callable

from typstpresenter.model.Element import Element


CHARS_TO_ESCAPE = ("*", "~", "[", "]", "#", "@", "<", ">")


class StringExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, str)

    def __call__(self, element: str, express: Callable[[Element | str | None], str], context: Any) -> str:
        # If it was hard to write, it should be hard to read.
        return reduce(lambda text, char: text.replace(char, rf"\{char}"), CHARS_TO_ESCAPE, element)
