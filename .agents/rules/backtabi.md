---
trigger: always_on
---

REGLAS ESTRICTAS DE ARQUITECTURA (Tabi Platform - Backend B2C TRS v1.0):

Stack Obligatorio: Todo el código debe escribirse en Python 3.11+ utilizando FastAPI (versión 0.110+). La base de datos es PostgreSQL 15+ usando SQLAlchemy 2.0 (modo asíncrono). Para la caché y tareas en segundo plano usar Redis 7+ y Celery.

Arquitectura: Debes usar una arquitectura de "Monolito Modular". El código se organizará estrictamente por dominios (auth, usuarios, restaurantes, reservas). Los dominios NUNCA deben comunicarse mediante "joins" directos en la base de datos, sino a través de interfaces de servicio y DTOs (Pydantic).

Estructura de Capas: El diseño debe mantener una separación limpia: Routers/Controllers -> Services (Reglas de negocio) -> Repositories (ORM/Base de datos) -> Models/Entities.

Bases de Datos: Prohibido usar objetos del modelo SQLAlchemy directamente en las respuestas de la API. Siempre transfórmalos a DTOs de Pydantic. Las consultas deben estar parametrizadas para evitar inyecciones SQL.

Reservas (Regla Crítica): La creación de reservas debe incluir bloqueos pesimistas en la base de datos (SELECT FOR UPDATE) para evitar condiciones de carrera (dobles reservas) en la misma franja horaria.

Endpoints: Las rutas deben seguir el estándar REST (/api/v1/...), usar paginación basada en cursores y devolver errores bajo el estándar RFC 7807 (Problem Details JSON).

Documentación: El código debe usar type hints estrictos (Mypy) y docstrings para OpenAPI.
