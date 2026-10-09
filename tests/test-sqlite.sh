#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB="$(mktemp "${TMPDIR:-/tmp}/sqlcourse-sqlite.XXXXXX.db")"
trap 'rm -f "$DB"' EXIT

command -v sqlite3 >/dev/null 2>&1 || {
  echo "ERROR: sqlite3 is required" >&2
  exit 127
}

fail() {
  echo "ERROR: $1" >&2
  exit 1
}

assert_eq() {
  local actual="$1"
  local expected="$2"
  local message="$3"
  [[ "$actual" == "$expected" ]] || fail "$message (expected '$expected', got '$actual')"
}

cat "$ROOT_DIR/sqlite.sql" "$ROOT_DIR/sqlite-data.sql" | sqlite3 -bail "$DB"

fk_errors="$(sqlite3 "$DB" "PRAGMA foreign_key_check;")"
[[ -z "$fk_errors" ]] || fail "foreign key violations detected: $fk_errors"

assert_eq "$(sqlite3 "$DB" "SELECT upper(type) FROM pragma_table_info('locations') WHERE name='country_id';")" "TEXT"   "locations.country_id must use TEXT affinity"
assert_eq "$(sqlite3 "$DB" "SELECT \"notnull\" FROM pragma_table_info('departments') WHERE name='location_id';")" "0"   "departments.location_id must be nullable"
assert_eq "$(sqlite3 "$DB" "SELECT \"notnull\" FROM pragma_table_info('jobs') WHERE name='min_salary';")" "0"   "jobs.min_salary must be nullable"
assert_eq "$(sqlite3 "$DB" "SELECT \"notnull\" FROM pragma_table_info('jobs') WHERE name='max_salary';")" "0"   "jobs.max_salary must be nullable"
assert_eq "$(sqlite3 "$DB" "SELECT \"notnull\" FROM pragma_table_info('employees') WHERE name='department_id';")" "0"   "employees.department_id must be nullable"

for table in regions countries locations departments jobs employees dependents; do
  rows="$(sqlite3 "$DB" "SELECT COUNT(*) FROM $table;")"
  [[ "$rows" -gt 0 ]] || fail "$table contains no sample rows"
done

echo "SQLite schema/data test passed; foreign_key_check returned no violations."
