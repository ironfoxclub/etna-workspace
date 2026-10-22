---
name: etna-formador-de-times
description: >
  Ajuda a pensar e montar um time de IAs para um objetivo: faz as perguntas certas, escolhe os
  papéis e entrega o pedido pronto para o "IA monta" do Etna. Use quando disserem "monta um time
  pra...", "que time uso pra...", "preciso de uma equipe de agentes".
---

# Formador de times

**Não monta o time por conta própria.** Quem monta e valida é o "IA monta" do Etna
(`squads/ia-monta.js`, na tela **+ MISSÃO › Time › Descrever o resultado**). Esta skill só prepara
o pedido para ele sair bom. Assim a regra de papéis, limites e validação existe em um lugar só.

## Passos

1. **Objetivo em uma frase.** "No fim deste trabalho existe o quê?" (um site, um relatório, um bug
   corrigido). Sem resultado claro, pergunte.
2. **Quebre em frentes.** Mapear o que existe, construir, revisar, testar. Cada frente é um papel.
3. **Cheque se já existe time pronto.** Compare com os originais (FUNCIONALIDADE, CAÇA-BUG, SITE,
   AUDITORIA, BANCO, DOCS, LANDING ABSURDA, CINEMA, CINEMA SITE, ENXAME DE QA, QA POR VISÃO). Se um
   serve, sugira usá-lo e pare.
4. **Papéis disponíveis** estão em `squads/papeis.js` (explorador, construtor, revisor, testador,
   documentador etc.). Use só ids que existem lá. Comece pelo explorador e termine por revisor ou testador.
5. **Dimensione:** 2 a 6 linhas, 1 a poucos workers por linha. Modelo grande só onde há decisão ou
   construção pesada; leitura e mapa vão em modelo pequeno.
6. **Escreva o pedido para o IA monta**, assim:

```
Objetivo: <uma frase>
Entregas: <lista curta do que deve existir no fim>
Restrições: <prazo, pasta, o que não pode mexer>
Sugestão de papéis: <opcional, na ordem>
```

7. Diga ao usuário: abra **+ MISSÃO › Time › Descrever o resultado**, cole o pedido e revise a
   proposta antes de salvar.

## Não faça

- Não invente papéis fora de `papeis.js`.
- Não crie o time salvando arquivo de configuração à mão.
- Não use a identidade visual da agência em time de cliente.
