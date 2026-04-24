from dataclasses import dataclass


@dataclass(frozen=True)
class Element:
    """
    A thing that can be on a slide.
    """

    pass


@dataclass(frozen=True)
class PlacedElement:
    """
    An element placed on a slide, complete with physical positional footprint details.
    """

    element: Element
    left: int | float | None = None
    top: int | float | None = None
    width: int | float | None = None
    height: int | float | None = None

