PYTHON ?= python3

.PHONY: autoformat
autoformat: style lint

.PHONY: style
style:
	$(PYTHON) -m isort .
	$(PYTHON) -m unify --recursive --in-place --quote "'" src
	$(PYTHON) -m yapf --recursive --in-place src

.PHONY: lint
lint:
	$(PYTHON) -m pylint -j0 src
