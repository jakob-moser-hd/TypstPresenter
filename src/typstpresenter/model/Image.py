from dataclasses import dataclass
from typstpresenter.model.Element import Element

@dataclass(frozen=True)
class Image(Element):
    name: str # The relative path it should be rendered at (e.g. Media/slide_1_image_0.png)
    blob: bytes
    ext: str
    width_pt: float | None = None
    height_pt: float | None = None
