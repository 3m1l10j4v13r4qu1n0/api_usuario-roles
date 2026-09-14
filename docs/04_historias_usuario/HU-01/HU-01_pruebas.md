# HU-01: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Login válido con email en minúsculas (Éxito)
- Dado un usuario registrado `Juan.Perez@Example.com` con contraseña `secreto123`
- Cuando se autentica con el email `juan.perez@example.com`
- Entonces recibe `200` con un `access_token` y los roles `["USUARIO"]`

## Escenario 2: Login con password incorrecto (Error)
- Dado un usuario registrado con contraseña correcta
- Cuando se envía una contraseña distinta
- Entonces recibe `401` con `{"error": "Credenciales inválidas"}`

## Escenario 3: Login de usuario dado de baja (Error)
- Dado un usuario con `activo = False`
- Cuando intenta autenticarse
- Entonces recibe `401` con mensaje genérico

## Escenario 4: Consulta de perfil con token válido (Éxito)
- Dado un token JWT válido
- Cuando se consulta `GET /auth/me`
- Entonces recibe `200` con id, email, nombre_usuario y roles

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc1_login.py::test_login_valido_devuelve_token`
- [ ] `test_uc1_login.py::test_login_ignora_mayusculas_en_email`
- [ ] `test_uc1_login.py::test_login_password_incorrecto_lanza`
- [ ] `test_uc1_login.py::test_login_email_inexistente_lanza`
- [ ] `test_auth_service.py::test_credenciales_validas_devuelve_usuario`
- [ ] `test_auth_service.py::test_password_incorrecto_lanza`
- [ ] `test_auth_service.py::test_usuario_inactivo_lanza`
- [ ] `test_integration::test_flujo_completo.py::test_login_password_incorrecto_devuelve_401`
- [ ] `test_integration::test_flujo_completo.py::test_baja_logica_rechaza_login`