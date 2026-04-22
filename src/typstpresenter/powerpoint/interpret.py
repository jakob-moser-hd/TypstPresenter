import logging
from itertools import groupby
from typing import Protocol

from pptx.enum.shapes import PP_PLACEHOLDER_TYPE
from pptx.shapes import Subshape
from pptx.shapes.base import BaseShape
from pptx.shapes.placeholder import SlidePlaceholder
from pptx.text.text import _Paragraph, TextFrame, _Run

from typstpresenter.model.Element import Element
from typstpresenter.model.List import List
from typstpresenter.model.PresentationTitle import PresentationTitle
from typstpresenter.model.Title import Title
from typstpresenter.model.text.Link import Link
from typstpresenter.model.text.Subscript import Subscript
from typstpresenter.model.text.Superscript import Superscript
from typstpresenter.model.text.Text import Text, Atom
from typstpresenter.powerpoint.Ignore import Ignore

logger = logging.getLogger(__name__)


class ShapeHandler(Protocol):
    def can_handle(self, shape: BaseShape | Subshape) -> bool:
        ...

    def interpret(self, shape: BaseShape | Subshape, context: dict | None = None) -> Element | Ignore | None:
        ...


_SHAPE_HANDLERS: list[ShapeHandler] = []


def register_shape_handler(handler: ShapeHandler) -> None:
    _SHAPE_HANDLERS.append(handler)


class SlidePlaceholderHandler:
    """
    Interpret a shape of type SlidePlaceholder.

    These are somewhat nicer to interpret, because some of them have a type assigned which is actually semantic.

    See: https://python-pptx.readthedocs.io/en/latest/user/understanding-shapes.html
    """
    def can_handle(self, shape: BaseShape | Subshape) -> bool:
        return isinstance(shape, SlidePlaceholder)

    def interpret(self, shape: BaseShape | Subshape, context: dict | None = None) -> Element | Ignore | None:
        if not isinstance(shape, SlidePlaceholder):
            return None
            
        match shape.placeholder_format.type:
            case PP_PLACEHOLDER_TYPE.TITLE:
                return Title(text=_interpret_text_frame(shape.text_frame, default_to_list=False))
            case PP_PLACEHOLDER_TYPE.CENTER_TITLE:
                return PresentationTitle(text=_interpret_text_frame(shape.text_frame, default_to_list=False))
            case PP_PLACEHOLDER_TYPE.SLIDE_NUMBER | PP_PLACEHOLDER_TYPE.HEADER | PP_PLACEHOLDER_TYPE.FOOTER | PP_PLACEHOLDER_TYPE.DATE:
                return Ignore()
            case PP_PLACEHOLDER_TYPE.SUBTITLE:
                return _interpret_text_frame(shape.text_frame, default_to_list=False)
            case PP_PLACEHOLDER_TYPE.OBJECT:
                # Just pretend that object means a bunch of text, and nothing else.
                return _interpret_text_frame(shape.text_frame, default_to_list=False)
            case _:
                return None


register_shape_handler(SlidePlaceholderHandler())


class TextBoxHandler:
    """
    Interpret generic shapes that contain a text frame (e.g. manually added text boxes).
    """
    def can_handle(self, shape: BaseShape | Subshape) -> bool:
        return hasattr(shape, "text_frame") and not isinstance(shape, SlidePlaceholder)

    def interpret(self, shape: BaseShape | Subshape, context: dict | None = None) -> Element | Ignore | None:
        if hasattr(shape, "text_frame") and getattr(shape, "has_text_frame", False):
            return _interpret_text_frame(shape.text_frame, default_to_list=False)
        return None

register_shape_handler(TextBoxHandler())


class PictureHandler:
    def can_handle(self, shape: BaseShape | Subshape) -> bool:
        from pptx.enum.shapes import MSO_SHAPE_TYPE
        return hasattr(shape, "shape_type") and shape.shape_type == MSO_SHAPE_TYPE.PICTURE
        
    def interpret(self, shape: BaseShape | Subshape, context: dict | None = None) -> Element | Ignore | None:
        from typstpresenter.model.Image import Image
        context = context or {}
        slide_idx = context.get("slide_index", 0)
        elem_idx = context.get("element_index", 0)
        
        ext = shape.image.ext
        name = f"slide_{slide_idx + 1}_pos_{elem_idx}.{ext}"
        blob = shape.image.blob
        width = getattr(shape, 'width', None)
        height = getattr(shape, 'height', None)
        width_pt = getattr(width, 'pt', None) if width else None
        height_pt = getattr(height, 'pt', None) if height else None
        return Image(name=name, ext=ext, blob=blob, width_pt=width_pt, height_pt=height_pt)

