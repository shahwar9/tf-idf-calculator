SHELL=/bin/bash

black:
	black --config=myproject.toml common/ handlers/

black-check:
	black --check --config=myproject.toml common/ handlers/

flake8-check:
	flake8 common/ handlers/
