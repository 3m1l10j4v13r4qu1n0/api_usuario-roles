# HU-02: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Registro exitoso (Éxito)
- Dado un email no registrado y datos válidos
- Cuando se registra el usuario
- Entonces recibe `201` con el usuario creado y `activo = True`

## Escenario 2: Autoasignación del rol USUARIO (Éxito)
- Dado que existe el rol `USUARIO`
- Cuando se registra un usuario
- Entonces el usuario queda con `ids_roles` conteniendo el id del rol `USUARIO`

## Escenario 3: Email duplicado (Error)
- Dado un email ya registrado
- Cuando se intenta registrar otro usuario con ese email
- Entonces recibe `409` con `{"error": "El email ... ya está registrado"}`

## Escenario 4: Email en mayúsculas (Éxito/Normalización)
- Dado un registro con `JUAN.PEREZ@EXAMPLE.COM`
- Entonces el email almacenado es `juan.perez@example.com`

## Escenario 5: Contraseña corta (Error)
- Dado un registro con una contraseña de menos de 8 caracteres
- Entonces recibe `422`

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc2_registrar_usuario.py::test_registro_exitoso_devuelve_usuario`
- [ ] `test_uc2_registrar_usuario.py::test_registro_autoasigna_rol_usuario_por_defecto`
- [ ] `test_uc2_registrar_usuario.py::test_registro_sin_rol_defecto_crea_sin_roles`
- [ ] `test_uc2_registrar_usuario.py::test_registro_normaliza_email_y_nombre`
- [ ] `test_uc2_registrar_usuario.py::test_registro_sin_nombre_completo`
- [ ] `test_uc2_registrar_usuario.py::test_email_duplicado_lanza`
- [ ] `test_uc2_registrar_usuario.py::test_email_duplicado_normaliza_mayusculas`
- [ ] `test_uc2_registrar_usuario.py::test_email_invalido_lanza`
- [ ] `test_uc2_registrar_usuario.py::test_password_corta_lanza`
- [ ] `test_uc2_registrar_usuario.py::test_nombre_usuario_vacio_lanza`
- [ ] `test_integration::test_autorizacion_roles.py::test_registro_autoasigna_rol_usuario`
- [ ] `test_integration::test_flujo_completo.py::test_email_duplicado_devuelve_409`