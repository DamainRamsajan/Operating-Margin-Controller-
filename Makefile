.PHONY: install test test-all demo vectors lint
install:
	pip install -e ".[dev]"
test:
	pytest -q
test-all:
	pytest -q -m "slow or not slow"
demo:
	python scripts/demo.py
vectors:
	python scripts/make_vectors.py
lint:
	ruff check src tests scripts
