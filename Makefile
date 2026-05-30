JEMDOC = python3 ../jemdoc
CONF = mysite.conf
PAGES = index research publications projects teaching cv

.PHONY: all clean

all:
	$(JEMDOC) -c $(CONF) $(addsuffix .jemdoc,$(PAGES))

clean:
	rm -f $(addsuffix .html,$(PAGES))
