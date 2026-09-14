# Auditoría de documentación — actualizar plan de implementacion

Regla dura. Aplica a agentes y humanos por igual.

## 1. Contexto y por qué existe

Cuando se audita documentación del proyecto (requerimientos, especificaciones, planes, historias de usuario), el
resultado no puede quedarse solo en un informe aparte: el documento fuente del grupo/área
afectada debe quedar **actualizado** para seguir siendo la fuente de verdad.

## 2. Alcance

- Aplica a auditorías de cualquier documento de `docs/` (análisis funcional, backend, plan de implementación).

## 3. Pasos obligatorios

1. **Identificar** el grupo/área del documento auditado (1=global, 2=tecnico, 3=procesos,
   4=historias_usuario/usecases, 5=auditorias).
2. **Leer completo** el archivo del grupo antes de editarlo (nunca editar sin releer).
3. **Marcar** con la leyenda de la sección 4 cada ítem según el estado verificado en la sesión.
4. **Aplicar** en el archivo del grupo las correcciones que surjan de la auditoría y estén
   verificadas (typos, valores, configs de ejemplo, estados).


## 4. Leyenda de estados (consistente con las auditorías existentes)

| Símbolo | Significado |
|---|---|
| ✅ | listo / ya cubierto por el proyecto (verificado en la sesión) |
| 🟡 | parcial: difiere levemente entre documentos o falta alinear |
| 🔵 | pendiente externo: depende de otro equipo / Dirección / Backend |
| ⏳ | en proceso / bloqueado temporalmente |

## 5. Anti-alucinación

- Marcar ✅ **solo** lo verificado en la sesión actual (archivo leído, comando corrido).
- No cambiar estados que dependan de decisiones externas no confirmadas (ej. "VPS contratado"
  no se marca ✅ porque lo diga una propuesta: hay que confirmarlo con Infra/Dirección).
- Releer el archivo del grupo tras editarlo (`.agents/rules/Reglas-anti-alucinacion.md` §4).

## 6. Cierre de la auditoría

1. Generar o actualizar el informe versionado en `docs/auditorias/auditoria-*.md`, referenciando
   el archivo del grupo modificado.
2. Actualizar `docs/estado_actual_proyecto.md` (sección correspondiente, in-place).
3. Agregar entrada en `docs/vitacora_agentica.md` (append-only) con fecha, qué se hizo,
   decisiones, archivos tocados y estado resultante.