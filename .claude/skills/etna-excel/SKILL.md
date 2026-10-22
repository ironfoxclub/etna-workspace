---
name: etna-excel
description: >
  Cria, lê e edita planilhas do Excel (.xlsx) — orçamentos, controles, relatórios com fórmulas.
  Use quando o pedido citar Excel, planilha, .xlsx, tabela com fórmulas ou trouxer um .xlsx.
---

# Excel (.xlsx) no Etna

Versão própria do Etna, feita com a biblioteca livre `openpyxl` (via `uv run --with`).

## Comandos (script [planilha.py](scripts/planilha.py))

```
PYTHONUTF8=1 uv run --with openpyxl scripts/planilha.py ler  arquivo.xlsx
PYTHONUTF8=1 uv run --with openpyxl scripts/planilha.py criar saida.xlsx dados.json
PYTHONUTF8=1 uv run --with openpyxl scripts/planilha.py exemplo saida.xlsx
```

`dados.json`: `{"abas": {"Nome da aba": [[linha 1], [linha 2], ...]}}`. A primeira linha vira
cabeçalho (negrito, fundo escuro) e as colunas se ajustam ao conteúdo. Texto que começa com `=`
vira fórmula (`"=B2*C2"`, `"=SUM(D2:D9)"`).

## Como trabalhar

1. **Ler antes de mexer.** `ler` mostra cada célula; fórmula aparece como `=B2*C2` e, quando o
   Excel já calculou e salvou, como `=B2*C2→120`.
2. **Use fórmula, não número digitado,** pra tudo que for conta. Assim a planilha continua viva.
3. **Fórmulas só têm valor depois que o Excel (ou o LibreOffice) abre e salva.** O openpyxl grava
   a fórmula, mas não calcula. Se precisar do resultado no próprio script, calcule em Python e
   avise que a planilha vai mostrar o valor ao abrir.
4. **Editar arquivo existente:** `load_workbook(caminho)` (sem `data_only`, senão as fórmulas
   viram valores fixos ao salvar), altere e salve com outro nome.
5. Datas como `datetime`, dinheiro com `cell.number_format = 'R$ #,##0.00'`.
6. Confira com `ler` e olhe se nenhuma célula ficou com erro (`#REF!`, `#DIV/0!`).
