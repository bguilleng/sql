"""Run with: python -m unittest discover -s tests -v (standard library only)."""
from pathlib import Path
import sqlite3
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
COUNTS = dict(regions=4, countries=26, locations=7, departments=11,
              jobs=19, employees=40, dependents=30)


class SQLiteScriptsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'SQLCOURSE.db'
        # Separate connections reproduce the documented two CLI invocations.
        with sqlite3.connect(self.path) as schema:
            schema.executescript((ROOT / 'sqlite.sql').read_text(encoding='utf-8'))
            self.assertEqual(schema.execute('PRAGMA foreign_keys').fetchone(), (1,))
            self.assertFalse(schema.in_transaction)
        schema.close()
        self.db = sqlite3.connect(self.path)
        self.addCleanup(self.db.close)
        self.db.executescript((ROOT / 'sqlite-data.sql').read_text(encoding='utf-8'))
        self.assertEqual(self.db.execute('PRAGMA foreign_keys').fetchone(), (1,))
        self.assertFalse(self.db.in_transaction)

    def test_load_and_integrity(self):
        for table, expected in COUNTS.items():
            with self.subTest(table=table):
                self.assertEqual(self.db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0], expected)
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(), [])
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchall(), [('ok',)])
        for table in ('countries', 'locations'):
            info = {row[1]: row[2] for row in self.db.execute(f'PRAGMA table_info({table})')}
            self.assertEqual(info['country_id'], 'TEXT')
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM locations l JOIN countries c USING(country_id)').fetchone(), (7,))

    def test_nullable_columns_and_required_salary(self):
        for table, column in [('regions', 'region_name'), ('countries', 'country_name'),
                              ('departments', 'location_id'), ('jobs', 'min_salary'),
                              ('jobs', 'max_salary'), ('employees', 'department_id')]:
            with self.subTest(table=table, column=column):
                self.db.execute(f'UPDATE {table} SET {column} = NULL')
                self.db.rollback()
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'NOT NULL'):
            self.db.execute('UPDATE employees SET salary = NULL WHERE employee_id = 100')
        self.db.rollback()

    def test_every_foreign_key_rejects_orphans(self):
        relationships = [('countries', 'region_id'), ('locations', 'country_id'),
                         ('departments', 'location_id'), ('employees', 'job_id'),
                         ('employees', 'department_id'), ('employees', 'manager_id'),
                         ('dependents', 'employee_id')]
        actual = {(table, fk[3]) for table in COUNTS
                  for fk in self.db.execute(f'PRAGMA foreign_key_list({table})')}
        self.assertEqual(actual, set(relationships))
        for table, column in relationships:
            with self.subTest(table=table, column=column):
                with self.assertRaisesRegex(sqlite3.IntegrityError, 'FOREIGN KEY'):
                    self.db.execute(f'UPDATE {table} SET {column} = ?', ('ZZ' if column == 'country_id' else -999,))
                self.db.rollback()

    def test_update_and_delete_cascades(self):
        self.db.execute("UPDATE countries SET country_id = 'UX' WHERE country_id = 'US'")
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM locations WHERE country_id = 'UX'").fetchone(), (3,))
        self.db.execute('UPDATE employees SET employee_id = 999 WHERE employee_id = 100')
        self.assertGreater(self.db.execute('SELECT COUNT(*) FROM employees WHERE manager_id = 999').fetchone()[0], 0)
        self.assertEqual(self.db.execute('SELECT employee_id FROM dependents WHERE dependent_id = 4').fetchone(), (999,))
        self.db.execute('DELETE FROM employees WHERE employee_id = 999')
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM employees').fetchone(), (0,))
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM dependents').fetchone(), (0,))
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_generated_identity_after_explicit_seed(self):
        cursor = self.db.execute("INSERT INTO regions(region_name) VALUES ('Test')")
        self.assertEqual(cursor.lastrowid, 5)
        self.db.execute('DELETE FROM regions WHERE region_id = 5')
        cursor = self.db.execute("INSERT INTO regions(region_name) VALUES ('Next')")
        self.assertEqual(cursor.lastrowid, 6)


if __name__ == '__main__':
    unittest.main()
