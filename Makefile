.PHONY: docs clean

install:
	pip install -r requirements.txt

test:
	py.test

flake8:
	flake8

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

clean:
	-rm -r docs/_build

record:
	py.test --vcr-record=new_episodes
