# HU-08: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Lista con roles (Éxito)
- Dado que existen roles (seed + creados)
- Cuando un ADMIN consulta `GET /roles/`
- Entonces recibe `200` con todos los roles

## Escenario 2: Lista vacía (Éxito)
- Dado que no hay roles
- Cuando un ADMIN consulta `GET /roles/`
- Entonces recibe `200` con `[]`

## Escenario 3: Sin rol ADMIN (Error)
- Dado un usuario autenticado sin ADMIN
- Cuando consulta `GET /roles/`
- Entonces recibe `403`

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc8_listar_roles.py::test_sin_roles_devuelve_lista_vacia`
- [ ] `test_uc8_listar_roles.py::test_con_roles_devuelve_todos`
- [ ] `test_uc8_listar_roles.py::test_devuelve_instancias_rol`
- [ ] `test_integration::test_flujo_completo.py::test_registrar_login_me_asignar_rol_y_listar_roles`