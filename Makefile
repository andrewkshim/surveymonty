venv:
	@which virtualenv || echo "Please install virtualenv https://virtualenv.pypa.io/en/stable"
	@virtualenv venv

dependencies: venv
	@source venv/bin/activate; \
	pip install -r requirements.txt

integration-tests:
	@nose2 tests.integration

unit-tests:
	@nose2 tests.unit

deploy:
	@python setup.py sdist upload
	@python setup.py bdist_wheel upload
