from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Callable, Any

from jinja2 import Environment, PackageLoader, select_autoescape, pass_context

from typstpresenter.model.Element import Element
from typstpresenter.model.List import List
from typstpresenter.model.Grid import Grid
from typstpresenter.model.PresentationTitle import PresentationTitle
from typstpresenter.model.Title import Title
from typstpresenter.model.text.Link import Link
from typstpresenter.model.text.Subscript import Subscript
from typstpresenter.model.text.Superscript import Superscript
from typstpresenter.model.text.Text import Text

if TYPE_CHECKING:
    from typstpresenter.model.Presentation import Presentation


_jinja_env = Environment(
    loader=PackageLoader("typstpresenter"), autoescape=select_autoescape()
)


def express(presentation: Presentation, media_dir: str = "media") -> str:
    """
    Express a presentation represented in an abstract format as a Typst string.
    """
    return _jinja_env.get_template("typst/presentation.diatypst.typ").render(
        presentation=presentation, media_dir=media_dir
    )


def _indent(string: str) -> str:
    return "\n".join(f"  {line}" for line in string.split("\n"))


def _indent_or_add_dash(criterion: bool, string: str) -> str:
    return _indent(string) if criterion else f"- {string}"


class ExpressionHandler(Protocol):
    def can_handle(self, element: Element | str | None) -> bool:
        ...

    def express(self, element: Element | str | None, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        ...


_EXPRESSION_HANDLERS: list[ExpressionHandler] = []


def register_expression_handler(handler: ExpressionHandler) -> None:
    _EXPRESSION_HANDLERS.append(handler)


class LinkHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Link)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return f'#link("{element.target}")[{dispatcher(element.text)}]'


class TextHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Text)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return "".join(dispatcher(x) for x in element.value)


class SubscriptHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Subscript)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return f"#sub[{dispatcher(element.text)}]"


class SuperscriptHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Superscript)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return f"#super[{dispatcher(element.text)}]"


class ListHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, List)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return "\n".join(_indent_or_add_dash(isinstance(item, List), dispatcher(item)) for item in element.items)


class GridHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Grid)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        items = ",\n".join(f"  [{dispatcher(item)}]" for item in element.items)
        cols = ", ".join(["1fr"] * element.columns)
        columns_value = f"({cols})" if element.columns > 1 else "1fr"
        return f"#grid(\n  columns: {columns_value},\n  gutter: 1em,\n{items}\n)"


class ImageHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        from typstpresenter.model.MediaImage import Image
        return isinstance(element, Image)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        media_dir = context.get('media_dir', 'media')
        import posixpath
        img_path = posixpath.join(media_dir, element.name)
        
        args = [f'"{img_path}"']
        
        # PowerPoint coordinates (defaults to 10"x7.5" = 720x540pt) are larger than Datypst
        # default coordinates (approx 14cm wide = 396.85pt). Multiplier ~ 0.55118.
        scale = 0.55118
        if element.width_pt is not None:
            args.append(f"width: {element.width_pt * scale:.2f}pt")
        if element.height_pt is not None:
            args.append(f"height: {element.height_pt * scale:.2f}pt")
            
        return f"#image({', '.join(args)})"

class TitleHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Title) or isinstance(element, PresentationTitle)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return dispatcher(element.text)


class StringHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, str)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        # TODO Improve escaping logic
        escaped = element.replace("*", r"\*").replace("~", r"\~")
        escaped = escaped.replace("[", r"\[").replace("]", r"\]")
        return escaped


class NoneHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return element is None

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return ""


class FallbackHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return True

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str], context: Any) -> str:
        return str(element)


register_expression_handler(LinkHandler())
register_expression_handler(TextHandler())
register_expression_handler(SubscriptHandler())
register_expression_handler(SuperscriptHandler())
register_expression_handler(ListHandler())
register_expression_handler(GridHandler())
register_expression_handler(ImageHandler())
register_expression_handler(TitleHandler())
register_expression_handler(StringHandler())
register_expression_handler(NoneHandler())
register_expression_handler(FallbackHandler())


@pass_context
def _express_element(context: Any, element: Element | str | None) -> str:
    def dispatcher(e: Element | str | None) -> str:
        return _express_element(context, e)

    for handler in _EXPRESSION_HANDLERS:
        if handler.can_handle(element):
            return handler.express(element, dispatcher, context)
    return str(element)


# This way, you can say something in Jinja like `{{ slide.title | express }}` and Jinja will apply the _express_element
# function to it, which renders stuff to Typst
_jinja_env.filters["express"] = _express_element
