PYTHON ?= python3

.PHONY: render serve

render:
	$(PYTHON) scripts/render_site.py

serve: render
	$(PYTHON) -m http.server 8000 --bind 127.0.0.1
