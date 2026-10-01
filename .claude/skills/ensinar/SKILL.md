---
name: ensinar
description: >
  Ensina algo novo ao Cérebro da VulcanOS: lê um arquivo (PDF, docx, md, print) ou um texto colado,
  resume, separa por assunto e grava as memórias no cliente certo (ou na sua empresa, ou no
  conhecimento geral) pelo MCP vulcanos-base. Use quando o usuário disser "/ensinar", "ensina isso
  pro cérebro", "guarda isso no cérebro", "aprende isso" ou "salva isso na memória do cliente X".
---

# /ensinar — Ensinar algo novo ao Cérebro

O Cérebro mora na VulcanOS. Esta skill grava nele pelas ferramentas do MCP `vulcanos-base`
(`listar_clientes`, `buscar_cerebro`, `gravar_memoria`), que o Etna liga em todo painel com o
login da aba VULCANOS. Sem o MCP (Etna sem login na VulcanOS), avisar e parar.

## Ensinar um arquivo ou texto

1. **Para quem é?** Descobrir o dono da memória:
   - um cliente: confirmar o nome com `listar_clientes`;
   - a **sua empresa**: é o cliente marcado com `empresa_propria` em `listar_clientes`;
   - **conhecimento geral** (metodologia, curso, mercado, sem dado de cliente nem identidade de
     marca): `conhecimento_geral=true`.
   Se não der pra saber pela conversa ou pelo arquivo, perguntar. Nunca chutar.
2. **Ler** o material inteiro (Read para PDF, imagem e md; docx: extrair o texto antes).
3. **Separar por assunto**: uma memória por assunto, cada uma com título curto, domínio
   (`oferta`, `produto`, `politicas`, `numeros`, `marketing`, `marca`, `vendas`, `identidade`,
   `arquivos`, `publico`, `concorrentes`, `resultados`) e o texto resumido com o que de fato
   está no material (nada inventado). No fim de cada memória, uma linha `Fonte: <nome do arquivo
   ou "texto colado em AAAA-MM-DD">`.
4. **Checar o que já existe**: para cada memória, `buscar_cerebro` com a pergunta que ela responde.
   - Nada parecido → vai como memória nova.
   - Já existe e o material traz algo diferente → vai como sugestão de alteração (usar o
     `node_id` do resultado; o conteúdo proposto é o nó inteiro já atualizado, não só o trecho novo).
   - Já existe e é igual → não grava.
5. **Mostrar o plano** ao usuário numa tabela curta (título · domínio · nova/sugestão/igual) e
   só gravar depois do "ok".
6. **Gravar** com `gravar_memoria` (PARA: `area` para conhecimento contínuo, `projeto` para algo
   com prazo, `recurso` para material de referência, `arquivo` para histórico).
7. **Responder** com o que foi gravado e quantas sugestões ficaram esperando aprovação (a
   aprovação é na tela Cérebro da VulcanOS).

## Regras

- Identidade visual e tom de voz da sua empresa só vão para o cliente marcado com
  `empresa_propria`, nunca para o conhecimento geral nem para outro cliente.
- Nada de dado pessoal de cliente (e-mail, telefone, CPF, contrato com valores) no conhecimento
  geral.
- Não existe ferramenta de apagar. Pedir "esquece isso" → avisar que apagar memória é pela
  VulcanOS (lixeira), ou propor com `gravar_memoria` + `node_id` um conteúdo corrigido.
