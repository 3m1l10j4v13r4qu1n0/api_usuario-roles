# Reglas de buenas prácticas para generar código Python (API, FastAPI, Clean Architecture)

## Principios generales
- Cada módulo/función/clase debe tener **una única responsabilidad** bien definida. Si mezcla persistencia, dominio, transporte y lógica de negocio sin necesidad, separalo.
- Antes de escribir código, pensá en el **contrato**: qué recibe (parámetros/tipos), qué devuelve (tipo de retorno), y qué efectos secundarios tiene (persistencia, llamadas externas, excepciones que lanza).
- Preferí **composición sobre herencia**: decoradores, mixins chicos y colaboración de objetos, no jerarquías profundas de clases.
- Separá **dominio (pureza), aplicación (casos de uso), infraestructura (adapters) y presentación (routers/schemas)**. El dominio NO importa frameworks (FastAPI, SQLAlchemy, Pydantic, requests).
- Toda dependencia externa (BD, HTTP, hashing de contraseñas, emisión/validación de tokens JWT, fecha/hora, random, librerías de terceros) debe inyectarse o encapsularse detrás de un port propio, nunca usarse directa y dispersa por la lógica de negocio.
- No aplicar estos principios a rajatabla en todos lados: ver sección "Cuándo NO aplicar esto a rajatabla" al final.

## Estructura y organización (equivalente a SRP)
- Un archivo = una responsabilidad. No mezclar mapeo de columnas, transformación de datos y validación en la misma función.
- Respetar las capas del proyecto: `app/domain/` (entidades puras + ports), `app/application/use_cases/` (`ucN_*`), `app/infrastructure/` (ORM/repositorios en `database/`, auth en `auth/`, DI en `dependencies/`), `app/presentation/` (routers, schemas, handlers).
- Los casos de uso reciben **ports** (contratos `ABC` + `abstractmethod`), no implementaciones concretas; orquestan el flujo y no contienen SQL ni lógica de transporte.
- El punto de entrada (`app/main.py`, `app/main:app`) y el wiring (`dependency_injection.py`) deben inicializar y orquestar, no contener lógica de negocio.
- Funciones puras (normalización, validación, transformación) sin estado ni I/O; estado y efectos secundarios confinados en los adapters.

## Abierto a extensión, cerrado a modificación
- Preferir agregar comportamiento nuevo vía **nuevos casos de uso, nuevas estrategias de validación o parámetros**, en vez de modificar un caso de uso estable agregándole condicionales (`if tipo == 'x'`) que crecen sin límite.
- Usar polimorfismo/estrategia (varias clases con un port común) antes que cadenas de `if/elif` sobre un enum o string.
- Extender la validación con funciones/estrategias nuevas en vez de tocar las existentes que ya pasan tests.
- En el mapeo de permisos/roles o validaciones de contraseña, agregar nuevas estrategias como datos/funciones nuevas, no reescribiendo las existentes.

## Sustitución de contratos (equivalente a LSP)
- Una clase que implementa un port debe comportarse de forma consistente con lo que el consumidor espera: mismos tipos de retorno, mismas excepciones, mismos casos de borde (ej. un repositorio fake en tests y el real con SQLAlchemy deben tener la misma semántica).
- No cambiar la semántica de un método heredado/port: no devolver `None` donde se espera un objeto, no lanzar una excepción distinta a la del contrato (usar las excepciones de dominio de `exceptions.py`).
- Respetar las firmas declaradas (ABC/Protocol): los tests unitarios con `FakeRepository` deben comportarse igual que la implementación real, salvo el efecto de persistencia.

## Interfaces pequeñas (equivalente a ISP)
- Preferir **ports y métodos pequeños y específicos** antes que un port con 15 métodos que la mayoría de los adapters deja `raise NotImplementedError`.
- Si un port expone métodos que la mayoría de sus implementaciones no usa, dividirlo en varios más chicos y específicos.
- Las entidades (dataclasses) deben exponer solo los campos que necesitan, sin "campos de más" para ahorrar creación de clases.
- En schemas Pydantic, preferir schemas chicos (base/update/response) antes que un schema gigante con todo opcional.

