#!/bin/sh

echo "Waiting for PostgreSQL..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT"; do
  sleep 1
done

echo "Database available - making migrations..."

python manage.py makemigrations RestHits
python manage.py migrate

echo "Starting up Django application..."

gunicorn RestHits.wsgi:application --bind 0.0.0.0:8000
