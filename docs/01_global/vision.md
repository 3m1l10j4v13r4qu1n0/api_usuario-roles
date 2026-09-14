# Visión del Proyecto

El ecosistema de microservicios necesita un punto central que diga **quién es** un usuario y **qué puede hacer**: una capa de autenticación y autorización compartida. Sin ella, cada servicio tendría que implementar su propia lógica de usuarios, contraseñas y permisos, generando duplicación, inconsistencias de datos y superficies de ataque distintas.

`api_usuario-roles` resuelve eso con una API REST **única** que centraliza el ciclo de vida de los usuarios y los roles: registro, login con JWT, gestión del perfil, alta/baja lógica y asignación de roles. El resto del ecosistema solo necesita confiar en el token emitido y verificar el rol del usuario, sin repetir lógica.

Este proyecto es además un **ejercicio educativo de arquitectura**: todo el código sigue Clean Architecture + Hexagonal (Ports & Adapters) para separar la lógica de negocio (dominio puro, sin frameworks) de la infraestructura (BD, hashing, tokens, cache), lo que lo hace testeable y entendible en capas.