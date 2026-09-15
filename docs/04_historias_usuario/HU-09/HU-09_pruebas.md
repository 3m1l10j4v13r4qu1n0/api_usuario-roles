# HU-09: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Asignación exitosa (Éxito)
- Dado un ADMIN autenticado, un rol existente y un usuario existente
- Cuando asigna el rol al usuario
- Entonces recibe `200` y el usuario incluye el rol en `ids_roles`

## Escenario 2: Asignación reflejada sin re-login (Éxito — revocación en caliente)
- Dado un usuario con token vigente sin rol ADMIN
- Cuando un ADMIN le asigna el rol ADMIN
- Entonces el próximo request del usuario accede a un endpoint ADMIN (sin re-login)

## Escenario 3: Rol inexistente (Error)
- Dado un `id_rol` inexistente
- Cuando se asigna
- Entonces recibe `404`

## Escenario 4: Usuario inexistente (Error)
- Dado un usuario inexistente
- Cuando se le asigna un rol
- Entonces recibe `404`

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc9_asignar_rol.py::test_asignacion_exitosa_agrega_rol_al_usuario`
- [ ] `test_uc9_asignar_rol.py::test_asignacion_invalida_estado_en_cache`
- [ ] `test_uc9_asignar_rol.py::test_rol_inexistente_lanza`
- [ ] `test_uc9_asignar_rol.py::test_usuario_inexistente_lanza`
- [ ] `test_integration::test_autorizacion_roles.py::test_asignar_rol_se_refleja_sin_relogin`