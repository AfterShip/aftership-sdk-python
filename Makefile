.PHONY: docs clean build

install:
	pip install --upgrade .
	pip install -r requirements-dev.txt

test:
	cd tests && py.test

record:
	cd tests && py.test --vcr-record=new_episodes

flake8:
	flake8

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

build:
	python setup.py sdist --formats=gztar
	python setup.py sdist bdist_wheel

clean:
	-rm -r docs/_build
	-rm -r build dist aftership.egg-info
