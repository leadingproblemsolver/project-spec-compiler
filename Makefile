.PHONY: test validate report build

test:
	python -m pytest -q

validate:
	python -m project_spec.cli validate specifications

report:
	python -m project_spec.cli report specifications --output var/portfolio-report.md

build:
	python -m pip wheel . --no-deps -w dist
