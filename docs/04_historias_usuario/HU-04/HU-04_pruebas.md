# HU-04: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: ADMIN consulta cualquier usuario (Éxito)
- Dado un ADMIN autenticado
- Cuando consulta `GET /usuarios/{id}` de un usuario existente
- Entonces recibe `200` con sus datos

## Escenario 2: El propietario consulta su perfil (Éxito)
- Dado un usuario autenticado con rol USUARIO
- Cuando consulta `GET /usuarios/{su propio id}`
- Entonces recibe `200`

## Escenario 3: Otro usuario sin ADMIN consulta un id ajeno (Error)
- Dado un usuario autenticado con rol USUARIO
- Cuando consulta `GET /usuarios/{id de otro usuario}`
- Entonces recibe `403`

## Escenario 4: Usuario inexistente (Error)
- Dado un id que no existe
- Cuando se consulta
- Entonces recibe `404`

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc4_obtener_usuario_por_id.py::test_usuario_existente_se_devuelve`
- [ ] `test_uc4_obtener_usuario_por_id.py::test_usuario_inexistente_lanza`
- [ ] `test_integration::test_autorizacion_roles.py::test_mismo_usuario_puede_ver_y_editar_su_perfil`
- [ ] `test_integration::test_autorizacion_roles.py::test_otro_usuario_no_admin_obtiene_403`