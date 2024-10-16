format:
	@python -m black . --exclude venv --exclude .git --exclude .vscode --exclude __pycache__ --exclude .pytest_cache --exclude .mypy_cache --exclude .ipynb_checkpoints --exclude ragu-sync 

install:
	@pip install -r requirements.txt

test:
	@python -m pytest tests