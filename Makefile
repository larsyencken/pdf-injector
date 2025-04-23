.PHONY: all test unittest typecheck checkformatting tidy clean

# Default target
all: test

# Virtual environment setup
.venv:
	uv sync -e dev
	touch .venv

# Run unit tests
unittest: .venv
	uv run pytest

# Run type checking
typecheck: .venv
	uv run pyright

# Check code formatting
checkformatting: .venv
	uv run ruff check .

# Format code
tidy: .venv
	uv run ruff format .
	uv run ruff check --fix .

# Run all tests
test: unittest typecheck checkformatting

# Clean up
clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .pyright
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete