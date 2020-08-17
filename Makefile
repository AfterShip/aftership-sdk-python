.PHONY: docs clean build

install:
	poetry install

test:
	poetry run py.test --cov=aftership

record:
	poetry run py.test --vcr-record=new_episodes

lint:
	poetry run flake8 aftership

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

build:
	poetry build

clean:
	-rm -r docs/_build
	-rm -r build dist aftership.egg-info
