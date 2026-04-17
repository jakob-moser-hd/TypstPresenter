# TypstPresenter Project Analysis

Here is the analysis of the project based on the current implementation in `src/typstpresenter`.

## 1. Current Status & Capabilities
**What is possible so far?**
The tool acts as a functioning proof-of-concept for PowerPoint to Typst conversion.
- It parses `.pptx` documents using `python-pptx`, flattening groups of shapes into easily accessible iterables.
- It translates text from **Slide Placeholders** (Titles, Body Text/Lists, Footers).
- In terms of styling, it supports extracting bold/italic variations indirectly, but explicitly maps **Subscripts, Superscripts, and Hyperlinks** to custom abstract syntax models (`Atom`, `Text`, `List`, `Link`).
- The project outputs a fully readable Typst file that utilizes the `diatypst` presentation package, compiled together via a Jinja2 template (`presentation.diatypst.typ`) to output Typst headers and body contents.

**Limitations:**
- It currently restricts each slide exclusively to a Title and exactly **1** content block, discarding other blocks with a logged warning (`Slide.content`).
- Manual shapes, explicit text boxes outside layout placeholders, and media are entirely ignored.

## 2. Next 3 Features / Progress Steps
1. **Multiple Content Elements & Basic Layout Integration**
   Currently, the framework assumes each `.pptx` slide has only one content element (`Slide.content` drops elements beyond index 0). Expanding the model to support multiple content elements (rendering them sequentially, or capturing position data to apply Typst alignments or columns) is the primary missing block to render a majority of traditional slides accurately.
2. **Support for Free-Form Text Boxes and Shapes**
   Currently, in `interpret.py`, only `SlidePlaceholder` types are successfully interpreted. PPTX allows users to put text inside auto-shapes and unstructured text boxes. Supporting base text extraction across all instances of `BaseShape` that have text frames would instantly map far more contents to the slides.
3. **Image & Media Extraction**
   Detect images, save the binary blob to an output `./media/` directory during conversion, and map an `Image` element into the Typst string, representing Typst's `#image("media/image1.png")` directive.

## 3. Recommended Code Changes & Improvements
- **File Naming Standards (PEP 8):** Modules under `typstpresenter\model\*` use capitalized PascalCase naming conventions (e.g. `Presentation.py`, `Element.py`). The Python community standard (PEP-8) strongly enforces `snake_case` for module names.
- **Architectural Cleanup - Extensibility:** `interpret.py` and `express.py` heavily rely on centralized `match / case` type checks. Instead of hard-coded statements, refactor this into mapping registries/strategies (e.g., `ShapeHandler` interface) so adding new features (like Tables, Media) avoids ballooning the file sizes.
- **Missing Test Suite:** Since this program maps heavily formatted, highly unstructured trees of objects together, adding a `tests/` directory with `pytest` is highly recommended. Small dummy PowerPoint sets can be used as fixtures to prevent regressions.
