from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typstpresenter.model.text.Link import Link

type Atom = str | Link
