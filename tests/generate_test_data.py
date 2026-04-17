import pptx
from pathlib import Path

def create_simple_pptx(path: Path):
    prs = pptx.Presentation()
    
    # Title Slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Hello World Presentation"
    subtitle.text = "A simple subtitle"
    
    # Bullet Slide
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    
    title_shape.text = "Slide 1 Title"
    
    tf = body_shape.text_frame
    tf.text = "This is a bullet point"
    
    p = tf.add_paragraph()
    p.text = "This is a second bullet point"
    
    prs.save(path)

def create_two_content_pptx(path: Path):
    prs = pptx.Presentation()
    
    # Title Slide (extracted as metadata, so the content slide must be 2nd)
    title_slide_layout = prs.slide_layouts[0]
    prs.slides.add_slide(title_slide_layout)
    
    # "Two Content" slide is usually layout index 3 in the default template
    slide_layout = prs.slide_layouts[3]
    slide = prs.slides.add_slide(slide_layout)
    shapes = slide.shapes
    
    title_shape = shapes.title
    title_shape.text = "Two Content Slide"
    
    # Typically, placeholders[1] and [2] are the two content boxes
    body_shape_1 = shapes.placeholders[1]
    body_shape_2 = shapes.placeholders[2]
    
    body_shape_1.text_frame.text = "Left content block"
    body_shape_2.text_frame.text = "Right content block"
    
    prs.save(path)

if __name__ == "__main__":
    out_dir = Path("tests/data")
    out_dir.mkdir(exist_ok=True, parents=True)
    create_simple_pptx(out_dir / "simple.pptx")
    create_two_content_pptx(out_dir / "two_content.pptx")
