



clean:
	rm -rf /site

poetry:
	pip install --upgrade pip
	pip install poetry==1.8.3

deps:
	poetry install -v --with docs

serve:
	mkdocs serve

build:
	mkdocs build

build-dry:
	mkdocs build --site-dir="temp"
	if [ -d "temp"]; then rm --recursive temp; fi