dev:
	@python ggfilm/manage.py runserver 0:8000

release:
	@pip freeze > requirements.txt