## Inversión de dependencias
- La lógica de negocio y los casos de uso no deben depender de detalles de implementación (SQL con SQLAlchemy, gspread, asyncpg) sino de abstracciones propias (ports con firma clara).
- Encapsular la BD (`app/infrastructure/database/`), el hashing de contraseñas y la emisión/validación de JWT (`app/infrastructure/auth/`) detrás de sus adapters; los casos de uso usan los ports, nunca las librerías (`bcrypt`, `PyJWT`) ni SQL/SQLAlchemy directo.
- Inyectar dependencias vía `Depends` y `dependency_injection.py` (funciones `get_*`), nunca construir el adapter dentro del caso de uso ni acceder a singletons ocultos/globales.
- El ensamblaje (`dependency_injection.py`, `app/main.py`) es el único lugar permitido para instanciar clientes concretos (async engine, sesión de BD, hasher de contraseñas, emisor de tokens).

## Reglas específicas de Python
- Tipar todo lo que se pueda: anotaciones en parámetros y retornos; `Optional[T]`/`T | None` en lugar de valores por defecto sin tipo.
- Usar `dataclasses` para entidades planas; no abusar de clases con estado si una función pura alcanza.
- Manejo de errores: las excepciones de negocio no se capturan en routers/use cases; se mapean a HTTP solo en `presentation/handlers.py`. No tragar excepciones con `except Exception: pass`.
- Preferir `with`/context managers para recursos (sesiones, conexiones, clientes de Google); evitar abrir/cerrar a mano.
- No importar desde `app/...` con rutas relativas desde dentro de `app/`; ejecutar desde la raíz del repo (imports `app.*`).
- Async por omisión (SQLAlchemy async + asyncpg): no bloquear con llamadas sync en endpoints sin necesidad.

## Cuándo NO aplicar esto a rajatabla
- No crear un port/abstracción para una dependencia que se usa una sola vez y no hay plan de reutilizarla o testearla por separado.
- No dividir una función corta (pocas líneas, alta cohesión) solo por "separación de responsabilidades" si no hay motivo de cambio independiente.
- Scripts únicos, seeds, migraciones puntuales, POCs o código de un solo uso no necesitan la misma rigurosidad que el código de producción reutilizable.
- Helpers puros y triviales (limpiar DNI, capitalizar) no necesitan port propio ni inyección de dependencias.

## Señales de alerta (smells)
- Clase/módulo con cientos de líneas mezclando SQL, validación, lógica de negocio y transformación → candidato a partirla en capas.
- Caso de uso instanciando `AsyncSession`, `bcrypt`, `PyJWT` o haciendo `session.execute(...)` directo → violación de inversión de dependencias.
- Import de FastAPI/SQLAlchemy/Pydantic dentro de `app/domain/` → violación de arquitectura limpia (el dominio debe ser puro).
- Port con métodos que casi todos los adapters dejan `pass`/`raise NotImplementedError` → interfaz gorda, dividir.
- Nombres genéricos tipo `utils.py`, `helpers.py`, `common.py` que terminan acumulando de todo → posible God Object.
- `try/except` de negocio en routers o use cases (la traducción a HTTP va solo en `handlers.py`) → smell.
- Valores mágicos repetidos (estados de usuario, nombres de roles por defecto, códigos de error) → centralizar en constantes/enums.

## Verificación
- Al terminar de escribir código, revisar explícitamente: responsabilidad única, extensibilidad sin tocar lo existente, contratos consistentes (excepciones + tipos), interfaces chicas, dependencias invertidas.
- Validar antes de dar por terminada una tarea:
  ```bash
  ./venv/bin/python -m pytest -q
  ```
- Correr sanity del dominio cuando el cambio es solo de dominio:
  ```bash
  ./venv/bin/python -m pytest tests/unit/domian/services -q
  ```