"""Gera, lê e junta PDFs.
Uso:
  uv run --with pypdf --with reportlab pdf.py ler arquivo.pdf
  uv run --with pypdf --with reportlab pdf.py exemplo saida.pdf
  uv run --with pypdf --with reportlab pdf.py criar saida.pdf conteudo.json
  uv run --with pypdf --with reportlab pdf.py juntar saida.pdf a.pdf b.pdf ...
conteudo.json: {"titulo": "...", "paragrafos": ["texto", "texto"]}
"""
import json, sys
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def criar(destino, dados):
    est = getSampleStyleSheet()
    cont = [Paragraph(dados.get("titulo", "Documento"), est["Title"]), Spacer(1, 12)]
    for p in dados.get("paragrafos", []):
        cont += [Paragraph(p, est["BodyText"]), Spacer(1, 8)]
    SimpleDocTemplate(destino, pagesize=A4).build(cont)


def ler(caminho):
    r = PdfReader(caminho)
    print(f"{len(r.pages)} página(s)")
    for n, pg in enumerate(r.pages, 1):
        print(f"--- página {n} ---"); print(pg.extract_text())


def juntar(destino, entradas):
    w = PdfWriter()
    for e in entradas:
        for pg in PdfReader(e).pages: w.add_page(pg)
    w.write(destino)


EXEMPLO = {"titulo": "Relatório de exemplo", "paragrafos": ["Primeiro parágrafo com acentuação: ação, coração.", "Segundo parágrafo."]}

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    cmd, arq = sys.argv[1], sys.argv[2]
    if cmd == "ler": ler(arq)
    elif cmd == "exemplo": criar(arq, EXEMPLO)
    elif cmd == "criar": criar(arq, json.load(open(sys.argv[3], encoding="utf-8")))
    elif cmd == "juntar": juntar(arq, sys.argv[3:])
    else: sys.exit(__doc__)
