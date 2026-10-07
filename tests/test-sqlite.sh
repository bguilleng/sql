#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB="$(mktemp "${TMPDIR:-/tmp}/sqlcourse-sqlite.XXXXXX.db")"
trap 'rm -f "$DB"' EXIT

command -v sqlite3 >/dev/null 2>&1 || {
  echo "ERROR: sqlite3 is required" >&2
  exit 127
}

cat "$ROOT_DIR/sqlite.sql" "$ROOT_DIR/sqlite-data.sql" | sqlite3 -bail "$DB"

fk_errors="$(sqlite3 "$DB" "PRAGMA foreign_key_check;")"
if [[ -n "$fk_errors" ]]; then
  echo "ERROR: foreign key violations detected:" >&2
  echo "$fk_errors" >&2
  exit 1
fi

sqlite3 -bail "$DB" <<'SQL'
SELECT CASE
  WHEN (SELECT upper(type) FROM pragma_table_info('locations') WHERE name='country_id') <> 'TEXT'
  THEN RAISE(ABORT, 'locations.country_id must be TEXT')
END;

SELECT CASE
  WHEN (SELECT "notnull" FROM pragma_table_info('departments') WHERE name='location_id') <> 0
  THEN RAISE(ABORT, 'departments.location_id must be nullable')
END;

SELECT CASE
  WHEN (SELECT "notnull" FROM pragma_table_info('jobs') WHERE name='min_salary') <> 0
    OR (SELECT "notnull" FROM pragma_table_info('jobs') WHERE name='max_salary') <> 0
  THEN RAISE(ABORT, 'job salary bounds must be nullable')
END;

SELECT CASE
  WHEN (SELECT "notnull" FROM pragma_table_info('employees') WHERE name='department_id') <> 0
  THEN RAISE(ABORT, 'employees.department_id must be nullable')
END;

SELECT CASE
  WHEN (SELECT COUNT(*) FROM regions) = 0
    OR (SELECT COUNT(*) FROM countries) = 0
    OR (SELECT COUNT(*) FROM locations) = 0
    OR (SELECT COUNT(*) FROM departments) = 0
    OR (SELECT COUNT(*) FROM jobs) = 0
    OR (SELECT COUNT(*) FROM employees) = 0
    OR (SELECT COUNT(*) FROM dependents) = 0
  THEN RAISE(ABORT, 'sample data was not loaded completely')
END;
SQL

echo "SQLite schema/data test passed; foreign_key_check returned no violations."
