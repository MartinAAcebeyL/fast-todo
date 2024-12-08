test:
	docker compose run --rm app pytest --cov=app --cov-report=html tests

lint:
	docker compose run --rm app flake8 app tests

format:
	docker compose run --rm app black app tests

autofix:
	docker compose run --rm app autopep8 --in-place --recursive app tests

check: lint format test autofix
