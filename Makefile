test: clean
	pip install -e .[test]
	mkdir tests/test_output_dir
	pytest -vv

clean:
	rm -rf src/__pycache__ src/osparc_filecomms.egg-info/
	rm -rf tests/test_output_dir
