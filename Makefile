# Makefile for common Python development tasks

# Define the directories/files to check/format.
# Adjust as needed for your project structure.
SOURCES = app tests

# Use SHELL for potentially more complex commands if needed later
SHELL := /bin/bash

.PHONY: all fix lint test format check-imports clean install-dev

# Default target: Run the linter
all: lint

# Install development dependencies (assuming flake8, black, isort, autoflake are listed here)
# Adjust requirements file name if needed.
install-dev:
	@echo "Checking/installing development dependencies..."
	pip install -r requirements.txt


fix:
	@echo "Running isort to sort imports..."
	isort $(SOURCES)
	@echo "Running autoflake to remove unused imports/variables..."
	autoflake --in-place --recursive --remove-all-unused-imports --remove-unused-variables $(SOURCES)
	@echo "Running black to format code..."
	black $(SOURCES)
	@echo "Running flake8 check after fixes..."
	$(MAKE) lint
	@echo "Fix and lint process complete."

# ASSUMES: Dependencies are installed and virtual environment is active.
lint:
	@echo "Running flake8 check..."
	flake8 $(SOURCES)
	@echo "Lint check complete."

# ASSUMES: Dependencies are installed and virtual environment is active.
test:
	@echo "Running pytest..."
	pytest tests/
	@echo "Test suite complete."