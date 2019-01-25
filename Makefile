install:
	python3 setup.py install

clean:
	python setup.py clean
	rm -rf MANIFEST build dist markr.egg-info

build:
	python3 setup.py sdist bdist_wheel

upload: build
	python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

test:
	pytest tests
