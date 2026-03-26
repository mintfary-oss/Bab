#!/bin/bash
set -e

echo "=== BabyBlog: Waiting for database ==="

until python -c "
import psycopg2
import os
conn = psycopg2.connect(
    dbname=os.environ.get('POSTGRES_DB', 'babyblog'),
    user=os.environ.get('POSTGRES_USER', 'babyblog'),
    password=os.environ.get('POSTGRES_PASSWORD', 'babyblog_secret'),
    host=os.environ.get('POSTGRES_HOST', 'db'),
    port=os.environ.get('POSTGRES_PORT', '5432'),
)
conn.close()
print('Database is ready')
" 2>/dev/null; do
    echo "Database unavailable, retrying in 2s..."
    sleep 2
done

echo "=== BabyBlog: Running migrations ==="
python manage.py migrate --noinput

echo "=== BabyBlog: Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== BabyBlog: Starting server ==="
exec "$@"
