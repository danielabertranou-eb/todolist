release: python manage.py migrate
web: gunicorn todolist.wsgi --log-file - --settings=settings.dev
