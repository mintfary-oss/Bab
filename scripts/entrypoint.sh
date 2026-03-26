#!/bin/bash
set -e

echo "=== BabyBlog: Ожидание базы данных ==="

# Ожидание доступности PostgreSQL
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
" 2>/dev/null; do
    echo "БД недоступна, ожидание..."
    sleep 2
done

echo "=== BabyBlog: Применение миграций ==="
python manage.py migrate --noinput

echo "=== BabyBlog: Сбор статических файлов ==="
python manage.py collectstatic --noinput

echo "=== BabyBlog: Запуск ==="
exec "$@"
