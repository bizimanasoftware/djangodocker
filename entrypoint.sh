#!/bin/sh

# This script waits for the database to be available before running Django commands.

# It checks if the database host and port are set.
if [ -z "$MYSQL_HOST" ] || [ -z "$MYSQL_PORT" ]; then
    echo "ERROR: MYSQL_HOST and MYSQL_PORT environment variables must be set."
    exit 1
fi

echo "Waiting for MySQL database at $MYSQL_HOST:$MYSQL_PORT..."

# Loop until netcat can connect to the database port.
while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  sleep 1
done

echo "MySQL database is ready!"

# Now, run database migrations.
echo "Applying database migrations..."
python manage.py makemigrations # If you have new models
python manage.py migrate --noinput

# Start the Django application using the Gunicorn WSGI server.
# The placeholder <your_project_name> is replaced with your actual project name.
exec gunicorn --bind 0.0.0.0:8000 --timeout 120 gloexproject.wsgi:application