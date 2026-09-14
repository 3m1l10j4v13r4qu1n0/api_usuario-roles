# Reglas de Negocio Transversales

Reglas aplicables de forma transversal al sistema. Las **RN01..RN06** están codificadas en
`app/domain/services/` (normalización y validación, dominio puro). Las **USR-RN07..RN15**
describen comportamiento del sistema deducido del código y verificado por tests.

| Código | Regla | Dónde se aplica |
|---|---|---|
| RN01 | Los emails se **almacenan en minúsculas** (y se normalizan antes de comparar). | UC1, UC2, UC5 — `normalizacion.py` |
| RN02 | Los textos no deben contener espacios al inicio ni al final (se recortan con `strip`). | UC1, UC2, UC5, UC7 — `normalizacion.py` |
| RN03 | Los **nombres de usuario conservan mayúsculas** (solo se recortan los bordes). | UC2 — `normalizacion.py` |
| RN04 | El email debe tener un **formato válido** (validado con `email-validator`). | UC1, UC2, UC5 — `validacion.py` |
| RN05 | Los **campos obligatorios no pueden estar vacíos** (email, nombre de usuario, contraseña). | UC2, UC7 — `validacion.py` / schemas Pydantic |
| RN06 | La **contraseña debe tener un largo mínimo de 8 caracteres**. | UC2, UC5 — `validacion.py` / schema `UsuarioCreate` |
| USR-RN07 | La **baja de usuario es lógica**: `activo = False`, nunca se borra físicamente. | UC6 — `usuario_command_repository.dar_de_baja` |
| USR-RN08 | El **login rechaza usuarios inactivos** (mismo error genérico de credenciales). | UC1 — `auth_service.verificar_activo` |
| USR-RN09 | La **autorización por rol usa intersección**: el usuario debe poseer *alguno* de los roles requeridos; si la lista requerida está vacía, se permite. | `auth_service.autorizar` — todos los endpoints con rol |
| USR-RN10 | **Matriz de roles**: listar usuarios, dar de baja, asignar/quitar rol y `/roles/*` exigen `ADMIN`; ver/editar un usuario exige `ADMIN` o el propio usuario (`require_mismo_usuario_o_admin`); el registro es público. | `app/presentation/routers/` |
| USR-RN11 | La **autorización lee el estado real** (activo + roles) del usuario desde el cache TTL o la BD; **no confía en las claims del token**. | `auth_dependencies.get_current_user` |
| USR-RN12 | La **revocación es en caliente**: asignar rol, quitar rol o dar de baja invalidan el estado cacheado del usuario, y el cambio se refleja en el próximo request sin re-login. | UC6, UC9, UC10 — `EstadoUsuarioCachePort.invalidar` |
| USR-RN13 | El **registro autoasigna el rol `USUARIO`** (por defecto); si el rol no existe, el alta no se rompe (el usuario queda sin rol). | UC2 — `ROL_POR_DEFECTO = "USUARIO"` |
| USR-RN14 | El **`password_hash` nunca se expone** en las respuestas de la API. | Schemas de salida (`UsuarioResponse`, `TokenResponse`, `CurrentUserResponse`) |
| USR-RN15 | El login usa un **mensaje de error genérico** (“Credenciales inválidas”) para no revelar si falló el email o la contraseña. | UC1 — `auth_service.verificar_credenciales` |