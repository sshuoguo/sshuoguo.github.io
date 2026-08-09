JEMDOC ?= python3 -W ignore::SyntaxWarning ./jemdoc
CONF := mysite.conf
PAGES := index research notes cv
SOURCES := $(addsuffix .jemdoc,$(PAGES))
HTML := $(addsuffix .html,$(PAGES))

.PHONY: all serve clean

all: $(HTML)

%.html: %.jemdoc MENU $(CONF) jemdoc jemdoc.css
	$(JEMDOC) -c $(CONF) $<

serve: all
	python3 -m http.server 8000 --bind 127.0.0.1

clean:
	rm -f $(HTML)
