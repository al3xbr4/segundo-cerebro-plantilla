# -*- coding: utf-8 -*-
"""Genera grafo.html, un visor del grafo de Graphify más cómodo que graph.html.

Uso:  python visor_grafo.py <carpeta graphify-out> [--titulo "Nombre"]
Mete graph.json dentro del HTML, así que se abre con doble clic, sin servidor.
Vuelve a ejecutarlo después de cada `/graphify . --update`.
"""
import argparse, json
from pathlib import Path

PLANTILLA = Path(__file__).with_name("visor") / "plantilla.html"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("salida", nargs="?", default="graphify-out", help="carpeta graphify-out")
    ap.add_argument("--titulo", help="nombre que sale arriba (por defecto, la carpeta del proyecto)")
    a = ap.parse_args()

    out = Path(a.salida).resolve()
    grafo = json.loads((out / "graph.json").read_text(encoding="utf-8"))
    raiz = out / ".graphify_root"
    titulo = a.titulo or (Path(raiz.read_text(encoding="utf-8").strip()).name if raiz.exists() else out.parent.name)
    datos = {
        "titulo": titulo,
        "nodes": grafo.get("nodes", []),
        "links": grafo.get("links") or grafo.get("edges") or [],
        "hyperedges": grafo.get("hyperedges", []),
    }
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA.read_text(encoding="utf-8")
    html = html.replace("/*__DATOS__*/null", js).replace("__TITULO__", titulo.replace("<", "&lt;"))
    destino = out / "grafo.html"
    destino.write_text(html, encoding="utf-8")
    print(f"Visor: {destino}  ({len(datos['nodes'])} nodos, {len(datos['links'])} relaciones)")


if __name__ == "__main__":
    main()
