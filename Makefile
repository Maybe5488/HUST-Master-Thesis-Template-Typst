TYPST ?= typst

.PHONY: all watch

all:
	$(TYPST) compile --root . --font-path fonts main.typ thesis.pdf

watch:
	$(TYPST) watch --root . --font-path fonts main.typ thesis.pdf
