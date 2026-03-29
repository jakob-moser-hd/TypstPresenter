import logging

import typer


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] @%(name)s:%(lineno)d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("typstpresenter")
logger.setLevel(logging.INFO)


app = typer.Typer(pretty_exceptions_show_locals=False)

if __name__ == "__main__":
    app()
