TYPST ?= typst
FONT_PATH ?= font

.PHONY: typst typst-final typst-watch

typst:
	$(TYPST) compile --root . --font-path $(FONT_PATH) main.typ main-typst.pdf

typst-final:
	$(TYPST) compile --root . --font-path $(FONT_PATH) --input format=final main.typ main-typst-final.pdf

typst-watch:
	$(TYPST) watch --root . --font-path $(FONT_PATH) main.typ main-typst.pdf
