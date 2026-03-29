import typer
import logging
from pathlib import Path
from typing import Annotated

from typstpresenter.model.Presentation import Presentation


app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def stats(
    presentation_dir: Annotated[
        Path,
        typer.Argument(
            help="Path to a directory containing *.pptx files (or subdirectories with *.pptx files)"
        ),
    ],
) -> None:
    """
    Calculate statistics for all presentations found in the given folder or any of its subfolders.

    Statistics can be used to judge how much effort a batch migration will be.
    """
    presentations = (
        Presentation.from_file(pptx_path)
        for pptx_path in presentation_dir.rglob("*.pptx")
    )

    for presentation in presentations:
        print(presentation.slides)
