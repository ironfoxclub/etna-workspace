---
name: qa-fix-protocol
description: Protocolo do resolvedor de QA: consulta o contrato TASK/items/F-XXX.md (um arquivo por bug), prioriza por severidade, agrupa por arquivo, faz um commit por achado com o ID, usa git add específico e valida no dev antes de marcar como corrigido. Use sempre que for corrigir achados no QA Vision Lab.
---

# qa-fix-protocol

Você corrige, em laço, os achados do contrato `<workspace>/TASK/items/` (um arquivo por bug,
`F-XXX.md`).

## Escolha (consulta)

1. Leia `TASK/items/*.md` (ou a vista ao vivo com prioridade: `pnpm hub` → `http://127.0.0.1:7788/tasks?filter=bugs`).
2. Candidatos = achados com `status: aberto`.
3. Prioridade: severidade `alta` > `média` > `baixa`; empate = menor ID.
4. **Agrupe por arquivo**: bugs que tocam o MESMO arquivo ficam com o MESMO resolvedor. Se outro resolvedor já está num achado daquele arquivo, pule pro próximo candidato. Nunca edite arquivo que outro worker está corrigindo.

## Correção

1. Leia antes de editar: o arquivo apontado, quem o chama e a evidência (print/trecho), até entender a CAUSA RAIZ. Sintoma não é causa.
2. Conserto mínimo que resolve o achado. Nada de refatoração de carona, nada de "melhoria" no código vizinho.
3. **Valide ANTES de marcar**: checagem de tipos da área + reprodução do cenário do achado no servidor de desenvolvimento rodando (processo de apoio do Tauri = reiniciar o `tauri dev`; tela = o recarregamento a quente costuma bastar). Olhe o log do dev atrás de erros novos. Validação que não rodou é achado que volta como `reaberto`.

## Commit (um por achado)

- `git add` SÓ dos arquivos que VOCÊ tocou neste achado. NUNCA `git add -A`, NUNCA `git add .`. Arquivo de outro worker no stage é contaminação.
- Mensagem com o ID: `fix(área): F-XXX — resumo do conserto`.
- 1 achado = 1 commit. Dois achados no mesmo arquivo ainda assim viram commits separados, na ordem em que você corrigiu.

## Atualização do contrato

Depois do commit e da validação, no arquivo `TASK/items/F-XXX.md`:

- `status: aberto` → `status: corrigido`
- preencha `- (resolvedor) Correção:` com a causa raiz (1 ou 2 frases), os arquivos com o hash do commit e COMO você validou (o que rodou e o que observou).

## Exceções

- Dúvida de PRODUTO (comportamento esperado ambíguo, decisão de UX ou de escopo): marque `precisa-decisão`, deixe uma pergunta objetiva no achado e SIGA pro próximo. Não decida produto sozinho e não trave.
- No máximo 3 tentativas na mesma abordagem; na 3ª falha, registre no achado o que tentou e mude de abordagem ou devolva no handoff.
- Nunca derrube processo que você não subiu (a produção pode estar rodando): encerre o dev por PID específico, jamais por nome.

## Handoff (quando acabar)

Sem mais achados `aberto` elegíveis, ou orçamento do briefing atingido: handoff com os IDs
corrigidos e os commits, os `precisa-decisão` pendentes e os agrupamentos que sobraram.
