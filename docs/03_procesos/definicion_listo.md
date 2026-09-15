# Definition of Ready (DoR)

Checklist mínima para que una Historia de Usuario / Caso de Uso pase de "pendiente" a
"en desarrollo" en este proyecto. Está adaptado al flujo por fases de `docs/plan_implementacion.md`.

- [ ] La HU/UC está redactada con el formato **Como / quiero / para** y tiene **criterios de aceptación**
      en Gherkin (Dado/Cuando/Entonces).
- [ ] Los **casos de prueba TDD / SbE** están definidos con los nombres esperados de los tests
      (patrón `tests/unit/domian/services/test_ucN_*.py`).
- [ ] La **especificación de API** está documentada (método, ruta, request/response JSON,
      status codes por error) tomando los schemas reales de `app/presentation/schemas/`.
- [ ] Las **entidades de datos** afectadas están identificadas (dominio y tablas ORM).
- [ ] El **caso de uso expandido** tiene actor, precondición, flujo principal y flujos alternativos
      (excepciones de dominio → status code).
- [ ] Se definió la **protección del endpoint**: público, `require_roles(...)` o `require_mismo_usuario_o_admin`.
- [ ] La implementación sigue Clean Architecture: dominio puro, port nuevo si aplica, cableado en
      `dependency_injection.py` y test unitario con fakes.

---

## Checklist de "listo para merge" (DoD)

- [ ] `venv/bin/ruff check .` en verde.
- [ ] `venv/bin/black --check .` en verde.
- [ ] `venv/bin/python -m pytest -q` en verde (unitarios con fakes, sin BD).
- [ ] Si toca BD real: `venv/bin/python -m pytest tests/integration/` en verde.
- [ ] Si cambia el esquema: migración Alembic (`alembic revision --autogenerate` + `upgrade head`).
- [ ] Commit atómico con Conventional Commits en español y un solo tema.
- [ ] Actualización de `docs/estado_actual_proyecto.md` + entrada en `docs/vitacora_agentica.md`.