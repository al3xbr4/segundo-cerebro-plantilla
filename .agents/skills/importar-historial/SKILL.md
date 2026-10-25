---
name: importar-historial
description: Importa a la bóveda las conversaciones antiguas de Claude Code de este ordenador (o un export de claude.ai) y las convierte en notas de raw/. Úsalo cuando el usuario diga "importa mi historial", "aprovecha mis conversaciones", "/importar-historial" o al montar la bóveda en un ordenador nuevo.
---

# /importar-historial

Convierte las conversaciones pasadas en conocimiento de la bóveda. Se ejecuta **dentro de la bóveda**.

## 1. Extraer

```bash
python scripts/extraer_historial.py            # todas las pendientes de este ordenador
python scripts/extraer_historial.py --dias 90  # si el usuario quiere solo las recientes
python scripts/extraer_historial.py --claude-ai <ruta>/conversations.json   # export de claude.ai
```

El script deja una ficha por conversación en `~/.cache/segundo-cerebro/historial/` (fuera de la bóveda, no se sube) y muestra cuántas hay por proyecto y su tamaño aproximado. Las ya importadas se saltan solas.

Si salen más de ~300k tokens, enséñale al usuario el reparto por proyecto y pregúntale si quiere todo o solo algunos proyectos o los últimos N días.

## 2. Resumir en notas

Reparte las fichas por proyecto. Si son muchas, lanza subagentes `general-purpose` en paralelo, uno por proyecto o por bloque de unos 150k tokens, cada uno con estas instrucciones:

- Lee las fichas completas que le tocan.
- Escribe en `raw/` de la bóveda **una nota por proyecto y tema**, no una por conversación: `raw/AAAA-MM-DD <proyecto> - <tema>.md`, con la fecha de la conversación más reciente del tema.
- Frontmatter:
  ```yaml
  ---
  tipo: fuente
  origen: historial de Claude Code (<ordenador>)
  proyecto: <proyecto>
  sesiones: [<id8>, <id8>]
  capturado: <hoy>
  procesado: false
  ---
  ```
- Contenido: qué se hizo, **decisiones y por qué**, problemas y su causa, cómo funciona lo que costó entender, datos del proyecto o cliente, preferencias del usuario y lo que quedó pendiente. En viñetas, sin copiar la conversación.
- **No guardar:** contraseñas, claves, tokens, datos bancarios ni datos personales de terceros (teléfonos, DNI, direcciones de particulares). Si una ficha trae `[CLAVE]`, `[TOKEN]` u `[OCULTO]`, no hay que intentar reconstruirlo.
- Las conversaciones triviales (un saludo, una pregunta suelta sin resultado) se ignoran.
- Si ya existe en `raw/` o en `wiki/` una nota del mismo proyecto y tema, añade la información en lugar de duplicarla.
- Al acabar, devuelve la lista de notas creadas o ampliadas.

## 3. Cerrar

1. `python scripts/extraer_historial.py --marcar`: marca las conversaciones como importadas y borra las fichas temporales.
2. Pregúntale al usuario si quiere procesarlo ya a la wiki (subagente `procesador-raw`, o «procesa raw»).
3. Resume: cuántas conversaciones, qué notas y de qué proyectos. La subida a GitHub la hace el hook al cerrar la sesión.

Nota: Claude Code borra las conversaciones de más de 30 días salvo que `cleanupPeriodDays` diga otra cosa en `~/.claude/settings.json`. Si el usuario quiere conservar más historial para el futuro, sugiérele subir ese valor (por ejemplo a 365).
