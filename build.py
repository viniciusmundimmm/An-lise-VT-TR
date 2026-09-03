#!/usr/bin/env python3
"""Gera a versão autônoma do comparador, com a biblioteca de leitura embutida.

    python3 build.py

Lê index.html (que carrega o SheetJS por CDN) e escreve
dist/comparador-psvt-offline.html, um único arquivo que roda sem internet.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "index.html"
LIB = ROOT / "vendor" / "xlsx.full.min.js"
OUT = ROOT / "dist" / "comparador-psvt-offline.html"

CDN = re.compile(r'<script src="https://cdnjs\.cloudflare\.com/[^"]*xlsx[^"]*"></script>')
FONTS = re.compile(r'\s*<link rel="(?:preconnect|stylesheet)" href="https://fonts\.[^"]*"[^>]*>')

def main():
    html = SRC.read_text(encoding="utf-8")
    lib = LIB.read_text(encoding="utf-8")

    # A tag </script> não ocorre no bundle, então a inclusão literal é segura.
    if "</script" in lib.lower():
        sys.exit("o bundle contém </script> e não pode ser embutido literalmente")

    inline = (
        "<script>\n"
        "/* SheetJS (xlsx) 0.18.5 — Apache-2.0 — https://sheetjs.com\n"
        "   Embutido para que o arquivo funcione sem internet.\n"
        "   Licença completa em vendor/xlsx-LICENSE.txt */\n"
        + lib + "\n</script>"
    )
    if not CDN.search(html):
        sys.exit("tag do SheetJS não encontrada em index.html")
    html = CDN.sub(lambda _: inline, html, count=1)

    # Sem as fontes remotas a página cai na pilha do sistema; retirar a
    # requisição evita a espera de rede ao abrir offline.
    html = FONTS.sub("", html)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print("{} — {:.0f} KB".format(OUT.relative_to(ROOT), OUT.stat().st_size / 1024))

if __name__ == "__main__":
    main()
