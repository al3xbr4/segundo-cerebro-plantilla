---
tipo: herramienta
etiquetas: [claude-code, tokens, codigo]
creado: 2026-10-25
fuentes: ["https://github.com/Graphify-Labs/graphify"]
---

# Graphify

Skill + CLI que convierte un proyecto (código, docs, PDFs, imágenes, vídeo) en un **grafo de conocimiento** que se consulta en vez de hacer grep o releer archivos. Es la base del [[Ahorro De Tokens]].

- El código se analiza en local con tree-sitter (sin LLM, nada sale de tu máquina).
- Cada relación se marca como `EXTRACTED` (explícita) o `INFERRED` (deducida).

## Uso (instalado)
En [[Claude Code]], dentro del proyecto:
```
/graphify .                 # crea graphify-out/ (graph.html, GRAPH_REPORT.md, graph.json)
/graphify . --obsidian      # además genera notas para Obsidian
```
CLI: `graphify query "pregunta"`, `graphify path "A" "B"`, `graphify explain "X"`.

Instalado con `uv tool install graphifyy` + `graphify install --platform claude`. Ejecutable en `~/.local/bin`.
