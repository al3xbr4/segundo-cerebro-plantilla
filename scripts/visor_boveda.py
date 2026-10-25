# -*- coding: utf-8 -*-
"""Genera cerebro.html: el grafo de la bóveda (notas y sus [[enlaces]]) con el
mismo visor que los grafos de código. Se abre con doble clic, sin servidor.

Uso:  python scripts/visor_boveda.py [--con-raw] [--con-proyectos] [--titulo "Mi cerebro"]
La rutina diaria lo regenera solo.
"""
import argparse, json, re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
PLANTILLA = Path(__file__).with_name("visor") / "plantilla.html"
CARPETAS = ["wiki", "empresa", "output"]
ENLACE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
GRUPOS = {  # tipo del frontmatter -> (orden, nombre del área)
    "proyecto": (0, "Proyectos"), "persona": (1, "Personas y empresas"), "concepto": (2, "Conceptos"),
    "herramienta": (3, "Herramientas"), "output": (4, "Lo que ha creado la IA"), "plantilla": (5, "Plantillas"),
    "fuente": (6, "Fuentes (raw)"), "indice": (7, "Índices"), "otro": (8, "Otras notas"),
}


def frontmatter(texto):
    m = re.match(r"^---\n(.*?)\n---\n?", texto, re.S)
    if not m:
        return {}, texto
    datos = {}
    for linea in m.group(1).splitlines():
        if ":" in linea and not linea.startswith(" "):
            k, v = linea.split(":", 1)
            datos[k.strip()] = v.strip()
    return datos, texto[m.end():]


def resumen(cuerpo):
    for bloque in re.split(r"\n\s*\n", cuerpo):
        b = bloque.strip()
        if b and not b.startswith(("#", "|", "```", "-", ">", "<")):
            b = ENLACE.sub(lambda m: m.group(1).split("/")[-1], b)
            b = re.sub(r"[*_`]", "", b)
            return b[:400] + ("…" if len(b) > 400 else "")
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--con-raw", action="store_true", help="incluir las notas de raw/")
    ap.add_argument("--con-proyectos", action="store_true", help="incluir los grafos de código de proyectos/ (muchos nodos)")
    ap.add_argument("--titulo", default="Segundo cerebro")
    ap.add_argument("--salida", default=str(VAULT / "cerebro.html"))
    a = ap.parse_args()

    carpetas = CARPETAS + (["raw"] if a.con_raw else []) + (["proyectos"] if a.con_proyectos else [])
    archivos = [p for c in carpetas for p in sorted((VAULT / c).rglob("*.md"))]
    archivos += [p for p in [VAULT / "Inicio.md"] if p.exists()]
    archivos = [p for p in archivos if p.name != "README.md" and "subagentes" not in p.parts]

    notas, por_nombre = {}, {}
    for p in archivos:
        rel = p.relative_to(VAULT).with_suffix("").as_posix()
        fm, cuerpo = frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        tipo = fm.get("tipo", "").split("|")[0].strip().lower()
        if p.stem == "Inicio":
            tipo = "indice"
        elif rel.startswith("raw/"):
            tipo = "fuente"
        elif rel.startswith("output/"):
            tipo = "output"
        elif tipo not in GRUPOS:
            tipo = "plantilla" if "Plantilla" in p.stem else "otro"
        titulo = re.search(r"^# (.+)$", cuerpo, re.M)
        notas[rel] = {"id": rel, "label": titulo.group(1).strip() if titulo else p.stem, "file_type": tipo,
                      "community": GRUPOS[tipo][0], "community_name": GRUPOS[tipo][1],
                      "source_file": p.relative_to(VAULT).as_posix(), "resumen": resumen(cuerpo),
                      "_texto": cuerpo + "\n" + fm.get("fuentes", "")}
        por_nombre.setdefault(p.stem.lower(), rel)
        por_nombre[rel.lower()] = rel

    enlaces, vistos = [], set()
    for rel, n in notas.items():
        for m in ENLACE.finditer(n.pop("_texto")):
            destino = m.group(1).strip().removesuffix(".md")
            dst = por_nombre.get(destino.lower()) or por_nombre.get(destino.split("/")[-1].lower())
            if dst and dst != rel and (rel, dst) not in vistos and (dst, rel) not in vistos:
                vistos.add((rel, dst))
                enlaces.append({"source": rel, "target": dst, "relation": "references", "confidence": "EXTRACTED"})

    datos = {"titulo": a.titulo, "nodes": list(notas.values()), "links": enlaces, "hyperedges": []}
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA.read_text(encoding="utf-8")
    html = html.replace("/*__DATOS__*/null", js).replace("__TITULO__", a.titulo.replace("<", "&lt;"))
    Path(a.salida).write_text(html, encoding="utf-8")
    print(f"Cerebro: {a.salida}  ({len(notas)} notas, {len(enlaces)} enlaces)")


if __name__ == "__main__":
    main()
