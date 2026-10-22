---
name: etna-route
description: "Escreve um plano de implementação a partir de uma especificação antes de mexer no código: mapa de arquivos, tarefas do tamanho certo com caminhos exatos, passos com teste que falha primeiro, código completo, autorrevisão e passagem para a execução. Use quando uma tarefa de vários passos já tem especificação e precisa de um plano que um worker sem nenhum contexto consiga executar."
---

# etna-route: um plano que um desconhecido executa

Escreva para quem conhece a linguagem mas não sabe nada deste projeto, das ferramentas ou do
assunto. Tudo de que essa pessoa precisa está DENTRO do plano: quais arquivos, que código, como
testar, o que commitar. Ao começar, avise: "Usando etna-route para escrever o plano."

**Onde guardar:** `docs/plans/AAAA-MM-DD-<funcionalidade>.md`, a menos que o projeto defina outro
lugar. Se o projeto acompanha o trabalho num quadro (cards, tarefas), cada tarefa do plano vira um
card e o arquivo do plano é rascunho descartável: o contrato é o card.

## 1. Conferir o escopo

Um plano = um subsistema que entrega software funcionando e testável sozinho. Especificação que
cobre subsistemas independentes ganha um plano para cada. Diga isso antes de escrever.

## 2. Mapa de arquivos primeiro

Antes de qualquer tarefa, liste cada arquivo criado ou alterado e a responsabilidade única dele.
Divida por responsabilidade, não por camada; o que muda junto fica junto; siga a estrutura que o
projeto já tem (nunca reestruture por conta própria). A decomposição fica travada aqui.

## 3. Tamanho certo da tarefa

Tarefa é a menor unidade com ciclo de teste próprio que um revisor poderia rejeitar sem afetar a
vizinha. Coloque preparação, configuração e documentação dentro da tarefa cuja entrega precisa
delas. Toda tarefa termina com algo executável.

## 4. Passos de 2 a 5 minutos

"Escreva o teste que falha" · "Rode e veja falhar" · "Implementação mínima" · "Rode e veja
passar" · "Commit". Cada um é uma caixinha.

## 5. Cabeçalho (obrigatório)

```markdown
# Plano de implementação: <Funcionalidade>
**Objetivo:** uma frase.
**Arquitetura:** 2 ou 3 frases.
**Stack:** bibliotecas e ferramentas principais.
## Restrições globais
Uma linha cada, com os valores exatos copiados da especificação (versões, nomes, plataforma, limites).
```

## 6. Modelo de tarefa

````markdown
### Tarefa N: <componente>
**Arquivos:** Criar `caminho/exato` · Alterar `caminho/exato:linhas` · Testar `caminho/do/teste`
**Interfaces:** Consome: <assinaturas exatas de tarefas anteriores> · Produz: <nomes e tipos exatos de que as próximas dependem>
- [ ] Passo 1: o teste que falha (código completo)
- [ ] Passo 2: rodar `<comando exato>` → esperado: FALHA com "<mensagem>"
- [ ] Passo 3: a implementação (código completo)
- [ ] Passo 4: rodar `<comando exato>` → esperado: PASSA
- [ ] Passo 5: `git add <caminhos> && git commit -m "<tipo>: <o quê>"`
````

## 7. Sem lacunas: tudo isto é falha do plano

"A definir", "TODO", "tratar erros", "cobrir casos de borda", "escrever testes para o acima" sem o
código do teste, "igual à Tarefa N" (repita o código; as tarefas são lidas fora de ordem), passos
que descrevem sem mostrar, referências a nomes que nenhuma tarefa define.

## 8. Autorrevisão antes de entregar

1. **Cobertura da especificação**: cada requisito aponta para uma tarefa; liste as lacunas e acrescente as tarefas.
2. **Busca de lacunas**: procure os padrões acima e corrija no próprio texto.
3. **Consistência de nomes e tipos**: `clearLayers()` na Tarefa 3 e `clearFullLayers()` na Tarefa 7 é bug.

## 9. Passar para a execução

Ofereça a escolha: (a) um worker novo por tarefa, com revisão entre elas; no Etna, um
`etna-pilot` abrindo um painel `etna-builder` por tarefa; ou (b) execução no próprio painel, com
pontos de conferência. Não comece a executar no mesmo turno do planejamento, a menos que peçam.
