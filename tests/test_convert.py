from pathlib import Path
from typstpresenter.model.Presentation import Presentation

def test_simple_presentation_conversion():
    test_file = Path(__file__).parent / "data" / "simple.pptx"
    assert test_file.exists(), "Test data missing, please run generate_test_data.py"

    presentation = Presentation.from_file(test_file)

    # The title slide becomes the PresentationTitle metadata, not a regular slide
    assert presentation.title is not None
    # Depending on how the title is extracted, we can check its text
    assert len(presentation.slides) == 1

    # Get Typst string
    typst_output = presentation.to_typst_str()
    print(typst_output)
    
    assert "Hello World Presentation" in typst_output or "A simple subtitle" in typst_output or "Slide 1 Title" in typst_output
    assert "This is a bullet point" in typst_output

def test_two_content_blocks(caplog):
    test_file = Path(__file__).parent / "data" / "two_content.pptx"
    assert test_file.exists(), "Test data missing, please run generate_test_data.py"

    presentation = Presentation.from_file(test_file)
    
    # Depending on how the elements are parsed, only one content should make it into the typst result
    typst_output = presentation.to_typst_str()
    print(typst_output)

    # We now expect BOTH content blocks to be rendered inside a Grid markup without dropping.
    assert "#grid(" in typst_output
    assert "columns: 2" in typst_output
    
    assert "Left content block" in typst_output
    assert "Right content block" in typst_output

