# Scripts del Libro de SQL

Colección de scripts SQL utilizados como material de apoyo para el libro de SQL.

Incluye ejemplos completos para **DB2, MySQL, Oracle, PostgreSQL, SQLite y SQL Server**, organizados por motor y listos para ejecutar.

# Estructura del repositorio

El repositorio contiene dos tipos de archivos por cada motor de base de datos:

- **`<motor>.sql`** → Script principal con la definición de tablas, índices, relaciones y objetos necesarios.
- **`<motor>-data.sql`** → Script con datos de ejemplo para poblar las tablas.
- **`drop-tables.sql`** → Script universal para eliminar las tablas creadas (cuando aplica).

## Motores incluidos

| Motor | Script de estructura | Script de datos |
|-------|----------------------|-----------------|
| DB2 | `DB2.sql` | `DB2-Data.sql` |
| MySQL | `mysql.sql` | `mysql-data.sql` |
| Oracle | `oracle.sql` | `oracle-data.sql` |
| PostgreSQL | `postgresql.sql` | `postgresql-data.sql` |
| SQLite | `sqlite.sql` | `sqlite-data.sql` |
| SQL Server | `sqlserver.sql` | `sqlserver-data.sql` |

# Cómo usar los scripts

## 1. Crear las tablas

Ejecuta el archivo correspondiente al motor que estés utilizando.

**Ejemplo en MySQL**

```bash
mysql < mysql.sql
```

**Ejemplo en SQLite**

SQLite no implementa `CREATE DATABASE`: la base de datos se crea al abrir el archivo con `sqlite3`.

```bash
sqlite3 sqlcourse.db < sqlite.sql
```

## 2. Insertar datos de ejemplo

Ejecuta el script de datos:

```bash
mysql < mysql-data.sql
```

Para SQLite, carga esquema y datos en la misma sesión para mantener activada la comprobación de claves foráneas:

```bash
cat sqlite.sql sqlite-data.sql | sqlite3 -bail sqlcourse.db
```

## 3. Eliminar las tablas (opcional)

```bash
mysql < drop-tables.sql
```

# Prueba reproducible de SQLite

Requiere el ejecutable `sqlite3`. La prueba crea una base temporal desde cero, carga los datos y falla si SQLite detecta una violación de clave foránea o si las relaciones principales no quedaron declaradas.

```bash
bash tests/test-sqlite.sh
```

# Objetivo del repositorio

Este repositorio sirve como base práctica para:

- Aprender SQL desde cero con ejemplos reales.
- Comparar sintaxis entre distintos motores SQL.
- Probar consultas, joins, subconsultas, funciones y procedimientos.
- Realizar ejercicios del libro sin depender de un único motor de base de datos.

# Compatibilidad entre motores

Los scripts están diseñados para ser equivalentes funcionalmente, respetando las diferencias sintácticas de cada motor.

La nulabilidad y las relaciones del esquema SQLite siguen el modelo común de MySQL, Db2 y PostgreSQL. Se conservan deliberadamente estas diferencias de representación en SQLite:

- no existe `CREATE DATABASE`; el archivo se crea con `sqlite3 sqlcourse.db`;
- las claves enteras autogeneradas usan `INTEGER PRIMARY KEY AUTOINCREMENT`;
- `hire_date` se almacena como `TEXT` en formato ISO `YYYY-MM-DD`, ya que SQLite no tiene un tipo DATE dedicado;
- los importes usan afinidad `NUMERIC` en lugar de un `DECIMAL(8,2)` rígido.

Esto permite ejecutar los mismos ejercicios en distintos motores y, al mismo tiempo, respetar el modelo de tipos propio de SQLite.

# Autor

**Giovanny (bguilleng)**

Repositorio oficial de apoyo al libro de SQL.

# Contribuciones

Si deseas mejorar los scripts, agregar nuevos motores o reportar inconsistencias, puedes abrir un **Issue** o enviar un **Pull Request**.
