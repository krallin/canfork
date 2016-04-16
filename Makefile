lint:
	flake8 canfork tests

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source canfork setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install

clean: clean-tox clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-tox:
	rm -rf .tox/

.PHONY: clean-tox clean-pyc clean-build
