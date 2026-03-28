install:
	python3 -m venv amazeing
	amazeing/bin/pip install --upgrade pip
	amazeing/bin/pip install flake8
	amazeing/bin/pip install mypy

run:
	amazeing/bin/python a_maze_ing.py config.txt

debug:
	amazeing/bin/python -m pdb a_maze_ing.py config.txt

clean:
	rm -rf src/__pycache__
	rm -rf src/algorithms/__pycache__
	rm -rf .mypy_cache

lint:
	amazeing/bin/python -m flake8 a_maze_ing.py
	amazeing/bin/python -m flake8 src
	amazeing/bin/python -m mypy a_maze_ing.py --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs
	amazeing/bin/python -m mypy src --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	amazeing/bin/python -m flake8 a_maze_ing.py
	amazeing/bin/python -m flake8 src
	amazeing/bin/python -m mypy --strict a_maze_ing.py
	amazeing/bin/python -m mypy --strict src