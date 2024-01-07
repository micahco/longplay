run:
	.venv/bin/flask --app mpd-web run --debug

freeze:
	pip freeze > requirements.txt