#!/bin/bash
set -e
echo "=== Ожидание БД ==="
while ! python -c "import psycopg2,os;psycopg2.connect(dbname=os.environ.get('POSTGRES_DB','babyblog'),user=os.environ.get('POSTGRES_USER','babyblog'),password=os.environ.get('POSTGRES_PASSWORD','babyblog_secret'),host=os.environ.get('POSTGRES_HOST','db'),port=os.environ.get('POSTGRES_PORT','5432')).close()" 2>/dev/null; do sleep 2; done
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
