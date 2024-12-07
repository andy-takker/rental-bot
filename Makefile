PROJECT_NAME = rental_bot
PYTHON_VERSION := 3.12
TEST_FOLDER_NAME = tests

develop: clean_dev ##@Develop Create virtualenv
	python$(PYTHON_VERSION) -m venv .venv
	.venv/bin/pip install -U pip poetry
	.venv/bin/poetry config virtualenvs.create false
	.venv/bin/poetry install

develop-ci: ##@Develop Create virtualenv for CI
	python -m pip install -U pip poetry
	poetry config virtualenvs.create false
	poetry install --no-root

test-ci: ##@Test Run tests with pytest and coverage in CI
	pytest ./$(TEST_FOLDER_NAME) --junitxml=./junit.xml --cov=./$(PROJECT_NAME) --cov-report=xml

lint-ci: ruff mypy ##@Linting Run all linters in CI

local:
	docker compose -f docker-compose.dev.yaml up --build --force-recreate --remove-orphans

local-down:
	docker compose -f docker-compose.dev.yaml down -v

migrate_latest:
	python ./endrex_portal_backend/infrastructure/database/__main__.py upgrade head

clean_dev: ##@Develop Remove virtualenv
	rm -rf .venv


ruff: ##@Linting Run ruff
	ruff check ./$(PROJECT_NAME)

mypy: ##@Linting Run mypy
	mypy --config-file ./pyproject.toml ./$(PROJECT_NAME)
