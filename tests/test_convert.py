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
    assert "columns: (1fr, 1fr)" in typst_output
    
    assert "Two content layout, left block." in typst_output
    assert "Two content layout, right block." in typst_output

def test_multi_content_blocks(caplog):
    test_file = Path(__file__).parent / "data" / "multi_content.pptx"
    assert test_file.exists(), "Test data missing, please run generate_test_data.py"

    presentation = Presentation.from_file(test_file)
    typst_output = presentation.to_typst_str()
    print(typst_output)

    # Some basic expectations for multi_content, acknowledging that complex grid interpretation
    # might not be fully supported by Slide.py yet (which makes this test fail, and that's okay).
    
    assert "Two Rows Layout" in typst_output
    assert "Two rows setup, top row (1/2)." in typst_output
    
    assert "Three Rows Layout" in typst_output
    assert "Three rows setup, row 1 of 3." in typst_output
    
    assert "Full 2x2 Grid" in typst_output
    assert "Full 2x2 grid, placeholder 1 of 4 (top-left)." in typst_output
    
    # We'd expect grids with potentially more than 2 columns/rows or sequences
    assert "Sequential Grid (4/4)" in typst_output

def test_media_conversion(caplog, tmp_path):
    test_file = Path(__file__).parent / "data" / "media.pptx"
    assert test_file.exists(), "Test data missing, please run generate_test_data.py"

    presentation = Presentation.from_file(test_file)
    
    # Save the presentation to the tmp_path to verify media extraction
    out_file = tmp_path / "media_test.typ"
    presentation.to_file(out_file)
    
    assert out_file.exists()
    typst_output = out_file.read_text(encoding="utf-8")
    
    # By default, to_file sets media_dir to the file's stem + "_media"
    expected_media_dir = "media_test_media"
    media_dir_path = out_file.parent / expected_media_dir
    assert media_dir_path.exists()
    assert media_dir_path.is_dir()
    
    # Check that there is at least one image inside the directory
    extracted_images = list(media_dir_path.glob("*.*"))
    assert len(extracted_images) >= 1
    
    # Check that the typst_output includes an #image() reference
    image_rel_path = f"{expected_media_dir}/{extracted_images[0].name}".replace("\\", "/")
    assert f'#image("{image_rel_path}"' in typst_output
