from typing import Protocol

from pptx.shapes import Subshape
from pptx.shapes.base import BaseShape

from typstpresenter.model.Element import Element
from typstpresenter.powerpoint.Ignore import Ignore


class Interpreter(Protocol):
    def can_interpret(self, shape: BaseShape | Subshape) -> bool:
        ...

    def __call__(self, shape: BaseShape | Subshape, context: dict | None = None) -> Element | Ignore | None:
        ...
