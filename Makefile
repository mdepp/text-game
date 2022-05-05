.PHONY: autoformat
autoformat: style lint

.PHONY: style
style:
	isort .
	unify --recursive --in-place --quote "'" src
	yapf --recursive --in-place src

.PHONY: lint
lint:
	pylint -j0 src
