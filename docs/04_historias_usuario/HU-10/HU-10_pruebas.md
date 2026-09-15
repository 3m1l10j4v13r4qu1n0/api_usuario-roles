# HU-10: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Quitado exitoso (Éxito)
- Dado un ADMIN autenticado y un usuario que posee un rol
- Cuando quita el rol
- Entonces recibe `200` y el usuario ya no lo incluye en `ids_roles`

## Escenario 2: Revocación sin re-login (Éxito)
- Dado un usuario con token vigente y rol ADMIN
- Cuando un ADMIN le quita el rol ADMIN
- Entonces el próximo request del usuario recibe `403` al intentar un endpoint ADMIN (sin re-login)

## Escenario 3: Rol inexistente (Error)
- Dado un `rol_id` inexistente
- Cuando se quita
- Entonces recibe `404`

## Escenario 4: Usuario inexistente (Error)
- Dado un usuario inexistente
- Cuando se le quita un rol
- Entonces recibe `404`

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc10_quitar_rol.py::test_quitar_rol_remueve_el_rol_del_usuario`
- [ ] `test_uc10_quitar_rol.py::test_quitar_rol_invalida_estado_en_cache`
- [ ] `test_uc10_quitar_rol.py::test_rol_inexistente_lanza`
- [ ] `test_uc10_quitar_rol.py::test_usuario_inexistente_lanza`
- [ ] `test_integration::test_autorizacion_roles.py::test_quitar_rol_revoca_sin_relogin`