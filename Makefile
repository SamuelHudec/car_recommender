install::
	pip install --upgrade pip wheel build
	pip install -e .[dev]

black::
	black .

flake::
	flake8 .

isort::
	isort .

lint::
	black isort flake

test-run::
	python -m test_src.whats_the_date