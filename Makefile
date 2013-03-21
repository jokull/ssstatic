.DEFAULT_GOAL := develop

develop:
	python setup.py develop

clean:
	rm -rf *.egg-info dist

publish: clean
	python setup.py register sdist upload
