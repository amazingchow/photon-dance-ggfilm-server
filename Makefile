dev:
	@python ggfilm/manage.py runserver

release:
	@pip freeze > requirements.txt
