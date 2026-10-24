# -*- coding: utf-8 -*-
"""Extrae las conversaciones antiguas de Claude Code de este ordenador a texto
limpio, para que la skill /importar-historial las resuma en raw/ de la bóveda.

Lee ~/.claude/projects/<proyecto>/<sesion>.jsonl y escribe una ficha .md por
conversación en una carpeta temporal FUERA de la bóveda (no se sube a GitHub).
Solo guarda lo que dijeron el usuario y Claude: ni salidas de herramientas, ni
razonamiento interno, ni avisos del sistema. Tapa claves y tokens.

Uso:
  python extraer_historial.py              # todas las pendientes
  python extraer_historial.py --dias 90    # solo las de los últimos 90 días
  python extraer_historial.py --claude-ai conversations.json   # export de claude.ai
"""
import argparse, json, os, re, socket, sys, time
from datetime import datetime, timezone
from pathlib import Path

VAULT = Path(os.environ.get("SEGUNDO_CEREBRO", Path.home() / "Documents" / "SegundoCerebro"))
PROJECTS = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")) / "projects"
OUT = Path.home() / ".cache" / "segundo-cerebro" / "historial"
ESTADO = VAULT / "scripts" / "historial_importado.json"
MAX_MSG = 1500          # caracteres por mensaje
MAX_FICHA = 40000       # caracteres por conversación
MIN_USUARIO = 2         # conversaciones con menos mensajes del usuario se ignoran

