#!/bin/bash
set -euo pipefail
BACKUP_DIR="${1:-/var/backups/babyblog}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "${BACKUP_DIR}"
docker exec babyblog_db pg_dump -U "${POSTGRES_USER:-babyblog}" "${POSTGRES_DB:-babyblog}" | gzip > "${BACKUP_DIR}/db_${TIMESTAMP}.sql.gz"
tar -czf "${BACKUP_DIR}/media_${TIMESTAMP}.tar.gz" -C "$(dirname "$0")/../" uploads/
find "${BACKUP_DIR}" -name "*.gz" -mtime +30 -delete
echo "Готово: ${BACKUP_DIR}"
