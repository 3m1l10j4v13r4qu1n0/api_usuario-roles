# HU-03: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Lista con usuarios (Éxito)
- Dado que existen usuarios registrados
- Cuando un ADMIN consulta `GET /usuarios/`
- Entonces recibe `200` con todos los usuarios

## Escenario 2: Lista vacía (Éxito)
- Dado que no hay usuarios
- Cuando un ADMIN consulta `GET /usuarios/`
- Entonces recibe `200` con `[]`

## Escenario 3: Sin rol ADMIN (Error)
- Dado un usuario autenticado con rol USUARIO
- Cuando consulta `GET /usuarios/`
- Entonces recibe `403`

## Escenario 4: Sin token (Error)
- Dado un request sin token
- Cuando consulta `GET /usuarios/`
- Entonces recibe `401`

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc3_listar_usuarios.py::test_sin_usuarios_devuelve_lista_vacia`
- [ ] `test_uc3_listar_usuarios.py::test_con_usuarios_devuelve_todos`
- [ ] `test_integration::test_autorizacion_roles.py::test_403_sin_rol_admin_en_endpoints_admin`
- [ ] `test_integration::test_flujo_completo.py::test_endpoints_protegidos_sin_token_devuelven_401`