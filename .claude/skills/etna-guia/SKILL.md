---
name: etna-guia
description: >
  Manual do Etna 1.0 em português simples: abas, painéis, missões, Times, Harness, Quadro,
  Magma, contas e atalhos. Use quando alguém perguntar "como faço X no Etna", "onde fica Y",
  "o que é Harness/Time/missão" ou estiver perdido no app.
---

# Etna 1.0: guia de uso

Explique pra quem não é programador: frases curtas, um passo de cada vez, nome do botão como
aparece na tela. Se a pessoa descrever um problema, diga onde clicar antes de explicar a teoria.

## O que é o Etna

Uma central de comando: vários terminais de IA lado a lado (painéis), mais a VulcanOS, o Magma
(criação visual), o Quadro (tarefas) e um chat, tudo numa janela só.

## Onde fica cada coisa

- **Barra de cima:** nome, limites de uso das contas (clique para ver o detalhe) e os botões da janela.
- **Faixa de abas:** casinha (Home), módulos **VULCANOS, MAGMA, QUADRO, CHAT** e uma aba por
  workspace. À direita: busca, organizar grade, **ARQUIVOS**, ditado, **NATHAN**, **+ PANE** e a conta.
- **Lateral de missões** (dentro de um workspace): lista de missões, **+** para criar, ARQUIVADOS
  para as encerradas, e a raposa com seu nível.
- **Painéis:** cada um é um terminal. Arraste a divisória para mudar o tamanho; arraste o
  cabeçalho para trocar de lugar. Luz verde = livre; amarela girando = trabalhando; vermelha =
  precisa de você; vermelha com "!" = falhou.
- **Caixa** (aprovações) e **CONFIG** ficam no menu do avatar.

## Conceitos

- **Workspace:** uma pasta de trabalho (um cliente, um projeto). Cada um tem sua aba.
- **Missão:** um objetivo com início e fim. Tem um **maestro** (quem planeja e divide) e
  **workers** (quem executa cada parte). Cada worker recebe um **brief**: um arquivo com a
  tarefa, e devolve o resultado na seção "Resultado".
- **Modos de missão:** *Livre* (você comanda cada painel), *Agêntico* (o maestro divide o
  objetivo sozinho) e *Time* (o maestro usa um time pronto).
- **Times:** grupos de papéis com quantidade, modelo e esforço (ex.: FUNCIONALIDADE, CAÇA-BUG,
  SITE, AUDITORIA, BANCO, DOCS, CINEMA, ENXAME DE QA). No **+ MISSÃO › Time** você escolhe um,
  ajusta e, se quiser, salva uma cópia sua. Também dá para **descrever o resultado e a IA monta o time**.
- **Harness:** a tabela que decide, para cada tipo de tarefa, qual IA, conta, modelo, esforço e
  skills usar. Tarefa difícil sobe de modelo; tarefa simples desce para economizar. Fica nas
  configurações; linha criada por você não é mexida em atualização.
- **Skills:** receitas que a IA lê quando o assunto aparece (Word, planilha, site, vídeo...).
  O Harness só cita skills que existem; se faltar uma, ele avisa.
- **Quadro:** cards de tarefa. Um pedido digitado vira card; ao terminar, o card é entregue. Cada
  card usa o tipo de tarefa para o Harness escolher quem executa.
- **Magma:** estúdio de criação (site, carrossel, post, vídeo). Tem chat com um maestro que
  delega para workers.
- **MCPs liberados:** veja a skill `etna-mcp`.

## Receitas rápidas

1. **Começar uma tarefa simples:** *+ PANE* › escolha a IA › digite o pedido.
2. **Missão com time:** *+ MISSÃO* › Time › escolha › REVISAR › começar. Acompanhe pelo
   checklist de cada painel.
3. **Ver o que sobrou de limite:** chips na barra de cima.
4. **Responder uma dúvida de um worker:** aparece um aviso/pop-up; responda e ele continua.
5. **Mandar um arquivo para a IA:** 📎 na caixa, colar ou soltar o arquivo.

## Se algo não funcionar

Peça para a pessoa descrever o que viu (cor da luz, mensagem). Painel vermelho com "!" = abra o
painel e leia a última mensagem. Skill não aparece = skill `etna-diagnostico-skills`.
Detalhes técnicos de cada etapa ficam no LEIAME e em `docs/guia-layout.md` da pasta do Etna.
