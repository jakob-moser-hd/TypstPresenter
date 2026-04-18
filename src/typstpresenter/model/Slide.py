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
        
        # Only try to make a grid if we have at least 1 element and all contents have coordinates
        if len(content_with_coords) >= 1 and len(content_with_coords) == len(content_placed):
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

            # --- Heuristics to infer missing grid dimensions ---
            if num_cols == 1:
                widths = [e.width for e in content_with_coords if e.width is not None]
                if widths:
                    max_w = max(widths)
                    # 3 columns if width < ~3.2 inches (2900000)
                    if max_w < 2900000: num_cols = 3
                    # 2 columns if width < ~5.3 inches (4800000)
                    elif max_w < 4800000: num_cols = 2
                    
            if num_rows == 1:
                heights = [e.height for e in content_with_coords if e.height is not None]
                if heights:
                    max_h = max(heights)
                    # 3 rows if height < ~2.0 inches (1828800)
                    if max_h < 1800000: num_rows = 3
                    # 2 rows if height < ~4.2 inches (3800000)
                    elif max_h < 3800000: num_rows = 2
            
            # If we detect some structure, put them into a Grid
            if num_cols > 1 or num_rows > 1:
                grid_items = [None] * (num_cols * num_rows)
                for e in content_with_coords:
                    # Find column index
                    if len(lefts) == num_cols:
                        col_idx = 0
                        for i, l in enumerate(lefts):
                            if abs(e.left - l) < TOLERANCE: col_idx = i; break
                    else:
                        if num_cols == 2: col_idx = 0 if e.left < 4500000 else 1
                        elif num_cols == 3: col_idx = 0 if e.left < 3000000 else (1 if e.left < 6000000 else 2)
                        else: col_idx = 0
                    
                    # Find row index
                    if len(tops) == num_rows:
                        row_idx = 0
                        for i, t in enumerate(tops):
                            if abs(e.top - t) < TOLERANCE: row_idx = i; break
                    else:
                        if num_rows == 2: row_idx = 0 if e.top < 3500000 else 1
                        elif num_rows == 3: row_idx = 0 if e.top < 2600000 else (1 if e.top < 5200000 else 2)
                        else: row_idx = 0
                    
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
    def from_pptx_slide(cls, pptx_slide: pptx.slide.Slide, slide_index: int = 0) -> Self:
        # pptx_slide.slide_layout.name contains the layout name, which is often rather useless, as it can be
        # "Titel und Inhalt" irrespective of whether the slide contains structured bullet-points or completely
        # free floating thought bubbles.

        elements_and_shapes = tuple(
            (interpret(shape, context={"slide_index": slide_index, "element_index": i}), shape) 
            for i, shape in enumerate(flatten(pptx_slide.shapes))
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
