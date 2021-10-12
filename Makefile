SHELL=/bin/bash

black:
	black --config=myproject.toml common/ handlers/

black-check:
	black --check --config=myproject.toml common/ handlers/

flake8-check:
	flake8 --config=setup.cfg common/ handlers/

integration-test:
	python integration_test.py