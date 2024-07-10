



clean:
	rm -rf /site

poetry:
	pip install --upgrade pip
	pip install poetry==1.8.3

deps:
	poetry install -v --with docs

serve:
	poetry mkdocs serve

build:
	poetry mkdocs build

build-dry:
	poetry mkdocs build --site-dir="temp"
	if [ -d "temp"]; then rm --recursive temp; fi