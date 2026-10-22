---
name: qa-finding-protocol
description: Protocolo de registro de achados de QA no contrato TASK/items/F-XXX.md (um arquivo por bug): formato F-XXX, ciclo de status, faixa de IDs por worker, evidência e regra contra duplicata. Use sempre que for registrar, atualizar ou verificar um achado no QA Vision Lab.
---

# qa-finding-protocol

O contrato `<workspace>/TASK/items/F-XXX.md` é a fonte única da verdade da operação de QA:
**um arquivo por bug**, nunca uma lista única (registrar cria `TASK/items/F-XXX.md`, nunca
acrescenta a um arquivo existente). Vista ao vivo, já com prioridade: `pnpm hub` →
`http://127.0.0.1:7788/tasks?filter=bugs`. Todo achado segue ESTE formato, sem variação:

```
# F-XXX — <título curto>

## F-XXX | categoria: funcional|usabilidade|visual|performance | severidade: alta|média|baixa | status: aberto
- Tela: <evidência: caminho do print, OU arquivo:linha se for revisão estática>
- Passos: 1) ... 2) ...
- Esperado: ...
- Observado: ...
- (resolvedor) Correção: <preenchido por quem corrigir>
```

## Ciclo de status

`aberto` → `corrigido` → `verificado` | `reaberto` | `precisa-decisão`

- `aberto`: registrado, ninguém corrigiu.
- `corrigido`: o resolvedor aplicou o conserto, validou e anotou em `Correção:`.
- `verificado`: o navegador repetiu os passos depois do conserto e confirmou.
- `reaberto`: repetiu e AINDA quebra (anote o que persiste e anexe a evidência nova).
- `precisa-decisão`: dúvida de produto; deixe uma pergunta objetiva no achado, a decisão é do usuário.

Só o navegador promove para `verificado`/`reaberto`. Só o resolvedor marca `corrigido`. Ninguém
pula etapa.

## Faixas de ID (para não colidir)

- Navegador (visão): `F-0XX`
- Revisores estáticos: uma faixa própria POR revisor, definida no briefing: `F-2XX`, `F-3XX`, `F-4XX`...

Antes de registrar: liste `TASK/items/`, ache o maior ID da SUA faixa e use o próximo. Nunca
reaproveite ID, nunca registre fora da sua faixa.

## Evidência (obrigatória)

- Achado visual ou de navegação: caminho do print (quadro numerado).
- Achado de revisão estática: `arquivo:linha` e o trecho citado em Observado.
- Sem evidência não é achado.

## Contra duplicata

ANTES de registrar, procure em `TASK/items/` (pelo componente, arquivo ou sintoma):

- Mesmo defeito já registrado: NÃO duplique. Tendo evidência nova, acrescente uma linha ao `F-XXX.md` existente.
- Mesmo sintoma com causa diferente comprovada: registre achado novo e referencie o antigo ("relacionado a F-XXX").
- Achado `corrigido`/`verificado` que voltou: status `reaberto` no MESMO ID, nunca um ID novo.

## Severidade

- `alta`: impede o uso ou o lançamento; perde dados; função principal quebrada.
- `média`: atrapalha, mas tem contorno.
- `baixa`: acabamento, detalhe cosmético.
