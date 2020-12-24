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

logrotate-test:
	@touch ggfilm/log/log-file.log
	@head -c 10M < /dev/urandom > ggfilm/log/log-file.log
	@touch ggfilm/wechat_ggfilm_backend/utils/log/log-file.log
	@head -c 10M < /dev/urandom > ggfilm/wechat_ggfilm_backend/utils/log/log-file.log
	logrotate -vf ./deploy/logrotate/ggfilm

clear:
	find . | grep -e __pycache__ -e  *.pyc -e *.pyo | xargs rm -rf

release:
	@pip freeze > requirements.txt

env:
	sudo cp ./deploy/cron/ggfilm /etc/cron.daily/
	sudo chmod 755 /etc/cron.daily/ggfilm
	sudo cp ./deploy/logrotate/ggfilm /etc/logrotate.d/
	sudo cp ./deploy/nginx/ggfilm-http-server.conf /etc/nginx/conf.d/
	sudo mkdir -p /var/log/django/ggfilm
