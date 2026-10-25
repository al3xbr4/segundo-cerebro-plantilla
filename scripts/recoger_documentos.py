# -*- coding: utf-8 -*-
"""Busca en las conversaciones de Claude Code y Codex de este ordenador los
documentos que se han mencionado (rutas a PDF, Word, Excel, PowerPoint) y copia
a raw/documentos/ los que todavía existen, para que entren en el cerebro.
Los originales no se tocan.

Uso:
  python scripts/recoger_documentos.py            # solo lista lo que encuentra
  python scripts/recoger_documentos.py --copiar   # copia los nuevos a raw/documentos/
"""
import argparse, json, os, re, shutil
from pathlib import Path

HOME = Path.home()
VAULT = Path(os.environ.get("SEGUNDO_CEREBRO", HOME / "Documents" / "SegundoCerebro"))
DESTINO = VAULT / "raw" / "documentos"
ESTADO = VAULT / "scripts" / "documentos_recogidos.json"
FUENTES = [Path(os.environ.get("CLAUDE_CONFIG_DIR", HOME / ".claude")) / "projects",
           Path(os.environ.get("CODEX_HOME", HOME / ".codex")) / "sessions"]
EXT = ("pdf", "docx", "xlsx", "pptx", "doc", "xls", "ppt")
MAX_MB = 50  # GitHub no admite archivos de más de 100 MB; con 50 hay margen
# Rutas de Windows (C:\...\x.pdf) y de Mac/Linux (/Users/.../x.pdf); admite espacios dentro de una carpeta
RAIZ = r"[A-Za-z]:[\\/]" if os.name == "nt" else r"/(?:Users|home|Volumes)/"
RUTA = re.compile(r"(?<![A-Za-z0-9])((?:%s)[^\"'`<>|*?\n\r\t{}\[\]]{1,240}?\.(?:%s))(?![A-Za-z0-9])" % (RAIZ, "|".join(EXT)), re.I)


def textos(obj):
    """Todas las cadenas de un JSON, ya descodificadas (saltos de línea reales, barras simples)."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from textos(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from textos(v)


def rutas_en_conversaciones():
    encontradas = {}
    for base in FUENTES:
        if not base.exists():
            continue
        for f in base.rglob("*.jsonl"):
            for linea in f.open(encoding="utf-8", errors="replace"):
                if not any(e in linea.lower() for e in (".pdf", ".doc", ".xls", ".ppt")):
                    continue
                try:
                    cadenas = textos(json.loads(linea))
                except ValueError:
                    continue
                for texto in cadenas:
                    for m in RUTA.findall(texto):
                        ruta = m.strip().lstrip("@").strip()
                        # dos rutas seguidas en la misma línea: quedarse con la última
                        ruta = re.split(r"\s(?=[A-Za-z]:[\\/])", ruta)[-1]
                        encontradas.setdefault(os.path.normcase(os.path.normpath(ruta)), os.path.normpath(ruta))
    return sorted(encontradas.values(), key=str.lower)


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--copiar", action="store_true", help="copiar a raw/documentos/ los que existan y no estén ya")
    a = ap.parse_args()
    hechos = set(json.loads(ESTADO.read_text(encoding="utf-8"))) if ESTADO.exists() else set()
    copiados = perdidos = 0
    for ruta in rutas_en_conversaciones():
        p = Path(ruta)
        dentro = VAULT in p.parents
        if not p.is_file():
            perdidos += 1  # ya no está, o era un ejemplo o un enlace web
            continue
        elif dentro:
            estado = "ya en la bóveda"
        elif os.path.normcase(str(p)) in hechos:
            estado = "ya recogido"
        elif p.stat().st_size > MAX_MB * 1e6:
            estado = f"demasiado grande ({p.stat().st_size / 1e6:.0f} MB)"
        else:
            estado = "nuevo"
            if a.copiar:
                DESTINO.mkdir(parents=True, exist_ok=True)
                destino = DESTINO / p.name
                n = 2
                while destino.exists():
                    destino = DESTINO / f"{p.stem} ({n}){p.suffix}"; n += 1
                shutil.copy2(p, destino)
                hechos.add(os.path.normcase(str(p)))
                copiados += 1
                estado = f"copiado → raw/documentos/{destino.name}"
        print(f"[{estado}] {ruta}")
    print(f"\n({perdidos} rutas mencionadas que ya no existen o no son archivos locales)")
    if a.copiar:
        ESTADO.write_text(json.dumps(sorted(hechos), indent=0, ensure_ascii=False), encoding="utf-8")
        print(f"\nCopiados: {copiados}. Di «procesa raw» (o espera a la rutina) para hacerles la ficha.")


if __name__ == "__main__":
    main()
