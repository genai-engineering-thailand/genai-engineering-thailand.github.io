



clean:
	rm -rf /site

poetry:
	pip install --upgrade pip
	pip install poetry==1.8.3

deps:
	poetry install -v --with docs

serve:
	poetry run mkdocs serve

build:
	poetry run mkdocs build

build-dry:
	poetry run mkdocs build --site-dir="temp"
	if [ -d "temp"]; then rm --recursive temp; fi