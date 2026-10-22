---
name: etna-pdf
description: >
  Cria, lê e junta arquivos PDF — relatórios, propostas, extrair texto de um PDF recebido.
  Use quando o pedido citar PDF, "extrair texto do PDF", "juntar PDFs" ou trouxer um .pdf.
---

# PDF no Etna

Versão própria do Etna, feita com as bibliotecas livres `pypdf` (ler/juntar) e `reportlab` (criar).

## Comandos (script [pdf.py](scripts/pdf.py))

```
PYTHONUTF8=1 uv run --with pypdf --with reportlab scripts/pdf.py ler    arquivo.pdf
PYTHONUTF8=1 uv run --with pypdf --with reportlab scripts/pdf.py criar  saida.pdf conteudo.json
PYTHONUTF8=1 uv run --with pypdf --with reportlab scripts/pdf.py juntar saida.pdf a.pdf b.pdf
PYTHONUTF8=1 uv run --with pypdf --with reportlab scripts/pdf.py exemplo saida.pdf
```

`conteudo.json`: `{"titulo": "...", "paragrafos": ["...", "..."]}`.

## Como trabalhar

1. **Ler:** `ler` extrai o texto página a página. PDF escaneado (imagem) não tem texto: o `ler`
   volta vazio. Nesse caso, avise e peça o arquivo original ou use leitura por imagem
   (abrir a página como print).
2. **Criar:** o `criar` faz texto corrido em A4. Para layout elaborado (cabeçalho de marca,
   tabelas, imagens), monte o documento em Word (skill `etna-word`) ou HTML e exporte.
3. **Juntar:** a ordem dos argumentos é a ordem das páginas.
4. **Nunca sobrescreva o PDF original;** grave sempre com outro nome.
5. Confira o resultado com `ler` (número de páginas e texto com acentos corretos).
6. Material de cliente usa a identidade do cliente, nunca a da agência.
