# HU-05: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Actualización parcial (Éxito)
- Dado un usuario existente
- Cuando se actualiza solo `nombre_completo`
- Entonces recibe `200` y solo cambia ese campo

## Escenario 2: Cambio de email normalizado (Éxito)
- Dado un usuario existente
- Cuando se actualiza el email con `JUAN.C@EXAMPLE.COM`
- Entonces recibe `200` y el email queda en minúsculas

## Escenario 3: Cambio de password (Éxito)
- Dado un usuario existente
- Cuando se envía un `password` nuevo válido
- Entonces recibe `200` y el `password_hash` se regenera

## Escenario 4: Email en uso por otro (Error)
- Dado que el email pertenece a otro usuario
- Cuando se intenta actualizar con ese email
- Entonces recibe `409`

## Escenario 5: Usuario inexistente (Error)
- Dado un id inexistente
- Cuando se actualiza
- Entonces recibe `404`

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc5_actualizar_usuario.py::test_actualiza_nombre_usuario_y_nombre_completo`
- [ ] `test_uc5_actualizar_usuario.py::test_actualiza_email_normalizado`
- [ ] `test_uc5_actualizar_usuario.py::test_cambia_password_y_hashea`
- [ ] `test_uc5_actualizar_usuario.py::test_email_en_uso_por_otro_lanza`
- [ ] `test_uc5_actualizar_usuario.py::test_mismo_email_no_lanza`
- [ ] `test_uc5_actualizar_usuario.py::test_usuario_inexistente_lanza`
- [ ] `test_uc5_actualizar_usuario.py::test_sin_campos_no_rompe`