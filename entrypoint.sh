#!/bin/sh
set -e

echo "Waiting for database at $DB_HOST:$DB_PORT..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
  sleep 1
done
echo "Database is up."

# Restore the Aiven backup on first boot only (skip if the DB already has tables,
# so restarts/rebuilds don't try to re-restore).
TABLE_COUNT=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tAc \
  "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';")

if [ "$TABLE_COUNT" -eq "0" ] && [ -f /app/dbdump/backup.dump ]; then
  echo "Empty database detected — restoring /app/dbdump/backup.dump ..."
  PGPASSWORD="$DB_PASSWORD" pg_restore --no-owner --no-privileges --clean --if-exists \
    -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" /app/dbdump/backup.dump || \
    echo "pg_restore reported errors — check output above (some are harmless, e.g. missing extensions)."
else
  echo "Skipping restore (tables already exist, or no dump file mounted)."
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

exec "$@"
