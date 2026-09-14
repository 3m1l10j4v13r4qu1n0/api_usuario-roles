# Actores del Sistema

El sistema distingue actores por **autenticación** y por **rol**. Los roles definidos por
seed son dos: `ADMIN` (acceso total) y `USUARIO` (acceso básico, autoasignado en el alta).
La autorización usa intersección de roles (el usuario debe tener **alguno** de los requeridos).

1. **Usuario No Autenticado (visitante)** — Persona o sistema sin token JWT. Solo puede
   realizar acciones públicas: registrar un usuario (`POST /usuarios/`), autenticarse
   (`POST /auth/login`) y el health check (`GET /`).

2. **Usuario Autenticado (token JWT válido)** — Tiene un Bearer token emitido por el login.
   Puede acceder a `/auth/me` y a su propio recurso en `/usuarios` (ver o editar su perfil,
   dependencia `require_mismo_usuario_o_admin`). Sus roles y su estado `activo` se resuelven
   desde el estado real (cache TTL / BD), no de las claims del token.

3. **Administrador (rol `ADMIN`)** — Usuario autenticado con rol `ADMIN`. Puede listar
   usuarios, dar de baja (lógica), asignar/quitar roles a cualquier usuario y gestionar roles
   (`/roles/*`). Es el único que opera sobre recursos que no le pertenecen.

4. **Sistema consumidor (frontend / otro microservicio)** — Cliente HTTP que consume la API
   en nombre de un actor anterior. Se identifica enviando el `Authorization: Bearer <token>`
   en cada request protegido; sobre él no se guarda estado en la BD.