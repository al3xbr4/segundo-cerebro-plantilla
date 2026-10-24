# Instalar el segundo cerebro en otro ordenador

Copia el prompt de tu sistema, cambia `<PLANTILLA>` por `al3xbr4/segundo-cerebro-plantilla` (o por la que te hayan pasado) y pégalo en **Claude Code**. Claude hará la instalación y te pedirá permiso para cada paso.

Requisito previo: tener Claude Code instalado y una cuenta de GitHub.

Cada persona crea **su propio repositorio privado** a partir de esta plantilla. La plantilla está vacía: tus notas solo van a tu repositorio y nadie más las ve.

---

## Prompt para Windows (ordenador de la empresa)

```text
Monta mi segundo cerebro en este ordenador Windows. Hazlo paso a paso y verifica cada cosa:

1. Si no tengo gh, instálalo con `winget install -e --id GitHub.cli` y pídeme que haga `gh auth login`. Después crea mi propio repositorio PRIVADO a partir de la plantilla y clónalo en %USERPROFILE%\Documents\SegundoCerebro: `gh repo create segundo-cerebro --private --template <PLANTILLA> --clone` desde %USERPROFILE%\Documents y renombra la carpeta a SegundoCerebro. Comprueba con `gh repo view --json visibility` que es PRIVATE.
2. Comprueba que tengo Node.js (npx), Python 3.10+ y git. Lo que falte, instálalo con winget (OpenJS.NodeJS.LTS, Python.Python.3.12, Git.Git).
3. Instala uv con `python -m pip install uv`.
4. Graphify: `python -m uv tool install graphifyy` y después `%USERPROFILE%\.local\bin\graphify install --platform claude`.
5. Skills: `npx -y skills add vercel-labs/skills@find-skills -g -a claude-code -y` y `npx -y skills add coreyhaines31/makerskills@watch-video -g -a claude-code -y`.
6. Dependencias de vídeo: `python -m uv tool install yt-dlp`, `winget install -e --id Gyan.FFmpeg`, y `python -m pip install --user faster-whisper "av==18.0.0"` (av 19 rompe faster-whisper 1.2.1).
7. Añade %USERPROFILE%\.local\bin y %LOCALAPPDATA%\Microsoft\WinGet\Links al PATH de mi usuario si no están.
8. Instala Obsidian (`winget install -e --id Obsidian.Obsidian`) y abre la bóveda con la URI obsidian://open?path=<ruta de la bóveda>.
9. Guardado y sincronización automáticos:
   - Añade al final de %USERPROFILE%\.claude\CLAUDE.md (créalo si no existe) estas dos líneas: `# Segundo cerebro` y `@~/Documents/SegundoCerebro/claude-global/REGLAS.md`.
   - Fusiona los hooks de claude-global/hooks.json de la bóveda en %USERPROFILE%\.claude\settings.json SIN borrar lo que ya haya.
   - Prueba `bash scripts/sync.sh pull` en la bóveda y revisa scripts/.sync.log.
10. Comprueba que funciona: `graphify --help`, `yt-dlp --version`, `ffmpeg -version` y `python -c "import faster_whisper"`.
11. Lee el CLAUDE.md de la bóveda y dime en qué estado está y qué hay en raw/ sin procesar.

Al acabar, recuérdame que reinicie Claude Code para que cargue las skills nuevas.
```

---

## Prompt para MacBook

```text
Monta mi segundo cerebro en este Mac. Hazlo paso a paso y verifica cada cosa:

1. Si no tengo Homebrew, dime cómo instalarlo (https://brew.sh) y espera a que lo haga.
2. Instala lo básico: `brew install git gh node python uv ffmpeg yt-dlp` y `brew install --cask obsidian`.
3. Si gh no tiene sesión, pídeme que haga `gh auth login`. Después crea mi propio repositorio PRIVADO a partir de la plantilla y clónalo en ~/Documents/SegundoCerebro: `gh repo create segundo-cerebro --private --template <PLANTILLA> --clone` desde ~/Documents y renombra la carpeta a SegundoCerebro. Comprueba con `gh repo view --json visibility` que es PRIVATE.
4. Graphify: `uv tool install graphifyy`, `uv tool update-shell` y `graphify install --platform claude`.
5. Skills: `npx -y skills add vercel-labs/skills@find-skills -g -a claude-code -y` y `npx -y skills add coreyhaines31/makerskills@watch-video -g -a claude-code -y`.
6. Transcripción local: crea un entorno con `uv venv ~/.venvs/whisper` e instala en él `faster-whisper "av==18.0.0"`. Si el Mac es Apple Silicon (M1/M2/M3/M4), instala también `mlx-whisper`, que es el que usa watch-video en esos Mac. Dime qué ruta de Python tiene que usar la skill.
7. Abre la bóveda: `open "obsidian://open?path=$HOME/Documents/SegundoCerebro"`.
8. Guardado y sincronización automáticos:
   - Añade al final de ~/.claude/CLAUDE.md (créalo si no existe) estas dos líneas: `# Segundo cerebro` y `@~/Documents/SegundoCerebro/claude-global/REGLAS.md`.
   - Fusiona los hooks de claude-global/hooks.json de la bóveda en ~/.claude/settings.json SIN borrar lo que ya haya.
   - Prueba `bash scripts/sync.sh pull` en la bóveda y revisa scripts/.sync.log.
9. Comprueba que funciona: `graphify --help`, `yt-dlp --version`, `ffmpeg -version` y que el entorno importa faster_whisper.
10. Lee el CLAUDE.md de la bóveda y dime en qué estado está y qué hay en raw/ sin procesar.

Al acabar, recuérdame que reinicie Claude Code para que cargue las skills nuevas.
```

---

## Cómo se mantiene al día solo

- **Al abrir cualquier sesión de Claude Code**, en cualquier carpeta, el hook `SessionStart` ejecuta `scripts/sync.sh pull` y trae lo que hayas guardado en otro ordenador.
- **Durante la sesión**, las reglas de `claude-global/REGLAS.md` (importadas desde `~/.claude/CLAUDE.md`) hacen que Claude consulte la wiki y guarde en `raw/` lo importante de esa conversación.
- **Al cerrar la sesión**, el hook `SessionEnd` ejecuta `scripts/sync.sh push`, que hace commit y lo sube a GitHub.
- Si algo falla (sin conexión, conflicto), no bloquea Claude Code: queda anotado en `scripts/.sync.log` y se reintenta la próxima vez.
- `raw/` no se ordena solo. Abre Claude Code en la bóveda y di «procesa raw» para pasarlo a `wiki/`.

Si editas notas directamente en Obsidian sin abrir Claude Code, puedes instalar el plugin comunitario **Git** (de Vinzent03) para que Obsidian también haga commit y push solo.

## Proyectos de código

Para indexar un proyecto de código y volcarlo en la bóveda, ejecuta dentro del proyecto `/graphify . --update` la primera vez `/graphify . --obsidian --obsidian-dir <bóveda>/proyectos/<Nombre>`, y después de cada cambio `/graphify . --update`.

## Empezar a usarlo

1. Abre Claude Code en la carpeta de la bóveda.
2. Mete material en `raw/` (notas, PDFs, transcripciones con `/watch-video <url>`) y di «procesa raw».
3. Para el cerebro de empresa, empieza por `empresa/Elegir camino.md` y `empresa/Matriz de permisos.md`.
