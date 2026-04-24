import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Compiler:

    def __init__(self) -> None:
        try:
            subprocess.run(["typst", "--version"], check=True)
        except FileNotFoundError as e:
            e.add_note("The 'typst' CLI was not found, which is necessary to compile *.typ files. Please ensure typst is installed and in your PATH.")
            raise e

    def compile(self, typst_path: Path) -> None:
        subprocess.run(["typst", "compile", str(typst_path)], check=True)
