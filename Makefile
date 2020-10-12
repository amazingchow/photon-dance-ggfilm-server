account:
	@python ggfilm/manage.py createsuperuser

init-migrate:
	@python ggfilm/manage.py makemigrations

migrate:
	@python ggfilm/manage.py migrate

reset:
	@python ggfilm/manage.py flush

db:
	@python ggfilm/manage.py dbshell

static:
	@python ggfilm/manage.py collectstatic

dev:
	@python ggfilm/manage.py runserver 0.0.0.0:8000

release:
	@pip freeze > requirements.txt
