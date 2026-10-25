# 🧠 Segundo cerebro

Bóveda de Obsidian pensada para trabajar con Codex o Claude Code. Las reglas para el agente están en `AGENTS.md`.

## Cómo se usa

1. **Mete cosas en `raw/`** sin preocuparte del orden: notas, ideas, PDFs, transcripciones de vídeo.
2. **Abre tu agente (Codex o Claude Code) en esta carpeta** y pídele: *"procesa raw"*. Lo convierte en notas enlazadas en `wiki/`.
3. **Pídele trabajo**: *"hazme un plan de lanzamiento usando lo que sabes de mis clientes"*. El resultado aparece en `output/`.
4. Mira cómo crece en la **vista de grafo** de Obsidian (Ctrl+G).

## Atajos

- [[wiki/Inicio|Índice de la wiki]]
- [[empresa/Plan de 4 semanas|Plan: cerebro de IA de empresa]]
- [[empresa/Matriz de permisos]]
- Carpeta `proyectos/` → grafos de tus proyectos de código (Graphify)
- Carpeta `output/` → lo que ha creado el agente

## Herramientas instaladas

| Herramienta | Comando | Para qué |
|---|---|---|
| Graphify | `/graphify <ruta>` (añade `--obsidian` para volcarlo aquí) | Indexa un proyecto en un grafo para no releer todo el código (ahorro de tokens) |
| Watch Video | `/watch-video <url>` | Transcribe y analiza vídeos (YouTube, Instagram, TikTok, archivos locales) |
| Find Skills | `/find-skills` | Busca e instala nuevas skills |
