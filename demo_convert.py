import sys
import subprocess
from pathlib import Path
from typstpresenter.model.Presentation import Presentation

def main():
    if len(sys.argv) < 2:
        print("Usage: python demo_convert.py <path_to_pptx>")
        sys.exit(1)
        
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"Error: File {input_file} does not exist.")
        sys.exit(1)
        
    print(f"Loading presentation from {input_file}...")
    try:
        presentation = Presentation.from_file(input_file)
    except Exception as e:
        print(f"Error loading presentation: {e}")
        sys.exit(1)
    
    output_dir = Path("tests/results_tmp")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    typ_output_path = output_dir / input_file.with_suffix('.typ').name
    print(f"Generating Typst source to {typ_output_path}...")
    typst_str = presentation.to_typst_str()
    
    with open(typ_output_path, 'w', encoding='utf-8') as f:
        f.write(typst_str)
        
    print(f"Compiling Typst file to PDF...")
    try:
        subprocess.run(["typst", "compile", str(typ_output_path)], check=True)
        pdf_output_path = typ_output_path.with_suffix('.pdf')
        print(f"Successfully generated {pdf_output_path}")
    except FileNotFoundError:
        print("Error: 'typst' CLI not found. Please ensure typst is installed and in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Typst file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
