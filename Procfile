web: gunicorn shoppharm.wsgi
release: python3 manage.py makemigrations --noinput
release: python3 manage.py collectstatic --noinput
release: python3 manage.py migrate --noinput
worker: celery -A shoppharm worker --loglevel=info -P eventlet