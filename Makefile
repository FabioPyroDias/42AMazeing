PIP_INSTALL = amazeing/bin/pip install
PYTHON = amazeing/bin/python

RM = rm -rf

MYPY_FLAGS = -warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

install:
	python3 -m venv amazeing
	$(PIP_INSTALL) --upgrade pip
	$(PIP_INSTALL) flake8
	$(PIP_INSTALL) mypy

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	$(RM) src/__pycache__
	$(RM) src/algorithms/__pycache__
	$(RM) .mypy_cache

lint:
	$(PYTHON) -m flake8 a_maze_ing.py
	$(PYTHON) -m flake8 src
	$(PYTHON) -m mypy a_maze_ing.py $(MYPY_FLAGS)
	$(PYTHON) -m mypy src $(MYPY_FLAGS)

lint-strict:
	$(PYTHON) -m flake8 a_maze_ing.py
	$(PYTHON) -m flake8 src
	$(PYTHON) -m mypy --strict a_maze_ing.py
	$(PYTHON) -m mypy --strict src

build:
	$(PIP_INSTALL) build
	$(PYTHON) -m build --outdir .