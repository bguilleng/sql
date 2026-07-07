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

## 2. Insertar datos de ejemplo

Ejecuta el script de datos:

```bash
mysql < mysql-data.sql
```

## 3. Eliminar las tablas (opcional)

```bash
mysql < drop-tables.sql
```

# Objetivo del repositorio

Este repositorio sirve como base práctica para:

- Aprender SQL desde cero con ejemplos reales.
- Comparar sintaxis entre distintos motores SQL.
- Probar consultas, joins, subconsultas, funciones y procedimientos.
- Realizar ejercicios del libro sin depender de un único motor de base de datos.


# Compatibilidad entre motores

Los scripts están diseñados para ser equivalentes funcionalmente, respetando las diferencias sintácticas de cada motor.

Esto permite:

- Ejecutar los mismos ejercicios en distintos motores.
- Comprender las variaciones entre SQL estándar y las extensiones de cada proveedor.
- Migrar estructuras entre plataformas.


# Autor

**Giovanny (bguilleng)**

Repositorio oficial de apoyo al libro de SQL.


# Contribuciones

Si deseas mejorar los scripts, agregar nuevos motores o reportar inconsistencias, puedes abrir un **Issue** o enviar un **Pull Request**.
