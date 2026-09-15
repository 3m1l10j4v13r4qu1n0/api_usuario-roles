# Metodología (Kanban, WIP, flujo y ciclo de desarrollo con IA)

## Aplicación de Kanban en Trello

### Justificación

El proyecto se gestiona con **Kanban en Trello** porque su flujo por fases es continuo y
lineal (andamiaje → BD → tests → autorización → cierre), sin necesidad de sprints fijos.
Cada caso de uso (UC1..UC10) equivale a una tarjeta y cada fase del plan a un hito.

### Límites de WIP (work in progress)

- **En desarrollo**: máximo **1 tarjeta** (una rama = una HU/UC).
- **En revisión**: máximo **2 tarjetas**.
- **En pruebas (QA)**: máximo **2 tarjetas**.
- **Listo**: sin límite; solo se mueve a "Terminado" cuando se mergea a `develop`.

### Flujo de la tarjeta (5 pasos)

1. **Backlog** → item del plan o decisión pendiente de `docs/plan_implementacion.md`.
2. **En desarrollo** → se crea la rama `feature/<tema>` (o `fix/<tema>`) **desde `develop`**.
3. **En revisión** → `ruff`/`black`/`pytest` en verde y commit atómico.
4. **En pruebas** → merge a `develop` (previo integrar `origin/develop`) y, si aplica,
   correr `pytest tests/integration/` contra BD real.
5. **Terminado** → tag anotado semver (`v1.3.0`, etc.) al cerrar la fase.

### Política de commits

- Conventional Commits en **español**, scope en minúscula (`feat(usecase)`, `fix(auth)`...).
- **Un tema por commit**; si el cambio necesita "y", son dos commits.
- Prohibido mensajes vagos ("cambios", "update").

---

## Uso del ciclo de desarrollo con IA

El flujo de trabajo con el agente de IA sigue la tabla de **etapa / equipo / IA**:

| Etapa | Equipo | IA |
|---|---|---|
| Requisitos | Define alcanza, actores y reglas de negocio en `docs/01_global/`. | Documenta por ingeniería inversa desde el código y detecta huecos. |
| Diseño | Decide arquitectura, matriz de roles y decisiones técnicas. | Propone diagramas PlantUML y valida contra la arquitectura real. |
| Codificación | Implementación de UCs/endpoints por ramas feature cortas. | Escribe código siguiendo un skill de implementación (Clean Architecture + Hexagonal) y checklist `ruff`/`black`/`pytest`. |
| Pruebas | Revisa criterios de aceptación y DoR. | Escribe/actualiza tests unitarios (fakes) y de integración (BD real). |
| Documentación | Valida que la doc refleje el estado real. | Actualiza `estado_actual_proyecto.md` y la vitácora (append-only). |

### Reflexión

- La IA trabaja en **pasos chicos** (un UC, un endpoint, un componente por vez) y reporta
  qué verificó, qué cambió y qué queda pendiente.
- El **dominio nunca se acopla a frameworks**: si el cambio toca más de una HU o es un refactor
  transversal, se requiere OK explícito del equipo.
- La doc es **fuente de verdad** (`docs/`) y el código real puede corregirla: ante una
  discrepancia se avisa antes de asumir cuál prevalece.