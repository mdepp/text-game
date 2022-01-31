.PHONY: style
style:
	isort .
	unify --recursive --in-place --quote "'" src
	yapf --recursive --in-place src
	pylint -j0 src
