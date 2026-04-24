# Habi Backend — Prueba Técnica

API REST de consulta de inmuebles y diseño del servicio de "me gusta", desarrollada como prueba técnica para Habi.

## Tecnologías

| Tecnología | Versión | Por qué |
|---|---|---|
| Python | 3.11+ | Versión estable con mejoras de rendimiento y tipado |
| MySQL | 8.0 | Motor relacional provisto por Habi |
| `http.server` | stdlib | Requisito explícito — sin frameworks externos |
| `unittest` | stdlib | Suite de testing integrada, sin dependencias extra |
| `mysql-connector-python` | latest | Driver oficial de Oracle, sin ORM para control total del SQL |
| `python-dotenv` | latest | Carga de variables de entorno desde `.env` |

## Estructura del proyecto

```
habi-backend/
├── db/
│   └── connection.py          # Pool de conexiones MySQL reutilizable
├── service_properties/
│   ├── server.py              # Entry point HTTP
│   ├── handlers.py            # Routing y manejo de requests/responses
│   ├── service.py             # Lógica de negocio
│   ├── repository.py          # Acceso a base de datos
│   ├── filters.py             # Parseo y validación de filtros
│   └── tests/
│       ├── test_service.py
│       ├── test_repository.py
│       └── test_filters.py
├── service_likes/
│   ├── er_diagram.png         # Diagrama Entidad-Relación
│   └── schema_extension.sql   # SQL de extensión del modelo
├── examples/
│   └── filters_input.json     # JSON de ejemplo para el Servicio 1
├── .env.example               # Variables de entorno requeridas (sin valores)
└── README.md
```

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd habi-backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install mysql-connector-python python-dotenv

# Configurar variables de entorno
cp .env.example .env
# Editar .env con las credenciales provistas por Habi
```

## Ejecución

```bash
# Iniciar el servidor (Servicio 1 — Consulta de inmuebles)
python -m service_properties.server
# El servidor escucha en http://localhost:8080
```

### Ejemplo de uso

```bash
curl -X POST http://localhost:8080/properties \
  -H "Content-Type: application/json" \
  -d '{"city": "bogota", "status": "en_venta"}'
```

Ver más ejemplos en `examples/filters_input.json`.

## Tests

```bash
# Correr todos los tests
python -m unittest discover -s service_properties/tests -v

# Correr un módulo específico
python -m unittest service_properties.tests.test_filters -v
```

## Decisiones de diseño

### Servicio 1 — Consulta de inmuebles

- **Estado actual mediante subquery:** el estado activo de un inmueble es el último registro en `status_history`. Se usa un subquery con `MAX(id)` en lugar de `ORDER BY + LIMIT` para mantener la lógica en una sola query sin cursores.
- **Filtros dinámicos con parámetros:** los filtros se construyen dinámicamente agregando cláusulas `WHERE` con marcadores `%s`, nunca concatenación de strings. Esto elimina el riesgo de SQL injection.
- **Separación de capas:** `filters.py` valida y parsea la entrada, `repository.py` habla con la DB, `service.py` aplica reglas de negocio, `handlers.py` maneja HTTP. Cada capa tiene una sola responsabilidad.

### Servicio 2 — Me gusta

El modelo extiende el esquema existente con dos tablas nuevas:

- **`user`:** usuarios registrados con email único. Se eligió tabla separada para no modificar el modelo de inmuebles y para escalar el perfil de usuario independientemente.
- **`like`:** relación N:M entre `user` y `property` con timestamp. El índice único compuesto `(user_id, property_id)` garantiza la restricción de un like por usuario por inmueble a nivel de DB, no solo a nivel de aplicación.
- **Índice en `property_id`:** permite calcular el ranking de popularidad (`GROUP BY property_id ORDER BY COUNT(*)`) sin full table scan.

**Consultas derivadas:**
- Histórico de likes de un usuario: `SELECT * FROM like WHERE user_id = ? ORDER BY created_at DESC`
- Ranking de popularidad: `SELECT property_id, COUNT(*) as likes FROM like GROUP BY property_id ORDER BY likes DESC`

## Limitaciones conocidas

- `http.server` es single-thread: cada request bloquea al siguiente. Para producción se usaría `ThreadingHTTPServer` o un servidor WSGI (gunicorn/uvicorn).
- Sin autenticación: el Servicio 1 es público. El Servicio 2 requeriría un mecanismo de auth (JWT, sesión) no implementado en esta prueba.

## Dudas encontradas y resoluciones

| Duda | Resolución |
|---|---|
| ¿Cómo determinar el estado actual si hay múltiples registros en `status_history`? | Estado activo = registro con `MAX(id)` o `MAX(update_date)` para ese inmueble |
| ¿Los filtros son AND u OR entre sí? | AND — se aplican todos los filtros simultáneamente |
| ¿Qué pasa si un inmueble no tiene `status_history`? | Se excluye del resultado (INNER JOIN implica que debe existir al menos un registro) |
