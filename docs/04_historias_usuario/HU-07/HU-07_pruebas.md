# HU-07: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Crear rol con descripción (Éxito)
- Dado un nombre de rol nuevo
- Cuando un ADMIN crea el rol
- Entonces recibe `201` con el rol y su descripción

## Escenario 2: Crear rol sin descripción (Éxito)
- Dado un rol sin `descripcion`
- Cuando un ADMIN crea el rol
- Entonces recibe `201` con `descripcion = null`

## Escenario 3: Nombre duplicado (Error)
- Dado que el rol ya existe
- Cuando se intenta crear de nuevo
- Entonces recibe `422` con "ya existe"

## Escenario 4: Nombre vacío (Error)
- Dado un rol con nombre vacío
- Cuando se intenta crear
- Entonces recibe `422`

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_uc7_crear_rol.py::test_crea_rol_con_descripcion`
- [ ] `test_uc7_crear_rol.py::test_crea_rol_sin_descripcion`
- [ ] `test_uc7_crear_rol.py::test_normaliza_nombre_y_descripcion`
- [ ] `test_uc7_crear_rol.py::test_nombre_vacio_lanza`
- [ ] `test_uc7_crear_rol.py::test_nombre_faltante_lanza`
- [ ] `test_uc7_crear_rol.py::test_nombre_duplicado_lanza`
- [ ] `test_integration::test_autorizacion_roles.py::test_403_sin_rol_admin_en_endpoints_admin`