



clean:
	rm -rf /site

deps:
	pip install poetry==1.8.3
	poetry install -v --with docs

serve:
	mkdocs serve

build:
	mkdocs build

