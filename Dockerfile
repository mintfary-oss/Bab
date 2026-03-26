FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg libmagic1 libpq-dev gcc gettext && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
RUN mkdir -p /app/uploads/images /app/uploads/videos /app/uploads/documents /app/uploads/thumbnails /app/staticfiles
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "babyblog.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
