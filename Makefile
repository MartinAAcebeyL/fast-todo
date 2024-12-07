test:
	docker compose run --rm app pytest --cov=app --cov-report=html tests