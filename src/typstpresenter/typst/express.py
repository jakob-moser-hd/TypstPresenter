from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Callable, Any

from jinja2 import Environment, PackageLoader, select_autoescape

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


def express(presentation: Presentation) -> str:
    """
    Express a presentation represented in an abstract format as a Typst string.
    """
    return _jinja_env.get_template("typst/presentation.diatypst.typ").render(
        presentation=presentation
    )


def _indent(string: str) -> str:
    return "\n".join(f"  {line}" for line in string.split("\n"))


def _indent_or_add_dash(criterion: bool, string: str) -> str:
    return _indent(string) if criterion else f"- {string}"


class ExpressionHandler(Protocol):
    def can_handle(self, element: Element | str | None) -> bool:
        ...

    def express(self, element: Element | str | None, dispatcher: Callable[[Element | str | None], str]) -> str:
        ...


_EXPRESSION_HANDLERS: list[ExpressionHandler] = []


def register_expression_handler(handler: ExpressionHandler) -> None:
    _EXPRESSION_HANDLERS.append(handler)


class LinkHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Link)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        return f'#link("{element.target}")[{dispatcher(element.text)}]'


class TextHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Text)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        return "".join(dispatcher(x) for x in element.value)


class SubscriptHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Subscript)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        return f"#sub[{dispatcher(element.text)}]"


class SuperscriptHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Superscript)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        return f"#super[{dispatcher(element.text)}]"


class ListHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, List)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        return "\n".join(_indent_or_add_dash(isinstance(item, List), dispatcher(item)) for item in element.items)


class GridHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Grid)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        items = ",\n".join(f"  [{dispatcher(item)}]" for item in element.items)
        cols = ", ".join(["1fr"] * element.columns)
        columns_value = f"({cols})" if element.columns > 1 else "1fr"
        return f"#grid(\n  columns: {columns_value},\n  gutter: 1em,\n{items}\n)"


class TitleHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, Title) or isinstance(element, PresentationTitle)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        return dispatcher(element.text)


class StringHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return isinstance(element, str)

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        # TODO Improve escaping logic
        return element.replace("*", r"\\*").replace("~", r"\\~")


class NoneHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return element is None

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        return ""


class FallbackHandler:
    def can_handle(self, element: Element | str | None) -> bool:
        return True

    def express(self, element: Any, dispatcher: Callable[[Element | str | None], str]) -> str:
        return str(element)


register_expression_handler(LinkHandler())
register_expression_handler(TextHandler())
register_expression_handler(SubscriptHandler())
register_expression_handler(SuperscriptHandler())
register_expression_handler(ListHandler())
register_expression_handler(GridHandler())
register_expression_handler(TitleHandler())
register_expression_handler(StringHandler())
register_expression_handler(NoneHandler())
register_expression_handler(FallbackHandler())


def _express_element(element: Element | str | None) -> str:
    for handler in _EXPRESSION_HANDLERS:
        if handler.can_handle(element):
            return handler.express(element, _express_element)
    return str(element)


# This way, you can say something in Jinja like `{{ slide.title | express }}` and Jinja will apply the _express_element
# function to it, which renders stuff to Typst
_jinja_env.filters["express"] = _express_element
