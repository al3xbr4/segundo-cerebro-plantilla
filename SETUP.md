# Instalar el segundo cerebro

Copia el prompt de abajo y pégalo tal cual en tu agente: **Codex** o **Claude Code**. Él hace la instalación y te pide permiso en cada paso. Sirve para Windows y para Mac.

- **Con cuenta de GitHub:** se crea tu propio repositorio **privado** a partir de esta plantilla y la bóveda se sincroniza entre tus ordenadores.
- **Sin cuenta de GitHub:** todo se queda en tu ordenador, con historial local.

La plantilla está vacía: tus notas solo van a tu ordenador o a tu repositorio privado, y nadie más las ve.

---

## Prompt de instalación

```text
Monta mi "segundo cerebro": una bóveda de Obsidian que tú uses como memoria en todas mis conversaciones. Plantilla: https://github.com/al3xbr4/segundo-cerebro-plantilla
Hazlo paso a paso, pídeme permiso cuando haga falta y comprueba cada cosa.

0. Detecta: mi sistema (Windows o Mac), qué agente eres (Codex o Claude Code) y si tengo `gh` con sesión de GitHub iniciada. Dímelo antes de seguir.
1. Básicos que falten: git, Node.js (npx), Python 3.10+ y uv. Windows: winget (Git.Git, OpenJS.NodeJS.LTS, Python.Python.3.12) y `python -m pip install uv`. En Windows, define además la variable de usuario `UV_TOOL_DIR=%USERPROFILE%\.uv	ools` antes de instalar herramientas con uv: si el agente es una app de escritorio, lo que instale en AppData puede quedar aislado y la rutina programada no lo vería. Mac: Homebrew (`brew install git node python uv`; si no tengo Homebrew, dime cómo instalarlo y espera).
2. La bóveda, en Documentos/SegundoCerebro:
   - Con GitHub: `gh repo create segundo-cerebro --private --template al3xbr4/segundo-cerebro-plantilla --clone` desde Documentos, renombra la carpeta a SegundoCerebro y comprueba con `gh repo view --json visibility` que es PRIVATE.
   - Sin GitHub: `git clone https://github.com/al3xbr4/segundo-cerebro-plantilla.git SegundoCerebro`, borra su carpeta .git y haz `git init` con un primer commit.
3. Lee el AGENTS.md de la bóveda: son las reglas de funcionamiento.
4. Memoria en todas las conversaciones:
   - Codex: copia el contenido de global/REGLAS.md al final de ~/.codex/AGENTS.md (créalo si no existe, sin borrar nada). Añade la ruta de la bóveda a `writable_roots` en [sandbox_workspace_write] de ~/.codex/config.toml, para poder guardar notas trabajando en otras carpetas; si mi versión no tiene esa opción, dímelo.
   - Claude Code: añade al final de ~/.claude/CLAUDE.md las líneas `# Segundo cerebro` y `@~/Documents/SegundoCerebro/global/REGLAS.md`. Si hay GitHub, fusiona global/hooks-claude.json en ~/.claude/settings.json (sin borrar nada). Pon también `"cleanupPeriodDays": 365` para no perder conversaciones.
5. Skills (con `-a codex` o `-a claude-code`, según el agente): `npx -y skills add vercel-labs/skills@find-skills -g -a <agente> -y` y `npx -y skills add coreyhaines31/makerskills@watch-video -g -a <agente> -y`.
6. Graphify: `uv tool install graphifyy` (Windows: `python -m uv tool install graphifyy`) y `graphify install --platform <codex|claude>`. Comprueba que ~/.local/bin está en el PATH.
7. Vídeo: `uv tool install yt-dlp`; ffmpeg (Windows: `winget install -e --id Gyan.FFmpeg`, Mac: `brew install ffmpeg`); Whisper local: `faster-whisper` con `av==18.0.0` (la 19 da error). En un Mac M1 o posterior, añade `mlx-whisper`.
8. Obsidian: Windows `winget install -e --id Obsidian.Obsidian`, Mac `brew install --cask obsidian`. Ábrelo con obsidian://open?path=<ruta de la bóveda>.
9. Rutina diaria (actualiza grafos, importa conversaciones nuevas y ordena raw/ → wiki/):
   - Escribe en scripts/agente.local la palabra `codex` o `claude`.
   - Pregúntame qué proyectos de código quiero vigilar y apúntalos en scripts/proyectos.local, uno por línea, como `ruta|Nombre`.
   - Windows: `powershell -ExecutionPolicy Bypass -File scripts\instalar_rutina.ps1 -Hora 21:00`. Mac: `bash scripts/instalar_rutina.sh 21:00`. Si uso Codex y hay GitHub, añade `-SyncCada15Min` (Windows) o `--sync` (Mac).
10. Historial: ejecuta `python scripts/extraer_historial.py`, enséñame cuántas conversaciones antiguas tengo por proyecto y, si te digo que sí, sigue el procedimiento «Importa mi historial» de AGENTS.md.
11. Comprueba que todo funciona (`graphify --help`, `yt-dlp --version`, `ffmpeg -version`, `python -c "import faster_whisper"`) y explícame en 5 líneas cómo usarlo en el día a día. Recuérdame reiniciar el agente para que cargue las skills.
```

---

## Cómo se mantiene al día

| Qué | Cuándo | Cómo |
|---|---|---|
| Consultar la wiki y guardar lo importante en `raw/` | En cada conversación | Reglas globales (`global/REGLAS.md`) |
| Sincronizar con GitHub | Al abrir y cerrar sesión (Claude Code) o cada 15 min (Codex) | `scripts/sync.sh` |
| Actualizar grafos de código | Cada día | Rutina: `graphify update`, sin IA |
| Importar conversaciones nuevas | Cada día | Rutina: `extraer_historial.py` + el agente |
| Pasar `raw/` a `wiki/` | Cada día | Rutina: el agente en modo automático |

Lo que hace la rutina queda en `scripts/.rutina.log`, y los fallos de sincronización en `scripts/.sync.log`. Para quitarla: `instalar_rutina.ps1 -Quitar` o `instalar_rutina.sh --quitar`.

La rutina usa tu agente en modo automático, así que consume de tu plan o tu cuota cada día. Si no hay nada nuevo, apenas gasta.

## Proyectos de código

Dentro del proyecto, la primera vez: `/graphify . --obsidian --obsidian-dir <bóveda>/proyectos/<Nombre>` y `python <bóveda>/scripts/visor_grafo.py graphify-out`, que genera `grafo.html`, un visor del grafo que se abre con doble clic. Después, añade el proyecto a `scripts/proyectos.local` y la rutina lo mantendrá al día.

## Conversaciones de claude.ai

`python scripts/extraer_historial.py --claude-ai <ruta>/conversations.json` (el archivo sale de Ajustes → Privacidad → Exportar datos).
