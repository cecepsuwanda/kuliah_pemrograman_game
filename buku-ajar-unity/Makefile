# Build full book and per-chapter PDFs

LATEXMK=latexmk
LATEXMK_FLAGS=-pdf -interaction=nonstopmode -file-line-error -halt-on-error

all: book

book:
	$(LATEXMK) $(LATEXMK_FLAGS) main.tex

clean:
	$(LATEXMK) -C

chapters := $(patsubst chapters/%.tex,%.pdf,$(wildcard chapters/*.tex))

# Build a single chapter PDF using subfiles
chapters: $(chapters)

%.pdf: chapters/%.tex
	$(LATEXMK) $(LATEXMK_FLAGS) -jobname=$* chapters/$*.tex

.PHONY: all book clean chapters
