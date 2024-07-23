.PHONY: black
black:
	black src tests
	python tests/badges/exe_black.py

.PHONY: down
down:
	docker-compose down --remove-orphans -v

.PHONY: lint
lint:
	python tests/badges/exe_lint.py
	pycodestyle src tests
	python tests/badges/exe_code_style.py

.PHONY: lint_local
lint_local:
	black src tests
	pylint --rcfile=tox.ini src
	pycodestyle src tests	

.PHONY: pip_runner
pip_runner:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-test.txt

.PHONY: safety
safety:
	safety check -r requirements.txt --ignore=70612 
	docker run --rm aserv-worker /bin/bash -c "pip install safety && safety check --ignore=70612"
	docker run --rm aserv-api /bin/bash -c "pip install safety && safety check --ignore=70612"
	bandit -r src
	python tests/badges/exe_safety.py
	python tests/badges/exe_index.py

.PHONY: safety_local
safety_local:
	safety check --ignore=70612
	bandit -r src

.PHONY: test
test:
	coverage run -m pytest --color=yes
	coverage html -d tests/codecoverage
	coverage-badge -o tests/codecoverage/coverage.svg

.PHONY: up
up:
	./build.sh