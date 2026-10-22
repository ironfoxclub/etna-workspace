---
name: etna-word
description: >
  Cria, lê e edita documentos do Word (.docx) — propostas, contratos, relatórios, atas.
  Use quando o pedido citar Word, .docx, "documento", "proposta em Word" ou trouxer um .docx
  pra ler ou alterar.
---

# Word (.docx) no Etna

Versão própria do Etna, feita com a biblioteca livre `python-docx`. Não precisa instalar nada:
o `uv run --with` baixa na hora.

## Comandos (script [word.py](scripts/word.py))

```
PYTHONUTF8=1 uv run --with python-docx scripts/word.py ler  arquivo.docx
PYTHONUTF8=1 uv run --with python-docx scripts/word.py criar saida.docx conteudo.json
PYTHONUTF8=1 uv run --with python-docx scripts/word.py exemplo saida.docx
```

`conteudo.json` aceita: `titulo`, e em `blocos` qualquer mistura de `{"h1": ""}`, `{"h2": ""}`,
`{"p": ""}`, `{"lista": ["", ""]}` e `{"tabela": [["cabeçalho", ...], ["linha", ...]]}`.

## Como trabalhar

1. **Ler antes de mexer.** Se veio um .docx, rode `ler` e entenda a estrutura.
2. **Documento novo:** escreva o `conteudo.json` (título, seções, tabelas) e rode `criar`.
3. **Editar um arquivo existente:** abra com `Document(caminho)` num script curto, altere só o
   necessário e salve com **outro nome** (`-v2.docx`). Nunca sobrescreva o original do cliente.
4. **Conferir:** rode `ler` no arquivo gerado e compare com o que foi pedido. Texto em português
   com acento tem que sair sem caracteres quebrados.
5. Material de cliente usa a identidade do cliente, nunca a da agência.

## Limites desta versão

Cabeçalho/rodapé, estilos de marca e imagens exigem código extra com `python-docx`
(`doc.add_picture`, `doc.sections[0].header`). Faça no script quando o pedido pedir.
Se precisar de PDF final, gere o .docx e use a skill `etna-pdf` ou exporte pelo Word.
