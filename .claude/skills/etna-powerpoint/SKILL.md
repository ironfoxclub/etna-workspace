---
name: etna-powerpoint
description: >
  Cria e lê apresentações do PowerPoint (.pptx) — propostas, relatórios, treinamentos.
  Use quando o pedido citar PowerPoint, .pptx, "apresentação", "slides" em arquivo, ou trouxer um .pptx.
---

# PowerPoint (.pptx) no Etna

Versão própria do Etna, feita com a biblioteca livre `python-pptx` (via `uv run --with`).

## Comandos (script [slides.py](scripts/slides.py))

```
PYTHONUTF8=1 uv run --with python-pptx scripts/slides.py ler  arquivo.pptx
PYTHONUTF8=1 uv run --with python-pptx scripts/slides.py criar saida.pptx slides.json
PYTHONUTF8=1 uv run --with python-pptx scripts/slides.py exemplo saida.pptx
```

`slides.json`: `{"slides": [...]}`. Cada slide tem `titulo` e opcionalmente `topicos` (lista),
`imagem` (caminho de PNG/JPG), `notas` (fala do apresentador). O primeiro slide sem tópicos vira
capa (aceita `subtitulo`). Formato 16:9.

## Como trabalhar

1. **Uma ideia por slide.** Título que diga a conclusão ("Leads dobraram em setembro"), não o
   assunto ("Resultados"). No máximo 5 tópicos curtos.
2. **Ler antes de mexer** em arquivo existente; altere só o que foi pedido e salve com outro nome.
3. **Visual de cliente = identidade do cliente.** O modelo padrão desta skill é neutro de
   propósito; aplique cores e fonte da marca do cliente via `python-pptx`
   (`shape.fill.fore_color.rgb`, `font.name`). Nunca use a identidade da agência em material de cliente.
4. **Imagens** entram por caminho local; confira se o arquivo existe antes de rodar.
5. Quando o pedido é deck bonito pra apresentar (não só arquivo), considere a skill
   `frontend-slides`, que gera HTML animado.
6. Confira com `ler` e, se der, abra o arquivo e olhe se texto não vaza do slide.
