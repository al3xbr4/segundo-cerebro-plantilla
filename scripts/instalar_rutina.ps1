# Programa la rutina del segundo cerebro en Windows (Programador de tareas).
#   powershell -ExecutionPolicy Bypass -File scripts\instalar_rutina.ps1 [-Hora 21:00] [-SyncCada15Min]
# -SyncCada15Min: para Codex u otros agentes sin hooks; Claude Code ya sincroniza con sus hooks.
# Si el ordenador está apagado a esa hora, la rutina se ejecuta al encenderlo.
param([string]$Hora = "21:00", [switch]$SyncCada15Min, [switch]$Quitar)

$vault = Join-Path $env:USERPROFILE "Documents\SegundoCerebro"
$git = (Get-Command git -ErrorAction Stop).Source
$bash = Join-Path (Split-Path (Split-Path $git)) "bin\bash.exe"
if (-not (Test-Path $bash)) { throw "No encuentro bash de Git en $bash" }

if ($Quitar) {
  Unregister-ScheduledTask -TaskName "SegundoCerebro-Rutina" -Confirm:$false -ErrorAction SilentlyContinue
  Unregister-ScheduledTask -TaskName "SegundoCerebro-Sync" -Confirm:$false -ErrorAction SilentlyContinue
  "Tareas quitadas."; return
}

$ajustes = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 2)
$accion = New-ScheduledTaskAction -Execute $bash -Argument "-lc `"bash ~/Documents/SegundoCerebro/scripts/rutina.sh`"" -WorkingDirectory $vault
$disparo = New-ScheduledTaskTrigger -Daily -At $Hora
Register-ScheduledTask -TaskName "SegundoCerebro-Rutina" -Action $accion -Trigger $disparo -Settings $ajustes `
  -Description "Segundo cerebro: grafos, historial nuevo y procesar raw (scripts/rutina.sh)" -Force | Out-Null
"Rutina diaria programada a las $Hora."

if ($SyncCada15Min) {
  $accionSync = New-ScheduledTaskAction -Execute $bash -Argument "-lc `"bash ~/Documents/SegundoCerebro/scripts/sync.sh ciclo`"" -WorkingDirectory $vault
  $cada15 = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15)
  Register-ScheduledTask -TaskName "SegundoCerebro-Sync" -Action $accionSync -Trigger $cada15 -Settings $ajustes `
    -Description "Segundo cerebro: sincronizar con GitHub (scripts/sync.sh ciclo)" -Force | Out-Null
  "Sincronización cada 15 minutos programada."
}
