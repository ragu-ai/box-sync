.PHONY: format install test setup local-setup teardown clean

format:
	python -m black . --exclude "venv/|.git/|.vscode/|__pycache__/|.pytest_cache/|.mypy_cache/|.ipynb_checkpoints/|ragu-sync/"

install:
	pip install -r requirements.txt

test:
	python -m pytest tests

setup: teardown
	docker-compose up -d

local-setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

teardown:
	docker-compose down

clean: teardown
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +