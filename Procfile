web: sh -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn speedgarage.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --log-level info"
