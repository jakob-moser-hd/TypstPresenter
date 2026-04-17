import logging
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property
from typing import Self

import pptx.slide
from pptx.shapes.base import BaseShape

from typstpresenter.model.Element import Element
from typstpresenter.model.Title import Title
from typstpresenter.powerpoint.flatten import flatten
from typstpresenter.powerpoint.interpret import interpret


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Slide:
    elements: Sequence[Element]
    shapes: Sequence[BaseShape]

    @cached_property
    def title(self) -> Title | None:
        return self.get_singular_element_or_none(Title)

    @cached_property
    def contents(self) -> Sequence[Element]:
        """
        Return the content elements of the slide.
        """
        # Currently, everything which is not the title is content
        return tuple(e for e in self.elements if not isinstance(e, Title))

    def get_singular_element_or_none[T: Element](self, t: type[T]) -> T | None:
        elements = tuple(e for e in self.elements if isinstance(e, t))

        if not elements:
            return None

        if len(elements) > 1:
            raise ValueError(
                f"Slide had {len(elements)} elements of type {t}, but should have either 0 or 1."
            )

        return elements[0]

    @classmethod
    def from_pptx_slide(cls, pptx_slide: pptx.slide.Slide) -> Self:
        # pptx_slide.slide_layout.name contains the layout name, which is often rather useless, as it can be
        # "Titel und Inhalt" irrespective of whether the slide contains structured bullet-points or completely
        # free floating thought bubbles.

        elements_and_shapes = tuple(
            interpret(shape) or shape for shape in flatten(pptx_slide.shapes)
        )

        return cls(
            elements=tuple(x for x in elements_and_shapes if isinstance(x, Element)),
            shapes=tuple(x for x in elements_and_shapes if isinstance(x, BaseShape)),
        )
