JEMDOC ?= jemdoc
CONF = mysite.conf
PAGES = index research reading cv

.PHONY: all clean

all:
	$(JEMDOC) -c $(CONF) $(addsuffix .jemdoc,$(PAGES))

clean:
	rm -f $(addsuffix .html,$(PAGES))
