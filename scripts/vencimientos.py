# -*- coding: utf-8 -*-
"""Genera wiki/Vencimientos.md a partir de las fichas de documentos administrativos
(campos `vence`, `preaviso_dias`, `categoria`, `contraparte`… del frontmatter).

Uso:  python scripts/vencimientos.py [--hoy AAAA-MM-DD]
La rutina diaria lo ejecuta solo. También imprime lo urgente (para el registro).
"""
import argparse, re
from datetime import date, timedelta
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SALIDA = VAULT / "wiki" / "Vencimientos.md"


def frontmatter(p):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", p.read_text(encoding="utf-8", errors="replace"), re.S)
    datos = {}
    for linea in (m.group(1).splitlines() if m else []):
        if ":" in linea and not linea.startswith((" ", "-")):
            k, v = linea.split(":", 1)
            datos[k.strip()] = v.strip().strip('"').strip("'")
    return datos


def fecha(texto):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", texto or "")
    return date(*map(int, m.groups())) if m else None


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoy", help="fecha de referencia (para pruebas)")
    a = ap.parse_args()
    hoy = fecha(a.hoy) if a.hoy else date.today()

    filas = []
    for p in sorted((VAULT / "raw").rglob("*.md")):
        fm = frontmatter(p)
        vence = fecha(fm.get("vence"))
        if not vence:
            continue
        preaviso = int(re.sub(r"\D", "", fm.get("preaviso_dias", "")) or 0)
        limite = vence - timedelta(days=preaviso) if preaviso else None
        clave = limite or vence
        dias = (clave - hoy).days
        estado = ("🔴 Vencido" if (vence - hoy).days < 0 else "🔴 Avisar ya" if dias < 0 else
                  "🟠 ≤ 30 días" if dias <= 30 else "🟡 ≤ 90 días" if dias <= 90 else "🟢 Más adelante")
        enlace = f"[[{p.relative_to(VAULT).with_suffix('').as_posix()}|{p.stem.removesuffix('.pdf').removesuffix('.docx')}]]"
        filas.append({"estado": estado, "orden": clave, "vence": vence, "limite": limite, "dias": dias,
                      "categoria": fm.get("categoria", ""), "ambito": fm.get("ambito", ""), "area": fm.get("area", ""),
                      "contraparte": fm.get("contraparte", ""), "importe": fm.get("importe", ""),
                      "renovacion": fm.get("renovacion", ""), "ficha": enlace})
    filas.sort(key=lambda f: f["orden"])

    def tabla(xs):
        if not xs:
            return "_Nada._\n"
        cab = "| Estado | Vence | Avisar antes de | Qué | Contraparte | Importe | Renovación | Ámbito | Ficha |\n|---|---|---|---|---|---|---|---|---|\n"
        return cab + "".join(
            f"| {f['estado']} | {f['vence']} | {f['limite'] or '—'} | {f['categoria']} | {f['contraparte']} | {f['importe']} | "
            f"{f['renovacion']} | {f['ambito']}{(' · ' + f['area']) if f['area'] else ''} | {f['ficha']} |\n" for f in xs)

    urgentes = [f for f in filas if f["dias"] <= 30]
    texto = (f"---\ntipo: indice\nactualizado: {hoy}\n---\n\n# Vencimientos\n\n"
             f"Generado por `scripts/vencimientos.py` a partir de las fichas de documentos ({len(filas)} con fecha de vencimiento). "
             "No lo edites a mano: se rehace cada día. Para corregir un dato, cambia la ficha.\n\n"
             f"## Urgente (vencido o en los próximos 30 días)\n\n{tabla(urgentes)}\n"
             f"## Próximos 90 días\n\n{tabla([f for f in filas if 30 < f['dias'] <= 90])}\n"
             f"## Todo\n\n{tabla(filas)}")
    SALIDA.parent.mkdir(exist_ok=True)
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"Vencimientos: {len(filas)} documentos, {len(urgentes)} urgentes → {SALIDA.relative_to(VAULT)}")
    for f in urgentes:
        print(f"  {f['estado']}: {f['categoria']} {f['contraparte']} (vence {f['vence']}"
              f"{', avisar antes de ' + str(f['limite']) if f['limite'] else ''})")


if __name__ == "__main__":
    main()
