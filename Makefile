.PHONY: test lint clean

test:
	pytest

lint:
	ruff check .

clean:
	rm -rf __pycache__ .pytest_cache
