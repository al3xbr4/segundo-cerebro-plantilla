#!/usr/bin/env bash
# Sincroniza la bóveda con GitHub. Lo llaman los hooks de Claude Code:
#   sync.sh pull  -> al empezar una sesión (trae lo de otros ordenadores)
#   sync.sh push  -> al terminar una sesión (sube lo nuevo)
# Nunca bloquea a Claude Code: si algo falla (sin red, conflicto), lo deja en
# scripts/.sync.log y sale con 0.
VAULT="${SEGUNDO_CEREBRO:-$HOME/Documents/SegundoCerebro}"
LOG="$VAULT/scripts/.sync.log"
cd "$VAULT" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
log() { printf '%s %s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2" >> "$LOG"; }

case "$1" in
  pull)
    if out=$(git pull --rebase --autostash -q 2>&1); then log pull ok; else log pull "FALLO: $out"; fi
    ;;
  push)
    git add -A
    if ! git diff --cached --quiet; then
      git commit -q -m "Notas $(date '+%Y-%m-%d %H:%M') ($(hostname))" || log push "FALLO commit"
    fi
    if [ -n "$(git log '@{u}..' --oneline 2>/dev/null)" ]; then
      git pull --rebase --autostash -q >/dev/null 2>&1
      if out=$(git push -q 2>&1); then log push ok; else log push "FALLO: $out"; fi
    fi
    ;;
esac
exit 0
