.DEFAULT: all
.PHONY: all develop test coverage codecov

all:
	echo "nothing here, use one of the following targets:"
	echo "develop, test, coverage, codecov, clean"

develop:
	pip install -r requirements.txt
	python setup.py develop

test: develop
	pip install -r test-requirements.txt
	flake8 --exclude=src .
	pytest --ignore=src

coverage: develop
	pip install -r test-requirements.txt
	pytest --ignore=src --cov-report html --cov=opinionated_configparser tests --cov-report term

clean:
	rm -Rf *.egg-info htmlcov coverage.xml .coverage __pycache__ .pytest_cache opinionated_configparser/__pycache__ tests/__pycache__

codecov: coverage
	if test "$${CODECOV_TOKEN:-}" != ""; then codecov --token=$${CODECOV_TOKEN}; fi
