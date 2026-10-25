# Segundo cerebro: instrucciones para el agente

Este directorio es una bóveda de Obsidian. Abre aquí tu agente (Codex, Claude Code u otro que lea `AGENTS.md`) para trabajar con todo el contexto guardado.

## Estructura

| Carpeta | Para qué | Quién escribe |
|---|---|---|
| `raw/` | Bandeja de entrada: notas, ideas, transcripciones, PDFs, capturas. Sin orden. | El usuario y el agente |
| `wiki/` | Conocimiento estructurado, una nota por concepto, como una Wikipedia interna. | El agente |
| `output/` | Lo que produce el agente: documentos, investigaciones, planes, contenido. | El agente |
| `proyectos/` | Grafos de proyectos de código generados con Graphify. | Graphify |
| `empresa/` | Kit para montar el cerebro de IA de una empresa con permisos por persona. | Ambos |
| `plantillas/` | Plantillas de notas. | Ambos |

## Reglas

1. **Antes de responder sobre un tema, busca en `wiki/`** y luego en `raw/`. No empieces de cero si ya existe algo.
2. **Nunca borres ni reescribas el contenido de `raw/`.** Es la fuente original. Cuando una nota ya está procesada, cambia solo su frontmatter a `procesado: true`.
3. **Todo lo que crees para el usuario va a `output/`**, con la fecha en el nombre (`AAAA-MM-DD titulo.md`) y enlazando las notas de la wiki que usaste.
4. Escribe en español y en Markdown compatible con Obsidian: frontmatter YAML, `[[wikilinks]]` y `#etiquetas`.
5. En proyectos de código grandes, usa el grafo de Graphify (`proyectos/<Nombre>/` o `graphify-out/` del proyecto) en vez de leer todos los archivos.
6. Nunca guardes contraseñas, claves, tokens, datos bancarios ni datos personales de terceros.

## Procedimientos

### «Procesa raw»
- **Documentos primero.** Por cada archivo de `raw/` que no sea `.md` (PDF, Word, PowerPoint, Excel, imágenes, texto…) y que no tenga al lado su ficha `<archivo>.md`:
  - Saca el texto con `python scripts/extraer_texto.py "raw/<archivo>"`. Si no da texto (imagen, PDF escaneado o sin pypdf), míralo directamente.
  - Crea la ficha `raw/<archivo>.md` (p. ej. `raw/oferta.pdf.md`) con el frontmatter de fuente (`tipo: fuente`, `origen: documento`, `procesado: false`), una línea `Documento: [[<archivo>]]` y un resumen: de qué trata, datos clave (cifras, fechas, nombres, decisiones) y para qué sirve. El documento original no se toca.
- Busca en `raw/` las notas sin `procesado: true`, incluidas esas fichas.
- Extrae cada concepto, persona, proyecto o herramienta a su propia nota en `wiki/` (nombre en singular, Título Con Mayúsculas). Si ya existe, añade la información nueva en lugar de duplicarla.
- Enlaza con `[[wikilinks]]` y cita la fuente en el frontmatter: `fuentes: ["[[raw/nombre]]"]`.
- Marca la nota de `raw/` como `procesado: true` y actualiza `wiki/Inicio.md`.

### «Investiga / hazme un documento sobre…»
- Mira primero qué hay en `wiki/` y `raw/`. Solo si falta algo, busca fuera y cita las fuentes.
- Escribe el resultado en `output/AAAA-MM-DD <titulo>.md`, enlazando las notas usadas.

### «Importa mi historial»
1. `python scripts/extraer_historial.py`: extrae las conversaciones antiguas de Codex y de Claude Code de este ordenador a `~/.cache/segundo-cerebro/historial/`, una ficha por conversación, con las claves tapadas. Muestra cuántas hay por proyecto. Si son muchas, pregunta al usuario si las quiere todas o solo los últimos N días (`--dias N`).
2. Lee las fichas y escribe en `raw/` **una nota por proyecto y tema**, no una por conversación (`raw/AAAA-MM-DD <proyecto> - <tema>.md`): qué se hizo, decisiones y por qué, problemas y su causa, datos del proyecto, preferencias del usuario y pendientes. Ignora lo trivial y no reconstruyas nada marcado `[CLAVE]`, `[TOKEN]` u `[OCULTO]`.
3. `python scripts/extraer_historial.py --marcar` para no repetirlas la próxima vez.

### Indexar un proyecto de código
Dentro del proyecto: `/graphify . --obsidian --obsidian-dir <bóveda>/proyectos/<Nombre>` (o `graphify` desde la terminal), y después `python <bóveda>/scripts/visor_grafo.py graphify-out` para generar `grafo.html`, el visor del grafo. Tras cada cambio de código: `/graphify . --update` y vuelve a generar el visor.

## Frontmatter estándar

```yaml
---
tipo: concepto | persona | proyecto | herramienta | fuente | output
etiquetas: []
creado: AAAA-MM-DD
fuentes: []
---
```
