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
        content_with_coords = [e for e in content_placed if e.left is not None and e.top is not None]
        
        # Only try to make a grid if we have at least 2 elements and all contents have coordinates
        if len(content_with_coords) >= 2 and len(content_with_coords) == len(content_placed):
            TOLERANCE = 150000  # EMU tolerance (about 0.16 inches)
            
            def cluster(values: list[float]) -> list[float]:
                if not values: return []
                values = sorted(values)
                clusters = []
                curr = [values[0]]
                for v in values[1:]:
                    if v - (sum(curr) / len(curr)) < TOLERANCE:
                        curr.append(v)
                    else:
                        clusters.append(sum(curr) / len(curr))
                        curr = [v]
                clusters.append(sum(curr) / len(curr))
                return clusters

            lefts = cluster([e.left for e in content_with_coords])
            tops = cluster([e.top for e in content_with_coords])
            
            num_cols = len(lefts)
            num_rows = len(tops)
            
            # If we detect some structure, put them into a Grid
            if num_cols > 1 or num_rows > 1:
                grid_items = [None] * (num_cols * num_rows)
                for e in content_with_coords:
                    # Find column index
                    col_idx = 0
                    for i, l in enumerate(lefts):
                        if abs(e.left - l) < TOLERANCE: col_idx = i; break
                    
                    # Find row index
                    row_idx = 0
                    for i, t in enumerate(tops):
                        if abs(e.top - t) < TOLERANCE: row_idx = i; break
                    
                    idx = row_idx * num_cols + col_idx
                    if idx < len(grid_items):
                        grid_items[idx] = e.element
                
                return (Grid(columns=num_cols, items=grid_items),)

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
