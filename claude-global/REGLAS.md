# Segundo cerebro (reglas para todas las conversaciones)

El usuario tiene una bóveda de Obsidian en `~/Documents/SegundoCerebro` (en Windows, `%USERPROFILE%\Documents\SegundoCerebro`), sincronizada con un repositorio privado suyo en GitHub. Se trae sola al empezar cada sesión y se sube sola al cerrarla (hooks de `~/.claude/settings.json` que ejecutan `scripts/sync.sh`).

## Consultar
- Antes de empezar una tarea sobre un proyecto, cliente o tema, mira si hay algo en `wiki/` de la bóveda (empieza por `wiki/Inicio.md`). Úsalo como contexto sin anunciarlo.
- Si existe `proyectos/<Proyecto>/` o el proyecto tiene `graphify-out/graph.json`, consulta el grafo antes de leer muchos archivos.

## Guardar
Al terminar algo que merezca recordarse, escribe **una** nota en `raw/` de la bóveda, sin pedir permiso:
- **Sí:** decisiones y por qué, problemas resueltos y su causa, cómo funciona algo que costó entender, datos de un proyecto o cliente, preferencias del usuario, tareas pendientes.
- **No:** charla trivial, preguntas sueltas, lo que ya está en el código o en git, contraseñas, claves, tokens ni datos personales sensibles.

Formato: `raw/AAAA-MM-DD <proyecto> - <tema>.md`

```markdown
---
tipo: fuente
origen: conversación de Claude Code
proyecto: <nombre o ruta del proyecto>
capturado: AAAA-MM-DD
procesado: false
---

# <Tema>

- Qué se hizo / decidió
- Por qué
- Pendiente
```

Una nota por tema; si ya existe una del mismo día y tema, añádele contenido en vez de crear otra. Al final dile al usuario en una línea que lo has guardado en la bóveda.

No hagas commit ni push tú: lo hace el hook al cerrar la sesión. La conversión de `raw/` a `wiki/` se hace al decir «procesa raw» dentro de la bóveda.
