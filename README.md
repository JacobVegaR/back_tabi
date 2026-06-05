# Tabi Platform - Backend B2C TRS v1.0

Este repositorio contiene la base del backend para la plataforma Tabi, estructurado siguiendo reglas estrictas de desarrollo y arquitectura.

---

## 🛠️ Stack Tecnológico

- **Lenguaje**: Python 3.11+ (Recomendado 3.13+)
- **Framework Web**: FastAPI (v0.110+)
- **Base de Datos**: PostgreSQL 15+ (con SQLAlchemy 2.0 en modo asíncrono y `asyncpg`)
- **Caché y Tareas**: Redis 7+ y Celery
- **Validación de Tipos**: Mypy (modo estricto)

---

## 📐 Reglas de Arquitectura

1. **Monolito Modular**: El código está organizado estrictamente por dominios (`auth`, `usuarios`, `restaurantes`, `reservas`).
2. **Sin Acoplamiento de Base de Datos**: Los dominios **NUNCA** se comunican entre sí mediante "joins" en base de datos. Toda la comunicación se hace a través de las interfaces de servicio (`Service`) usando DTOs (`Pydantic`).
3. **Estructura de Capas**:
   - `Router/Controller` -> Expone los endpoints REST.
   - `Service` -> Contiene las reglas de negocio.
   - `Repository` -> Ejecuta consultas a la base de datos (con consultas parametrizadas contra inyecciones SQL).
   - `Models` -> Definición de tablas/entidades SQLAlchemy.
4. **Respuestas de API**: Prohibido devolver modelos SQLAlchemy directamente. Siempre se mapean a esquemas Pydantic (`schemas.py`).
5. **Bloqueo Pesimista (SELECT FOR UPDATE)**: La creación de reservas utiliza `with_for_update()` en las consultas para evitar condiciones de carrera (doble reserva) en el mismo horario.
6. **Errores Estándar**: Las excepciones se devuelven en formato **RFC 7807 (Problem Details JSON)**.
7. **Documentación**: El código implementa Type Hints estrictos y docstrings en los endpoints para la generación automática de OpenAPI.

---

## 📁 Estructura del Proyecto

```text
src/
├── app/
│   ├── config.py       # Configuración con Pydantic Settings
│   ├── database.py     # Motor SQLAlchemy y sesión asíncrona
│   ├── errors.py       # Controladores de error RFC 7807
│   ├── schemas.py      # Esquemas genéricos (Ej. Paginación Cursor)
│   └── main.py         # Punto de entrada de FastAPI
└── domains/
    ├── auth/           # Registro e inicio de sesión
    ├── usuarios/       # Gestión de perfiles de usuario
    ├── restaurantes/   # Gestión de información de restaurantes
    └── reservas/       # Reservas y slots con Pessimistic Lock
```

---

## 🚀 Guía de Instalación y Uso

### 1. Clonar el repositorio y configurar el entorno virtual

```bash
# Crear entorno virtual
py -m venv venv

# Activar el entorno virtual (Windows Powershell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Copia el archivo `.env.example` y renómbralo a `.env`:

```bash
copy .env.example .env
```

Ajusta las URLs de conexión según tu entorno local.

### 3. Ejecutar Verificación de Tipos (Mypy)

Antes de realizar commits, asegúrate de que el código no tiene errores de tipado:

```bash
mypy src
```

### 4. Iniciar el Servidor de Desarrollo

```bash
uvicorn src.app.main:app --reload
```

Una vez levantado el servidor, puedes acceder a la documentación interactiva en:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
