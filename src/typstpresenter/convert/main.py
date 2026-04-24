import logging
import multiprocessing
from pathlib import Path
from typing import Annotated

import typer

from typstpresenter.model.Presentation import Presentation
from typstpresenter.typst.Compiler import Compiler

app = typer.Typer()
logger = logging.getLogger(__name__)


def convert_single(pptx_path: Path, maybe_compiler: Compiler | None, output_path: Path | None) -> None:
    """
    Convert a single *.pptx file to a *.typ file.

    If a compiler is given, also compile it to a *.pdf.
    """
    presentation = Presentation.from_file(pptx_path)

    typst_path = (pptx_path if not output_path else output_path / pptx_path.relative_to(pptx_path.parent)).with_suffix(".typ")

    presentation.to_file(typst_path)

    if maybe_compiler:
        maybe_compiler.compile(typst_path)


@app.command()
def convert(
    pptx_paths: Annotated[
        list[Path],
        typer.Argument(help="One or more paths to *.pptx files"),
    ],
    compile: Annotated[
        bool,
        typer.Option(help="If the final presentation *.pdf should also automatically be built from the PDF"),
    ],
    output_path: Annotated[
        Path | None,
        typer.Option("--output-path", "-o", help="Path to a directory in which all output files should be stored")
    ] = None,
) -> None:
    """
    Convert a given presentation or set of presentations from PPTX to Typst.

    The output path is inferred from the PPTX paths, by replacing *.pptx with *.typ.
    """
    maybe_compiler = Compiler() if compile else None

    if output_path:
        output_path.mkdir(parents=True, exist_ok=True)

    with multiprocessing.Pool() as p:
        p.starmap(convert_single, ((path, maybe_compiler, output_path) for path in pptx_paths))
