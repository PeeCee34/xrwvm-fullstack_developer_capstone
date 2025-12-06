#!/bin/bash
set -e

# Navigate to app directory
cd /app

echo "Running Django setup tasks..."

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# If db.sqlite3 doesn’t exist, create it and optionally seed data
if [ ! -f "db.sqlite3" ]; then
  echo "No SQLite database found, creating one..."
  python manage.py migrate --noinput
  # Optionally create a superuser automatically (replace with your credentials)
  # python manage.py createsuperuser --noinput --username admin --email admin@example.com
fi

echo "Creating default superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "adminpass")
EOF

echo "Starting Gunicorn server..."
exec gunicorn --bind :8000 --workers 3 djangoproj.wsgi
