# TypstPresenter

Converts PowerPoint presentations (`*.pptx`) to Typst presentations (`*.typ`). The Typst library [diatypst](https://typst.app/universe/package/diatypst/) is used to typeset the slides, however, you can add your own _templates_ to this application if you want to support a different library.  

```bash
uv run typstpresenter convert presentation.pdf presentation.typ
```
