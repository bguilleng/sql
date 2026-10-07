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

## SQLite: creación, carga y validación

Desde la raíz del repositorio, con el cliente `sqlite3` instalado y un archivo
`SQLCOURSE.db` nuevo (o sin las tablas del ejemplo):

```bash
sqlite3 -bail SQLCOURSE.db < sqlite.sql
sqlite3 -bail SQLCOURSE.db < sqlite-data.sql
sqlite3 -bail SQLCOURSE.db "PRAGMA foreign_keys = ON; PRAGMA foreign_key_check; PRAGMA integrity_check;"
```

SQLite crea el archivo al abrirlo; no admite `CREATE DATABASE`. Los scripts son
para una instalación inicial: volver a ejecutarlos sobre las mismas tablas/datos
produce errores, no actualiza una instalación existente. `-bail` detiene el cliente
ante el primer error. Cada script tiene su propia transacción; si falla la carga,
el esquema creado en el paso anterior permanece. Al usar una API, detener la
ejecución y hacer `ROLLBACK` ante cualquier excepción; no continuar hasta `COMMIT`.

Ambos scripts activan `PRAGMA foreign_keys = ON` antes de iniciar su transacción.
Esta opción es **por conexión**: toda conexión posterior de la aplicación debe
activarla también, fuera de una transacción. Ejecutar los scripts sin una
transacción externa ya abierta.

La comprobación debe devolver cero filas para `foreign_key_check` y `ok` para
`integrity_check`. Los datos incluyen 4 regiones, 26 países, 7 ubicaciones,
11 departamentos, 19 puestos, 40 empleados y 30 dependientes (137 filas).
Se insertan las entidades padre antes que las hijas, incluidos los responsables
antes que sus subordinados.

### Prueba reproducible sin dependencias externas

Requiere Python 3 con el módulo estándar `sqlite3`:

```bash
python -m unittest discover -s tests -v
```

Crea una base temporal, ejecuta los scripts en conexiones separadas y comprueba
recuentos, integridad, las siete claves foráneas, rechazo de referencias huérfanas,
columnas opcionales, salario obligatorio, cascadas e identidades tras la carga.
No modifica `SQLCOURSE.db` ni requiere un servidor de base de datos.
También se conserva la prueba de consola `bash tests/test-sqlite.sh`, que requiere
el ejecutable `sqlite3` y carga ambos scripts en una misma conexión.

# Objetivo del repositorio

Este repositorio sirve como base práctica para:

- Aprender SQL desde cero con ejemplos reales.
- Comparar sintaxis entre distintos motores SQL.
- Probar consultas, joins, subconsultas, funciones y procedimientos.
- Realizar ejercicios del libro sin depender de un único motor de base de datos.


# Compatibilidad entre motores

Los scripts están diseñados para ser equivalentes funcionalmente, respetando las diferencias sintácticas de cada motor.

### Diferencias deliberadas de SQLite

La equivalencia es la del modelo didáctico y sus consultas, no una identidad
completa de tipos o políticas referenciales entre motores.

| Aspecto | SQLite | Comparación / alcance |
|--------|--------|----------------------|
| Código de país | `TEXT` tanto en `countries` como en `locations` | MySQL y Db2 usan `CHAR(2)`; SQLite no impone longitud ni relleno fijo. |
| Nulabilidad | Nombres de región/país, ubicación del departamento, salarios mínimo/máximo y departamento del empleado admiten `NULL` | Coincide con MySQL y Db2. `employees.salary` sigue siendo obligatorio. |
| Importes | Se conserva la afinidad `NUMERIC` de la corrección existente | MySQL y Db2 declaran `DECIMAL(8,2)`. SQLite no garantiza aritmética decimal exacta ni escala de dos decimales; estos ejemplos no son un modelo contable. |
| Fechas y texto | Fecha de contratación como `TEXT` con datos ISO `YYYY-MM-DD`; textos sin límites de longitud | No reproduce la validación de `DATE` ni los tamaños de `VARCHAR` de otros motores. |
| Identidades | `INTEGER PRIMARY KEY AUTOINCREMENT`; acepta IDs explícitos y genera los siguientes | No reproduce todas las reglas de `GENERATED ALWAYS AS IDENTITY` de Db2. |
| Cascadas | Se conservan `ON DELETE CASCADE ON UPDATE CASCADE` en las siete relaciones | MySQL no declara cascadas para `employees.manager_id`; Db2 declara cascadas de borrado, pero no de actualización. En SQLite, borrar un responsable borra sus subordinados y dependientes de forma transitiva. |

No se añaden restricciones `CHECK` ni tablas `STRICT`: se conserva el tipado
flexible de SQLite. La prueba incluida valida SQLite; no certifica la ejecución
de los scripts de los otros motores.

Esto permite:

- Ejecutar los mismos ejercicios en distintos motores.
- Comprender las variaciones entre SQL estándar y las extensiones de cada proveedor.
- Migrar estructuras entre plataformas.


# Autor

**Giovanny (bguilleng)**

Repositorio oficial de apoyo al libro de SQL.


# Contribuciones

Si deseas mejorar los scripts, agregar nuevos motores o reportar inconsistencias, puedes abrir un **Issue** o enviar un **Pull Request**.
