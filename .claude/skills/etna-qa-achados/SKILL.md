---
name: etna-qa-achados
description: Como registrar, atualizar e conferir achados (bugs) de QA no Etna — um arquivo por achado (F-XXX.md), estados do ciclo, faixa de ID por worker, evidência obrigatória e regra contra duplicata. Use sempre que um worker de QA (navegador, revisor estático, auditor) achar um bug ou precisar mudar o estado de um achado.
---

# etna-qa-achados

Bug achado em QA não vai pra resposta de texto: vira **um arquivo por achado** numa pasta
compartilhada. Essa pasta é a verdade da operação; o que não está nela não existe pro resto do squad.

- Pasta padrão: `TASK/items/` na raiz do trabalho (o brief pode indicar outra; vale a do brief).
- Nome do arquivo: `F-XXX.md` (três dígitos). Registrar = **criar arquivo novo**, nunca acrescentar
  achado num arquivo único de lista.

## Modelo do arquivo

```
# F-XXX — <título em poucas palavras>

## F-XXX | categoria: funcional|usabilidade|visual|desempenho|segurança | severidade: alta|média|baixa | status: aberto
- Evidência: <caminho do print> OU <arquivo:linha> (revisão de código)
- Passos: 1) ... 2) ...
- Esperado: ...
- Visto: ...
- Correção (resolvedor): <fica vazio até alguém corrigir>
```

Não invente campos nem mude a ordem: outros workers e o Etna leem esse formato.

## Estados

`aberto` → `corrigido` → `verificado`, ou `reaberto`, ou `precisa-decisão`.

| Estado | Quem põe | Quando |
|---|---|---|
| `aberto` | quem achou | acabou de registrar |
| `corrigido` | só o resolvedor | aplicou a correção, validou e preencheu "Correção" |
| `verificado` | só quem testa no navegador | refez os passos depois da correção e passou |
| `reaberto` | só quem testa no navegador | refez os passos e ainda falha (anota o que sobrou + evidência nova) |
| `precisa-decisão` | qualquer um | é dúvida de produto; escreve a pergunta objetiva no arquivo, quem decide é o usuário |

Nenhum estado é pulado (de `aberto` direto pra `verificado` não existe).

## Faixa de ID (pra dois workers não usarem o mesmo número)

- Teste visual no navegador: `F-0XX`.
- Cada revisor estático/auditor recebe a própria centena no brief: `F-2XX`, `F-3XX`, `F-4XX`...
- Antes de criar: liste a pasta, pegue o maior número **da sua faixa** e some 1.
- Número usado nunca volta; nunca registre fora da sua faixa.

## Evidência

- Achado de navegação: caminho do print (de preferência numerado na ordem dos passos).
- Achado de código: `arquivo:linha` e o trecho citado em "Visto".
- Sem evidência não é achado — não registre.

## Antes de registrar: procurar duplicata

Busque na pasta (grep pelo componente, arquivo ou sintoma):

- **Mesmo defeito já registrado** → não crie outro. Se tem evidência nova, acrescente uma linha
  no arquivo existente.
- **Mesmo sintoma, causa diferente comprovada** → crie novo e escreva "ligado a F-XXX".
- **Achado `corrigido`/`verificado` voltou a falhar** → `reaberto` no **mesmo** ID.

## Severidade

- `alta`: impede o uso ou a entrega, perde dado, ou quebra a função principal.
- `média`: atrapalha, mas dá pra contornar.
- `baixa`: acabamento, cosmético.

Quem corrige segue a skill `etna-qa-correcao`.
