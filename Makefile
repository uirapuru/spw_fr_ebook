BOOK ?= $(notdir $(CURDIR))
BUILD ?= build
TITLE ?= Sylwetki uzbrojenia Federacji Rosyjskiej
AUTHOR ?= Grzegorz KASZUBA
DATE ?= $(shell date '+%-d %m %Y' | awk '{m["01"]="stycznia"; m["02"]="lutego"; m["03"]="marca"; m["04"]="kwietnia"; m["05"]="maja"; m["06"]="czerwca"; m["07"]="lipca"; m["08"]="sierpnia"; m["09"]="wrzesnia"; m["10"]="pazdziernika"; m["11"]="listopada"; m["12"]="grudnia"; print $$1, m[$$2], $$3}')
PDF := $(BUILD)/$(BOOK).pdf
EPUB := $(BUILD)/$(BOOK).epub
COVER_IMAGE ?= $(shell find images -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) | sort | head -n 1)
RESOURCE_PATH := .:$(shell find . -mindepth 2 -type f -name '*.md' -printf '%h\n' | sort -u | paste -sd: -)
LIST_SOURCES = sed -n 's/^.*(//; s/).*$$//; /\.md$$/p' spis_tresci.md | while read -r file; do case "$$file" in spis_tresci.md|index.md) continue ;; esac; [ -f "$$file" ] && printf '%s ' "$$file"; done
PANDOC_COMMON := \
	--standalone \
	--from=markdown \
	--toc \
	--toc-depth=1 \
	--top-level-division=section \
	--resource-path="$(RESOURCE_PATH)" \
	-M title="$(TITLE)" \
	-M author="$(AUTHOR)" \
	-M date="$(DATE)"

.PHONY: all ebook pdf epub watch clean

all: ebook

ebook: pdf

pdf:
	@SRC="$$( $(LIST_SOURCES) )"; \
	test -n "$$SRC" || { echo "Brak plikow markdown do zlozenia na podstawie spis_tresci.md"; exit 1; }; \
	mkdir -p $(BUILD); \
	pandoc $$SRC \
	$(PANDOC_COMMON) \
	--lua-filter=filters/toc-sections.lua \
	--lua-filter=filters/image-width.lua \
	--lua-filter=filters/table-width.lua \
	--pdf-engine=xelatex \
	--template=template.tex \
	--highlight-style=tango \
	$(if $(COVER_IMAGE),-M titlepage_image="$(COVER_IMAGE)") \
	-o $(PDF)

epub:
	@SRC="$$( $(LIST_SOURCES) )"; \
	test -n "$$SRC" || { echo "Brak plikow markdown do zlozenia na podstawie spis_tresci.md"; exit 1; }; \
	mkdir -p $(BUILD); \
	pandoc $$SRC \
	$(PANDOC_COMMON) \
	-o $(EPUB)

watch:
	find . \( -name '*.md' -o -name '*.tex' \) | entr make pdf

clean:
	rm -rf $(BUILD)