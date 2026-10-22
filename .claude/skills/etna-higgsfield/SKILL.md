---
name: etna-higgsfield
description: >
  Use quando o trabalho pedir imagem ou vídeo gerado pela Higgsfield (ou quando a tarefa
  falar em "higgsfield", "gpt-image", "prompt de imagem em lote"): escolha do provedor,
  chamada pela ferramenta de mídia do Etna (etna_imagem_gerar / etna_video_gerar com
  provider "higgsfield"), formato do prompt de foto e de asset de layout, e o que fazer
  quando a chave não está ligada. Não gera nada por conta própria: tudo passa pela
  ferramenta de mídia do Etna. Para plano cinematográfico, carregue etna-cinema-shot;
  para imagem simples em lote, etna-image-assets.
---

# Higgsfield no Etna

A Higgsfield é UM dos provedores da ferramenta de mídia do Etna. Não existe CLI nem
script próprio: você chama a mesma ferramenta de sempre e, quando precisar dela, diz `provider: "higgsfield"`.

## Antes de tudo

1. Chame `etna_midia_provedores`. Ela mostra quais IAs estão prontas, qual é o padrão da
   pessoa (Configurações › Imagem e vídeo) e o modelo de cada uma. Nunca mostra chave.
2. Higgsfield não aparece como pronta? Então a chave não foi guardada. **Não peça a chave
   no chat e não procure em `.env`.** Diga à pessoa: "Configurações › Imagem e vídeo ›
   Higgsfield, cole a chave no formato `ID:SEGREDO`". Enquanto isso, use o provedor que
   estiver ligado, se o briefing deixar.
3. Só force `provider: "higgsfield"` quando a tarefa exigir. Sem `provider`, vale a escolha
   da pessoa, e é isso que ela espera.

## Chamadas

- Imagem: `etna_imagem_gerar({ prompt, outPath, provider: "higgsfield", imageUrl?, formato? })`
- Vídeo: `etna_video_gerar({ prompt, outPath, provider: "higgsfield", imageUrl?, endImageUrl?, formato?, segundos? })`

Uma chamada por arquivo. Vários espaços de imagem = várias chamadas em paralelo.
Vídeo leva minutos: se a espera falhar e o erro trouxer um id de job, retome com
`recoverJobId` em vez de gerar e pagar de novo.

## Dois formatos de prompt de imagem

- **Foto** (hero, elenco, cena): texto corrido, cinematográfico. Assunto literal, luz,
  lente, enquadramento, paleta da marca em palavras (cor + nome, nada de hex solto).
- **Asset de layout** (fundo, pôster, gráfico): objeto JSON curto com `assunto`, `estilo`,
  `paleta`, `proporção`, `texto_na_imagem` (vazio quando não houver texto).

Todo prompt cita a paleta do DNA de design do projeto. Prompt sem paleta volta pra revisão.

## Erros comuns

| Sintoma | O que fazer |
|---|---|
| Erro de chave / não autorizado | Chave ausente ou errada. Pare e avise a pessoa (passo 2). Não tente de novo em laço. |
| Modelo não encontrado | O id vem da configuração (`config.midia.modelo`) e é trocável pela pessoa. Relate o id do erro, não invente outro. |
| Vídeo pediu quadro final | Mande `endImageUrl` junto com `imageUrl` (interpolação entre dois quadros). |
| Filtro de conteúdo recusou | Reescreva a cena sem nome de pessoa real nem marca; veja o filtro na `etna-cinema-shot`. |

## Regras

- Chave só no cofre do Etna (safeStorage). Nunca em variável de ambiente, arquivo ou resposta.
- Arquivo vai pra `outPath` dentro da pasta da missão. Cite o caminho no handoff como link.
- Não gaste crédito pra testar: um teste de chamada usa 1 imagem pequena, nunca vídeo.
