# Segundo cerebro — instrucciones para Claude

Este directorio es una bóveda de Obsidian. Abre Claude Code aquí dentro para trabajar con todo el contexto guardado.

## Estructura

| Carpeta | Para qué | Quién escribe |
|---|---|---|
| `raw/` | Bandeja de entrada: notas, ideas, transcripciones, PDFs, capturas. Sin orden. | El usuario (y las skills que capturan, p. ej. `/watch-video`) |
| `wiki/` | Conocimiento estructurado, una nota por concepto, como una Wikipedia interna. | Claude |
| `output/` | Lo que Claude produce: documentos, investigaciones, planes, contenido. | Claude |
| `empresa/` | Kit para montar el cerebro de IA de una empresa con permisos por persona. | Ambos |
| `plantillas/` | Plantillas de notas. | Ambos |

## Reglas

1. **Antes de responder sobre un tema, busca en `wiki/`** (y luego en `raw/`). No empieces de cero si ya existe algo.
2. **Nunca borres ni reescribas nada en `raw/`.** Es la fuente original. Cuando una nota de `raw/` ya está procesada, añádele `procesado: true` en el frontmatter.
3. **Procesar `raw/` → `wiki/`** (cuando el usuario diga "procesa raw", "ordena", o al detectar notas sin procesar):
   - Extrae cada concepto, persona, proyecto o herramienta a su propia nota en `wiki/` (nombre en singular, Título Con Mayúsculas).
   - Si la nota ya existe, añade la información nueva en vez de duplicar.
   - Enlaza con `[[wikilinks]]` a otras notas de la wiki y cita la fuente: `Fuente: [[raw/nombre-del-archivo]]`.
   - Actualiza `wiki/Inicio.md` (índice) con las notas nuevas.
4. **Todo lo que crees para el usuario va a `output/`**, con fecha en el nombre: `AAAA-MM-DD titulo.md`, y enlazando las notas de la wiki que usaste.
5. Escribe en español, en Markdown compatible con Obsidian (frontmatter YAML, `[[wikilinks]]`, `#etiquetas`).
6. Para proyectos de código grandes usa `/graphify <ruta> --obsidian` para volcar su grafo de conocimiento aquí en vez de leer todos los archivos.

## Frontmatter estándar

```yaml
---
tipo: concepto | persona | proyecto | herramienta | fuente | output
etiquetas: []
creado: AAAA-MM-DD
fuentes: []
---
```