register_shape_handler(PictureHandler())


type Level = int


def _interpret_text_frame(text_frame: TextFrame, default_to_list: bool = True) -> Text | List:
    if len(text_frame.paragraphs) == 1:
        return _interpret_paragraph(text_frame.paragraphs[0])
        
    if not default_to_list:
        atoms = []
        for p in text_frame.paragraphs:
            atoms.extend(_interpret_paragraph(p).value)
            atoms.append("\n")
        if atoms:
            atoms.pop()
        return Text(tuple(atoms))

    # Just pretend any multi-paragraph text is a list
    paragraphs_by_level = groupby(text_frame.paragraphs, key=lambda item: item.level)
    list_stack: list[tuple[Level, List]] = []

    for level, paragraphs in paragraphs_by_level:
        list_ = List(tuple(_interpret_paragraph(p) for p in paragraphs))

        if len(list_stack) > 0:
            previous_level, previous_list = list_stack.pop()
        else:
            # Stack was previously empty, this only happens in the first iteration.
            previous_level, previous_list = -1, None

        # Go up the stack until we find a parent (i.e. one whose level is smaller than the current one).
        # If the current list is a root level, we'd empty the stack completely
        while len(list_stack) > 0 and level <= previous_level:
            previous_level, previous_list = list_stack.pop()

        if level > previous_level:
            if previous_list is not None:
                # This list has a parent, append it to the parent and put the barent back on the stack.
                list_stack.append((previous_level, previous_list.append(list_)))

            # Put the list itself on the stack because it is the level we are currently working at.
            list_stack.append((level, list_))
        elif level == previous_level:
            # If this list is on the same level as the previous one, concatenate both lists and keep the
            # earlier one.
            list_stack.append((previous_level, previous_list.append(*list_)))

    if list_stack:
        root_level, root_list = list_stack[0]

        return root_list
    else:
        logger.warning("Found ill-formed list, returning nothing")
        return Text(("",))


def _interpret_paragraph(paragraph: _Paragraph) -> Text:
    return Text(tuple(_interpret_run(run) for run in paragraph.runs))


# See https://stackoverflow.com/questions/61329224/how-do-i-add-superscript-subscript-text-to-powerpoint-using-python-pptx
_SUBSCRIPT = "-25000"
_SUPERSCRIPT = "30000"


def _interpret_run(run: _Run) -> Atom:
    if run.hyperlink.address is not None:
        return Link(text=Text(run.text), target=run.hyperlink.address)

    # The text baseline indicates how high in a line the run is positioned.
    baseline_position = run.font._element.get("baseline")

    if baseline_position == _SUBSCRIPT:
        return Subscript(text=Text(run.text))
    elif baseline_position == _SUPERSCRIPT:
        return Superscript(text=Text(run.text))

    return run.text


def interpret(shape: BaseShape | Subshape, context: dict | None = None) -> Element | None:
    """
    Interpret a shape (or a subshape, which is an element introduced as child of a shape) coming from a PowerPoint.

    Interpreting a shape means converting it to an Element, i.e., an instance from our abstraction layer which
    represents the contents of a PowerPoint independently of its presentation format. Multiple Handlers exist
    for different kinds of shapes.

    Returns the element (if recognized) or None if it should be completely ignored (such as slide numbers or pure design lines)
    """

    for handler in _SHAPE_HANDLERS:
        if handler.can_handle(shape):
            interpreted = handler.interpret(shape, context=context)

            # We could be more explicit in the return types maybe?
            # E.g. what should you do with a SlideTitle? It feels strange returning it here alongside regular texts.
            if isinstance(interpreted, Ignore):
                return None

            if isinstance(interpreted, Element):
                return interpreted

    logger.warning(
        f"Ignoring Shape {shape.shape_type if hasattr(shape, 'shape_type') else 'Unknown'}. Did not find a matching handler."
    )
    return None
