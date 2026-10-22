---
name: etna-diagnostico-skills
description: >
  Descobre por que uma skill não aparece, não dispara ou foi ignorada pela IA no Etna. Tudo local,
  sem acessar a internet. Use quando disserem "a skill X não carrega", "a IA não usou a skill",
  "o Harness acusa skill inexistente".
---

# Diagnóstico de skills (offline)

Rode nesta ordem e pare no primeiro problema. Nenhum passo manda dado pra fora.

1. **Existe?** A skill é uma pasta com `SKILL.md`. Procure nos dois lugares:
   - do workspace: `.claude/skills/<nome>/SKILL.md`
   - da conta: `~/.claude/skills/<nome>/SKILL.md`
   O nome da pasta, o `name:` do cabeçalho e o nome citado no Harness têm que ser iguais.
2. **Cabeçalho válido?** O arquivo começa com `---`, tem `name:` e `description:` e fecha com `---`.
   Sem `description` a IA não sabe quando usar.
3. **A descrição bate com o pedido?** É ela que dispara a skill. Diga *quando* usar, com as palavras
   que o usuário usaria. Descrição vaga = skill ignorada.
4. **O Harness enxerga?** Rode na pasta do Etna: `node teste-harness.js`. Ele confere se cada
   skill citada na tabela existe. Skill acusada = nome errado na tabela ou pasta faltando.
5. **O workspace foi montado?** O workspace do cliente é refeito pelo `montar.py`; skill
   colocada direto nele some na próxima rodada. A fonte fica em `sobrepor/.claude/skills`.
6. **Scripts da skill rodam?** Rode o comando do `SKILL.md` com um exemplo. Erro de `uv`, `python`
   ou `node` ausente aparece aqui.
7. **Conflito?** Duas skills com o mesmo `name` (workspace e conta): a do workspace vence;
   renomeie uma delas.

## Relato

Devolva: qual passo falhou, o caminho do arquivo e a correção sugerida em uma linha. Se tudo
passar, diga que a skill está certa e que o problema é a descrição (passo 3).
