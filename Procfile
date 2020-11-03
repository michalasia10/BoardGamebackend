web: daphne untitled1.asgi:application --port $PORT --bind 0.0.0.0
web2: gunicorn untitled1.wsgi --log-file -
worker: python manage.py runworker channel_layer -v2