SECRETOS = [
    (re.compile(r"\b(sk-[A-Za-z0-9_-]{16,}|sk-ant-[A-Za-z0-9_-]{16,})"), "[CLAVE]"),
    (re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"), "[TOKEN]"),
    (re.compile(r"\b(AKIA|ASIA)[A-Z0-9]{16}\b"), "[CLAVE-AWS]"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{30,}"), "[CLAVE]"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), "[TOKEN]"),
    (re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), "[JWT]"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S), "[CLAVE-PRIVADA]"),
    (re.compile(r"(?i)\b(password|passwd|contraseña|pwd|secret|api[_-]?key|token)\s*[:=]\s*\S+"), r"\1: [OCULTO]"),
]
RUIDO = [
    re.compile(r"<system-reminder>.*?</system-reminder>", re.S),
    re.compile(r"<(command-[a-z-]+|local-command-[a-z-]+|task-notification|ci-monitor-event|side-sessions-event)>.*?</\1>", re.S),
    re.compile(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", re.S),
]


def limpiar(texto):
    for r in RUIDO:
        texto = r.sub("", texto)
    for r, rep in SECRETOS:
        texto = r.sub(rep, texto)
    texto = texto.strip()
    if len(texto) > MAX_MSG:
        texto = texto[:MAX_MSG] + " […]"
    return texto


def textos(contenido):
    if isinstance(contenido, str):
        return [contenido]
    return [b.get("text", "") for b in contenido or [] if isinstance(b, dict) and b.get("type") == "text"]


def leer_sesion(ruta):
    titulo, cwd, inicio, fin, msgs = None, None, None, None, []
    for linea in ruta.open(encoding="utf-8", errors="replace"):
        try:
            d = json.loads(linea)
        except ValueError:
            continue
        if d.get("type") == "custom-title":
            titulo = d.get("customTitle") or titulo
        cwd = cwd or d.get("cwd")
        if d.get("type") not in ("user", "assistant") or d.get("isSidechain"):
            continue
        ts = d.get("timestamp")
        inicio, fin = inicio or ts, ts or fin
        for t in textos((d.get("message") or {}).get("content")):
            t = limpiar(t)
            if t:
                msgs.append(("Usuario" if d["type"] == "user" else "Claude", t))
    return titulo, cwd, inicio, fin, msgs


def ficha(sid, titulo, cwd, inicio, fin, msgs, origen):
    proyecto = Path(cwd).name if cwd else "sin-proyecto"
    if "scratch-workspaces" in (cwd or ""):
        proyecto = "sin-carpeta"
    cuerpo = "\n\n".join(f"**{q}:** {t}" for q, t in msgs)
    if len(cuerpo) > MAX_FICHA:
        cuerpo = cuerpo[:MAX_FICHA // 2] + "\n\n[… parte central omitida …]\n\n" + cuerpo[-MAX_FICHA // 2:]
    cab = (f"---\nsesion: {sid}\norigen: {origen}\nordenador: {socket.gethostname()}\n"
           f"proyecto: {proyecto}\ncarpeta: {cwd or ''}\ntitulo: {titulo or ''}\n"
           f"inicio: {inicio or ''}\nfin: {fin or ''}\nmensajes: {len(msgs)}\n---\n\n")
    return proyecto, cab + f"# {titulo or 'Conversación'}\n\n" + cuerpo + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=0, help="solo conversaciones de los últimos N días")
    ap.add_argument("--claude-ai", help="ruta a conversations.json del export de claude.ai")
    ap.add_argument("--todas", action="store_true", help="incluir también las ya importadas")
    ap.add_argument("--marcar", action="store_true", help="marcar como importadas las fichas de la carpeta temporal")
    a = ap.parse_args()

    hechas = set(json.loads(ESTADO.read_text(encoding="utf-8"))) if ESTADO.exists() else set()
    if a.marcar:
        nuevas = {m.group(1) for f in OUT.glob("*.md")
                  for m in [re.search(r"^sesion: (\S+)", f.read_text(encoding="utf-8"), re.M)] if m}
        ESTADO.write_text(json.dumps(sorted(hechas | nuevas), indent=0), encoding="utf-8")
        for f in OUT.glob("*.md"):
            f.unlink()
        print(f"Marcadas {len(nuevas - hechas)} conversaciones como importadas ({len(hechas | nuevas)} en total).")
        return
    if a.todas:
        hechas = set()
    OUT.mkdir(parents=True, exist_ok=True)
    for viejo in OUT.glob("*.md"):
        viejo.unlink()
    limite = time.time() - a.dias * 86400 if a.dias else 0
    reciente = time.time() - 600  # la sesión en curso no se toca
    escritas = []

    if a.claude_ai:
        for c in json.loads(Path(a.claude_ai).read_text(encoding="utf-8")):
            sid = "web-" + c.get("uuid", "")
            if sid in hechas:
                continue
            msgs = []
            for m in c.get("chat_messages", []):
                t = limpiar(m.get("text") or " ".join(textos(m.get("content"))))
                if t:
                    msgs.append(("Usuario" if m.get("sender") == "human" else "Claude", t))
            if sum(q == "Usuario" for q, _ in msgs) < MIN_USUARIO:
                continue
            proyecto, texto = ficha(sid, c.get("name"), None, c.get("created_at"), c.get("updated_at"), msgs, "claude.ai")
            escritas.append((sid, proyecto, texto, c.get("created_at") or ""))
    else:
        for ruta in sorted(PROJECTS.glob("*/*.jsonl")):
            sid = ruta.stem
            mtime = ruta.stat().st_mtime
            if sid in hechas or mtime < limite or mtime > reciente:
                continue
            titulo, cwd, inicio, fin, msgs = leer_sesion(ruta)
            if sum(q == "Usuario" for q, _ in msgs) < MIN_USUARIO:
                continue
            if cwd and Path(cwd).resolve() == VAULT.resolve():
                continue  # las conversaciones dentro de la bóveda ya están en ella
            proyecto, texto = ficha(sid, titulo, cwd, inicio, fin, msgs, "claude-code")
            escritas.append((sid, proyecto, texto, inicio or ""))

    for sid, proyecto, texto, inicio in escritas:
        fecha = (inicio or "")[:10] or "sin-fecha"
        nombre = re.sub(r"[^\w.-]+", "_", f"{fecha}_{proyecto}_{sid[:8]}") + ".md"
        (OUT / nombre).write_text(texto, encoding="utf-8")

    print(f"Carpeta: {OUT}")
    print(f"Conversaciones nuevas: {len(escritas)} (ya importadas antes: {len(hechas)})")
    por_proyecto = {}
    for _, p, t, _ in escritas:
        por_proyecto.setdefault(p, [0, 0])
        por_proyecto[p][0] += 1
        por_proyecto[p][1] += len(t)
    for p, (n, c) in sorted(por_proyecto.items(), key=lambda x: -x[1][1]):
        print(f"  {p}: {n} conversaciones, ~{c // 4000}k tokens")


if __name__ == "__main__":
    main()
