#!/usr/bin/env bash
# Programa la rutina del segundo cerebro en macOS (launchd).
#   bash scripts/instalar_rutina.sh [HH:MM] [--sync]   (por defecto 21:00)
#   bash scripts/instalar_rutina.sh --quitar
# --sync: sincroniza cada 15 minutos (para Codex u otros agentes sin hooks).
# Si el Mac estaba dormido a esa hora, launchd la lanza al despertar.
set -e
DIR="$HOME/Library/LaunchAgents"; mkdir -p "$DIR"
R="$DIR/com.segundocerebro.rutina.plist"; S="$DIR/com.segundocerebro.sync.plist"

if [ "$1" = "--quitar" ]; then
  launchctl unload "$R" "$S" 2>/dev/null || true; rm -f "$R" "$S"; echo "Tareas quitadas."; exit 0
fi
HORA="${1:-21:00}"; [ "$HORA" = "--sync" ] && HORA="21:00"
H=$((10#${HORA%%:*})); M=$((10#${HORA##*:}))

cat > "$R" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.segundocerebro.rutina</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>-lc</string><string>bash "\$HOME/Documents/SegundoCerebro/scripts/rutina.sh"</string></array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>$H</integer><key>Minute</key><integer>$M</integer></dict>
</dict></plist>
EOF
launchctl unload "$R" 2>/dev/null || true; launchctl load "$R"
echo "Rutina diaria programada a las $HORA."

if [[ " $* " == *" --sync "* ]]; then
  cat > "$S" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.segundocerebro.sync</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>-lc</string><string>bash "\$HOME/Documents/SegundoCerebro/scripts/sync.sh" ciclo</string></array>
  <key>StartInterval</key><integer>900</integer>
</dict></plist>
EOF
  launchctl unload "$S" 2>/dev/null || true; launchctl load "$S"
  echo "Sincronización cada 15 minutos programada."
fi
