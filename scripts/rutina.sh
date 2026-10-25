#!/usr/bin/env bash
# Rutina diaria del segundo cerebro. La lanza el programador de tareas del
# sistema (ver instalar_rutina.ps1 / instalar_rutina.sh), sin nadie delante:
#   1. trae la bóveda de GitHub (si hay repositorio remoto)
#   2. actualiza los grafos de los proyectos de código de este ordenador (sin IA)
#   3. con el agente (Claude Code o Codex): importa conversaciones nuevas y procesa raw/ -> wiki/
#   4. sube la bóveda a GitHub
# Configuración local, que no se sube (está en .gitignore):
#   scripts/agente.local     -> "claude" o "codex" (si no existe, se detecta)
#   scripts/proyectos.local  -> una línea por proyecto:  ruta|Nombre
VAULT="${SEGUNDO_CEREBRO:-$HOME/Documents/SegundoCerebro}"
LOG="$VAULT/scripts/.rutina.log"
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
cd "$VAULT" || exit 0
exec >>"$LOG" 2>&1
echo "===== $(date '+%Y-%m-%d %H:%M:%S') rutina en $(hostname) ====="
PY=$(command -v python || command -v python3)

bash scripts/sync.sh pull

# 2. Grafos de código: graphify update re-extrae el código por AST, sin IA ni coste
if [ -f scripts/proyectos.local ]; then
  while IFS='|' read -r ruta nombre; do
    ruta="${ruta%$'\r'}"; nombre="${nombre%$'\r'}"
    case "$ruta" in ''|\#*) continue ;; esac
    [ -d "$ruta" ] || { echo "grafo: no existe $ruta"; continue; }
    nombre="${nombre:-$(basename "$ruta")}"
    echo "grafo: $nombre"
    # En Windows, desde el programador de tareas bash no arranca bien graphify.exe: se lanza con cmd
    if command -v cmd.exe >/dev/null 2>&1; then GRAPHIFY=(cmd.exe //c graphify); else GRAPHIFY=(graphify); fi
    ( cd "$ruta" && "${GRAPHIFY[@]}" update . \
      && "${GRAPHIFY[@]}" export obsidian --dir "$VAULT/proyectos/$nombre" \
      && rm -rf "$VAULT/proyectos/$nombre/.obsidian" \
      && "$PY" "$VAULT/scripts/visor_grafo.py" graphify-out --titulo "$nombre" ) || echo "grafo: FALLO en $nombre"
  done < scripts/proyectos.local
fi

# 3. Historial nuevo + procesar raw, con el agente en modo no interactivo
AGENTE=$(tr -d '[:space:]' < scripts/agente.local 2>/dev/null)
[ -z "$AGENTE" ] && { command -v claude >/dev/null && AGENTE=claude || { command -v codex >/dev/null && AGENTE=codex; }; }
PROMPT='Rutina automática del segundo cerebro. No hay nadie delante: no hagas preguntas y no escribas ninguna nota sobre esta rutina. Sigue el AGENTS.md de esta bóveda.
1. Ejecuta `python scripts/extraer_historial.py --dias 14 --max-tokens 250000`. Si hay fichas nuevas, resúmelas en raw/ con el procedimiento «Importa mi historial» y después ejecuta `python scripts/extraer_historial.py --marcar`.
2. Procesa raw: pasa a wiki/ las notas de raw/ que no tengan procesado: true, con el procedimiento «Procesa raw».
3. No modifiques nada fuera de esta carpeta y no ejecutes git.
Termina con un resumen de 5 líneas como máximo.'
case "$AGENTE" in
  claude)
    claude -p "$PROMPT" --permission-mode acceptEdits \
      --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Agent" \
      "Bash(python scripts/extraer_historial.py:*)" "Bash(python3 scripts/extraer_historial.py:*)" ;;
  codex)
    codex exec --full-auto -C "$VAULT" "$PROMPT" ;;
  *)
    echo "agente: no encuentro claude ni codex; me salto el historial y raw/" ;;
esac

# 4. Visor del cerebro entero (cerebro.html); el título se puede poner en scripts/titulo.local
TITULO=$(tr -d '\r' < scripts/titulo.local 2>/dev/null); "$PY" scripts/visor_boveda.py --con-raw --titulo "${TITULO:-Segundo cerebro}"

bash scripts/sync.sh push
echo "===== fin $(date '+%H:%M:%S') ====="
exit 0
