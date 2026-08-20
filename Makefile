.PHONY: install test lint run-example clean

install:
	uv sync

test:
	uv run pytest

lint:
	uv run python -m compileall src tests examples

run-example:
	uv run python examples/basic_login.py

clean:
	rm -rf .pytest_cache .venv dist build src/*.egg-info
