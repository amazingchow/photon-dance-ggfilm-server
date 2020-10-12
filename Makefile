account:
	@python ggfilm/manage.py createsuperuser --database=default

init-migrate:
	@python ggfilm/manage.py makemigrations

migrate:
	@python ggfilm/manage.py migrate wechat_ggfilm_backend --database=massive_dev_chart

db-reset:
	@python ggfilm/manage.py flush --database=massive_dev_chart

db-shell:
	@python ggfilm/manage.py dbshell --database=massive_dev_chart

static:
	@python ggfilm/manage.py collectstatic

dev:
	@python ggfilm/manage.py runserver 0.0.0.0:8000

clear:
	find . | grep -e __pycache__ -e  *.pyc -e *.pyo | xargs rm -rf

release:
	@pip freeze > requirements.txt
