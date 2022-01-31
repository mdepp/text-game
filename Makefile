.PHONY: format
format:
	isort .
	unify --recursive --in-place --quote "'" src
	yapf --recursive --in-place src
