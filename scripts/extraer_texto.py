# -*- coding: utf-8 -*-
"""Saca el texto de un documento para que el agente lo resuma en la bóveda.

Uso:  python scripts/extraer_texto.py <archivo> [--max 60000]
Formatos: .docx .pptx .xlsx (sin librerías extra), .pdf (con pypdf si está
instalado), .txt .md .csv .json .html. Las imágenes y los PDF escaneados no
tienen texto: el agente debe mirarlos directamente.
"""
import argparse, html, re, sys, zipfile
from pathlib import Path


def xml_texto(xml, etiqueta_parrafo):
    xml = re.sub(rf"</{etiqueta_parrafo}>", "\n", xml)
    xml = re.sub(r"<w:tab/>|<a:tab/>", "\t", xml)
    return html.unescape(re.sub(r"<[^>]+>", "", xml))


def docx(p):
    with zipfile.ZipFile(p) as z:
        return xml_texto(z.read("word/document.xml").decode("utf-8", "replace"), "w:p")


def pptx(p):
    with zipfile.ZipFile(p) as z:
        nombres = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                         key=lambda n: int(re.findall(r"\d+", n)[-1]))
        return "\n\n".join(f"--- Diapositiva {i} ---\n" + xml_texto(z.read(n).decode("utf-8", "replace"), "a:p")
                           for i, n in enumerate(nombres, 1))


def xlsx(p):
    with zipfile.ZipFile(p) as z:
        compartidas = []
        if "xl/sharedStrings.xml" in z.namelist():
            sx = z.read("xl/sharedStrings.xml").decode("utf-8", "replace")
            compartidas = [html.unescape(re.sub(r"<[^>]+>", "", si)) for si in re.findall(r"<si>(.*?)</si>", sx, re.S)]
        salida = []
        for n in sorted(x for x in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", x)):
            salida.append(f"--- {Path(n).stem} ---")
            for fila in re.findall(r"<row[^>]*>(.*?)</row>", z.read(n).decode("utf-8", "replace"), re.S):
                celdas = []
                for attrs, valor in re.findall(r"<c([^>]*)>(?:.*?<v>(.*?)</v>)?.*?</c>", fila, re.S):
                    if 't="s"' in attrs and valor.isdigit() and int(valor) < len(compartidas):
                        valor = compartidas[int(valor)]
                    celdas.append(html.unescape(valor or ""))
                salida.append("\t".join(celdas))
        return "\n".join(salida)


def pdf(p):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    return "\n\n".join(f"--- Página {i} ---\n{pg.extract_text() or ''}" for i, pg in enumerate(PdfReader(str(p)).pages, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("--max", type=int, default=60000, help="caracteres como máximo")
    a = ap.parse_args()
    p = Path(a.archivo)
    ext = p.suffix.lower()
    lectores = {".docx": docx, ".pptx": pptx, ".xlsx": xlsx, ".pdf": pdf}
    if ext in lectores:
        texto = lectores[ext](p)
        if texto is None:
            print(f"[Sin pypdf: lee {p.name} directamente con tu herramienta de lectura de PDF]")
            return
    elif ext in (".txt", ".md", ".csv", ".json", ".html", ".htm", ".xml", ".log"):
        texto = p.read_text(encoding="utf-8", errors="replace")
        if ext in (".html", ".htm"):
            texto = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", texto)))
    else:
        print(f"[{ext or 'sin extensión'}: no tiene texto extraíble; si es una imagen, mírala directamente]")
        return
    texto = re.sub(r"\n{3,}", "\n\n", texto).strip()
    if not texto:
        print("[Sin texto: probablemente es un PDF escaneado; míralo directamente]")
        return
    if len(texto) > a.max:
        texto = texto[:a.max] + f"\n\n[… recortado: {len(texto) - a.max} caracteres más. Vuelve a ejecutar con --max mayor si hace falta]"
    sys.stdout.reconfigure(encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
