account:
	@python ggfilm/manage.py createsuperuser

init-migrate:
	@python ggfilm/manage.py makemigrations

migrate:
	@python ggfilm/manage.py migrate

static:
	@python ggfilm/manage.py collectstatic

reset:
	@python ggfilm/manage.py flush

dev:
	@python ggfilm/manage.py runserver 0.0.0.0:8000

release:
	@pip freeze > requirements.txt
