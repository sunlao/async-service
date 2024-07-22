# TODO - Add for pipeline
# .PHONY: lint
# lint:
# 	black src tests
# 	./ci_commit_changes.sh
# 	pylint --rcfile=tox.ini src
# 	pycodestyle src tests

PHONY: lint_local
lint_local:
	black src tests
	pylint --rcfile=tox.ini src
	pycodestyle src tests	

.PHONY: down
down:
	docker-compose down --remove-orphans -v

.PHONY: up
up:
	./build.sh

# TODO - Add for pipeline
# .PHONY: publish_images
# publish_images:
# 	./publish_images.sh

.PHONY: safety_local
safety_local:
	safety check --ignore=70612
	bandit -r src
