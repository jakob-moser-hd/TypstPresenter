from pptx.enum.shapes import PP_PLACEHOLDER_TYPE
from pptx.shapes.base import BaseShape
from pptx.shapes.placeholder import SlidePlaceholder

from typstpresenter.model.Element import Element
from typstpresenter.model.Title import Title
from typstpresenter.powerpoint.Ignore import Ignore


def _interpret_placeholder(shape: SlidePlaceholder) -> Element | Ignore | None:
    """
    Interpret a shape of type SlidePlaceholder.

    These are somewhat nicer to interpret, because some of them have a type assigned which is actually semantic.

    See: https://python-pptx.readthedocs.io/en/latest/user/understanding-shapes.html
    """

    match shape.placeholder_format.type:
        case PP_PLACEHOLDER_TYPE.TITLE:
            return Title(text=shape.text)
        case PP_PLACEHOLDER_TYPE.SLIDE_NUMBER:
            return Ignore()
        case _:
            return None


def interpret(shape: BaseShape) -> Element | None:
    """
    Interpret a shape coming from a PowerPoint.

    Interpreting a shape means converting it to an Element, i.e., an instance from our abstraction layer which
    we control. If a shape cannot be interpreted, this returns None.
    """
    match shape:
        case SlidePlaceholder():
            return _interpret_placeholder(shape)
        case _:
            return None
