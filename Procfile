web: daphne untitled1.asgi:application --port $PORT --bind 0.0.0.0 -v2
web2: gunicorn untitled1.wsgi --log-file -
worker: python manage.py runworker channels -v2
