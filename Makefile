run:
	.venv/bin/gunicorn -w 4 'longplay:create_app()'

debug:
	.venv/bin/flask --app longplay run --debug

build:
	.venv/bin/python3 -m build --wheel