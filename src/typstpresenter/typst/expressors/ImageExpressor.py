from __future__ import annotations

from typing import Any, Callable

from typstpresenter.model.Element import Element
from typstpresenter.model.Image import Image


class ImageExpressor:
    def can_express(self, element: Element | str | None) -> bool:
        return isinstance(element, Image)

    def __call__(self, element: Any, express: Callable[[Element | str | None], str], context: Any) -> str:
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
