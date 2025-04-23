.PHONY: all test unittest typecheck checkformatting tidy clean

# Default target
all: test

# Virtual environment setup
.venv:
	uv sync
	touch .venv

# Run unit tests
unittest: .venv
	.venv/bin/pytest

# Run type checking
typecheck: .venv
	.venv/bin/pyright

# Check code formatting
checkformatting: .venv
	.venv/bin/ruff check .

# Format code
tidy: .venv
	.venv/bin/ruff format .
	.venv/bin/ruff check --fix .

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