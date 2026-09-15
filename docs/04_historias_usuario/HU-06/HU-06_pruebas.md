# HU-06: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Baja lógica (Éxito)
- Dado un ADMIN autenticado y un usuario existente y activo
- Cuando da de baja a ese usuario
- Entonces recibe `200` y el usuario queda con `activo = False`

## Escenario 2: Login rechazado post-baja (Error)
- Dado un usuario dado de baja
- Cuando intenta autenticarse con credenciales correctas
- Entonces recibe `401` con mensaje genérico

## Escenario 3: Token vigente de usuario inactivo (Error)
- Dado un usuario inactivo con token aún vigente
- Cuando consulta un endpoint protegido
- Entonces recibe `401`

## Escenario 4: Usuario inexistente (Error)
- Dado un id inexistente
- Cuando se da de baja
- Entonces recibe `404`

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc6_dar_de_baja_usuario.py::test_baja_logica_marca_inactivo`
- [ ] `test_uc6_dar_de_baja_usuario.py::test_baja_invalida_estado_en_cache`
- [ ] `test_uc6_dar_de_baja_usuario.py::test_usuario_inexistente_lanza`
- [ ] `test_integration::test_flujo_completo.py::test_baja_logica_rechaza_login`
- [ ] `test_integration::test_autorizacion_roles.py::test_usuario_inactivo_con_token_vigente_recibe_401`