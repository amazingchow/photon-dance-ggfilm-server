account:
	@python ggfilm/manage.py createsuperuser

init-migrate:
	@python ggfilm/manage.py makemigrations

migrate:
	@python ggfilm/manage.py migrate

dev:
	@python ggfilm/manage.py runserver 0.0.0.0:8000

release:
	@pip freeze > requirements.txt
