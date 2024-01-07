run:
	.venv/bin/flask --app longplay run --debug

freeze:
	python3 -m pip freeze > requirements.txt