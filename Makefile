test: clean
	pip install tox
	tox

clean:
	rm -rf src/__pycache__ src/osparc_filecomms.egg-info/
	rm -rf tests/functional/test_input_dir
	rm -rf tests/functional/test_output_dir
