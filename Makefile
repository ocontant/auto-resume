# Makefile for common Python development tasks

# Define the directories/files to check/format.
# Adjust as needed for your project structure.
SOURCES = app tests

# Use SHELL for potentially more complex commands if needed later
SHELL := /bin/bash

.PHONY: all fix lint test format check-imports clean install-dev check-venv

# Default target: Run the linter
all: lint

# Check if inside a virtual environment (recommended)
check-venv:
	@python -c 'import sys; sys.exit(0 if hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix) else 1)' || \
		(echo "ERROR: Not in a virtual environment. Please activate it first."; exit 1)

# Install development dependencies (assuming flake8, black, isort, autoflake are listed here)
# Adjust requirements file name if needed.
install-dev:
	@echo "Checking/installing development dependencies..."
	pip install -r requirements.txt # Or use requirements-dev.txt if you have one

# Target to run all formatters/fixers and then lint check
fix: check-venv install-dev
	@echo "Running isort to sort imports..."
	isort $(SOURCES)
	@echo "Running autoflake to remove unused imports/variables..."
	autoflake --in-place --recursive --remove-all-unused-imports --remove-unused-variables $(SOURCES)
	@echo "Running black to format code..."
	black $(SOURCES)
	@echo "Running flake8 check after fixes..."
	flake8 $(SOURCES)
	@echo "Fix and lint process complete."

# Target to only run the linter (check for issues)
lint: check-venv install-dev
	@echo "Running flake8 check..."
	flake8 $(SOURCES)
	@echo "Lint check complete."

# Target to run the test suite
test: check-venv
	@echo "Running pytest..."
	pytest tests/
	@echo "Test suite complete."
