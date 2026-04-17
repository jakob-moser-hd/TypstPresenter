import logging
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property
from typing import Self

import pptx.slide
from pptx.shapes.base import BaseShape

from typstpresenter.model.Element import Element, PlacedElement
from typstpresenter.model.Grid import Grid
from typstpresenter.model.Title import Title
from typstpresenter.powerpoint.flatten import flatten
from typstpresenter.powerpoint.interpret import interpret


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Slide:
    elements: Sequence[PlacedElement]
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
        content_placed = [e for e in self.elements if not isinstance(e.element, Title)]
        
        # Try to detect grid layout
        if len(content_placed) == 2:
            pe1, pe2 = content_placed[0], content_placed[1]
            if pe1.left is not None and pe2.left is not None:
                # Check if they are offset horizontally (side-by-side)
                if pe1.left != pe2.left:
                    ordered = sorted([pe1, pe2], key=lambda x: x.left)
                    return (Grid(columns=2, items=[pe.element for pe in ordered]),)

        return tuple(e.element for e in content_placed)

    def get_singular_element_or_none[T: Element](self, t: type[T]) -> T | None:
        elements = tuple(e.element for e in self.elements if isinstance(e.element, t))

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
            (interpret(shape), shape) for shape in flatten(pptx_slide.shapes)
        )

        placed_elements = []
        for element, shape in elements_and_shapes:
            if isinstance(element, Element):
                placed = PlacedElement(
                    element=element,
                    left=getattr(shape, "left", None),
                    top=getattr(shape, "top", None),
                    width=getattr(shape, "width", None),
                    height=getattr(shape, "height", None),
                )
                placed_elements.append(placed)

        return cls(
            elements=tuple(placed_elements),
            shapes=tuple(shape for _, shape in elements_and_shapes if isinstance(shape, BaseShape)),
        )
