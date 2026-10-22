---
name: etna-site-premium
description: >
  Constrói sites premium, dignos de prêmio (páginas de captura, sites de marca, portfólios) que
  parecem de agência (nível R$ 250 mil) e não de modelo feito por IA. Use quando um worker de
  squad precisa DESENHAR e CONSTRUIR um site que tem que parecer caro, editorial, de luxo,
  sofisticado ou "nada genérico", ou quando o briefing citar qualidade de premiação, nível
  Awwwards ou marca que vive de design. Cuida da doutrina de acabamento premium (a lista proibida
  de estética de IA, tipografia como identidade, o catálogo de estruturas, a coreografia de
  movimento, os microdetalhes) E amarra o motor de mídia do hero à pilha de geração PRÓPRIA do
  Etna (etna_imagem_gerar / etna_video_gerar pelas skills cinema-shot / site-scrub / site-encode),
  nunca com incorporações de terceiros, cenas copiadas ou banco de imagens por link externo.
  Adapta-se à stack: entrega por padrão uma página única publicável (HTML/CSS/JS), ou React/Next
  quando a receita pedir. Vincule ao worker construtor do site. Gatilhos: site premium, awwwards,
  landing de luxo, web editorial, design sofisticado, fazer parecer caro, qualidade de agência,
  site de marca, portfólio, nada genérico, hero premium.
---

> **Mídia no Etna (vale sobre qualquer outra menção neste arquivo).** Ferramentas MCP do Etna: `etna_imagem_gerar(prompt, outPath, provider?, imageUrl?, formato?)`, `etna_video_gerar(prompt, outPath, provider?, imageUrl?, endImageUrl?, formato?, segundos?)`, `etna_voz_gerar(prompt, outPath, voiceId?)` e `etna_midia_provedores()` (quem está pronto, a escolha da pessoa e o modelo de cada um; nunca mostra chave). Provedores: imagem = `antigravity` (padrão, plano do Google, sem chave) | `higgsfield` | `gemini` | `openai` | `fal`; vídeo = `higgsfield` (Seedance) | `fal` (Kling: o único que respeita `endImageUrl`, e o Etna já o escolhe sozinho quando você passa `endImageUrl`); voz = `elevenlabs`. Não passe `provider` a menos que a tarefa exija: vale a IA que a pessoa escolheu em Configurações › Imagem e vídeo. O Antigravity NÃO gera vídeo. `outPath` é relativo à pasta do painel. Sem provedor pronto a ferramenta diz o que falta: pare e avise a pessoa; nunca troque de motor em silêncio. Os nomes antigos (`google-image`, `openai-image`, `replicate-video`, `selectedModel`/`enabledModels`) = `antigravity`/`gemini`, `openai`, `fal` e o campo `modelo` de `etna_midia_provedores`.


# etna-site-premium: sites premium na pilha própria do Etna

Construa sites em que cada pixel é intencional, cada movimento é coreografado e a impressão é de
que houve talento criativo e orçamento de verdade, do tipo que faz as pessoas perguntarem "quem
desenhou isso?". Esta skill carrega a **doutrina de acabamento** premium e a liga ao **pipeline de
mídia próprio** do Etna, de modo que nada na página dependa de recurso, cena ou URL de terceiro.

> **PRINCÍPIO DE SALA LIMPA / MÍDIA PRÓPRIA (leia primeiro).** Todo visual de um site premium do
> Etna é (a) escrito em código (CSS/SVG/canvas) ou (b) **gerado pelas ferramentas de mídia do
> próprio Etna** (`etna_imagem_gerar`, `etna_video_gerar`), conduzidas pelas skills de cinema e
> rolagem. **Nunca** incorpore cena 3D de terceiros, **nunca** puxe a URL de um recurso do site ao
> vivo de outra pessoa, **nunca** use foto de banco de imagens por link externo. O "uau" vem de mídia
> própria, gerada e na identidade da marca, não de recurso emprestado. É isso que mantém a entrega
> distribuível e livre de problemas de propriedade intelectual.

---

## O problema da estética de IA

A maioria dos sites feitos por IA compartilha um DNA reconhecível. Vencê-lo exige saber exatamente
como ele é e recusá-lo de propósito.

### A lista proibida: nunca entregue isto

**Sinais na tipografia**
- Inter, Poppins, Montserrat, Raleway, Space Grotesk ou Outfit como fonte principal: o sinal instantâneo de "modelo de IA". (*Inter Tight* é outra família, com métricas próprias, e é permitida.)
- Uma família só para tudo; hierarquia uniforme e previsível (64 → 32 → 18 → 14).
- Espaçamento entre letras e entre linhas padrão em todo lugar; parágrafos de várias linhas centralizados em todo lugar.

**Sinais na cor**
- Gradientes de roxo para azul (o maior clichê isolado); índigo/violeta como cor da marca sem motivo.
- Fundo branco + um acento + texto cinza (o kit inicial de SaaS); gradientes gratuitos em botões e cards.
- Camadas semitransparentes no lugar de decisões reais de cor; o visual neon sobre escuro de "portfólio de dev".

**Sinais no layout**
- Hero → grade de 3 colunas de funções → depoimentos → chamada para ação → rodapé (SaaS padrão), ou hero → números → grade de trabalhos → sobre dividido → chamada → rodapé (o modelo "premium de IA", tão fórmula quanto o outro).
- Qualquer ordem de cima para baixo que poderia ser trocada entre dois sites. Cada site precisa do próprio DNA estrutural: número de seções e lógica de ordenação diferentes.
- Grades simétricas perfeitas de cards iguais; tudo centralizado numa coluna de largura máxima única.
- Retângulos arredondados + sombras como elemento principal de interface; ícone + título + parágrafo em fileira de 3 ou 4.
- Hero só de texto, chapado; o hero deve ser um momento espacial, guiado por mídia.

**Sinais no movimento**
- Tudo subindo com fade na rolagem (o truque gasto do AOS); transições idênticas em tudo.
- Hover = crescer + sombra; indicadores giratórios de carregamento em vez de esqueletos ou revelações coreografadas.

**Sinais na decoração**
- Formas de blob, primitivas geométricas flutuantes, fundos de malha de gradiente, grades uniformes de fotos de banco, emojis ou ícones de linha como marcadores de seção.

---

## Como o caro realmente se parece

O premium se lê por contenção, surpresa e detalhe obsessivo.

### Tipografia como identidade

A tipografia é a alavanca nº 1 entre um site de R$ 2 mil e um de R$ 250 mil.
- Fonte de título com personalidade e opinião: serifadas como *Playfair Display, Cormorant Garamond, DM Serif Display, Fraunces, Instrument Serif*; sem serifa pouco batidas como *Syne, General Sans, Satoshi, Switzer, Cabinet Grotesk, Inter Tight, IBM Plex Sans, Manrope, Archivo*. Monoespaçada como tipo de acento para rótulos, datas e metadados (*JetBrains Mono, IBM Plex Mono, Space Mono*) soa editorial.
- Combine um título cheio de caráter com um corpo neutro e refinado. Misture pesos de forma dramática (título 900 ao lado de corpo 300 cria tensão).
- Execução: `clamp()` para escala fluida (não saltos por ponto de quebra); contraste dramático (títulos de 8vw+); espaçamento entre letras negativo nos títulos grandes (`-0.03em` a `-0.06em`); altura de linha generosa no corpo (1,6 a 1,8) e justa nos títulos (0,9 a 1,1); `max-width` de 45 a 75ch nos parágrafos, `text-wrap: balance` nos títulos; microrrótulos em caixa-alta com espaçamento largo (`0.1em`+) para categorias e metadados.

### Cor como atmosfera

- Comece em preto e branco; acrescente cor só quando ela merecer o lugar. Um matiz dominante com intenção ("que território emocional ele reivindica?").
- Brancos quebrados e cinzas quentes vencem o `#fff`/`#000` puros (`#FAFAF8`, `#F5F0EB`, `#1A1A1A`, `#0D0D0D`).
- Monocromático ou análogo com um único momento de contraste soa mais sofisticado que arco-íris. Cor usada com parcimônia bate mais forte: um único link vermelho num campo preto e branco vence vermelho em todo lugar.
- Tema escuro bem feito = camadas de fundo pensadas, com leves tons quentes ou frios, não "branco sobre cinza-escuro".

### Layout como narrativa: a regra do DNA estrutural

A falha nº 1 são sites que parecem diferentes na superfície mas partilham o mesmo esqueleto. Antes
de qualquer marcação, **diga em voz alta o conceito estrutural principal**, numa expressão
nominal só. Num lote, **dois sites nunca compartilham o mesmo conceito.**

**Catálogo de DNA estrutural** (escolha UM, comprometa-se, não misture):
1. **Manuscrito indexado**: uma longa coluna editorial, sem seções, um único ritmo tipográfico. (um cardápio, um manifesto, uma carta.)
2. **Diorama horizontal fixo**: a rolagem vertical conduz uma cena que desliza na horizontal (`sticky` + `translateX` ligado à rolagem). (uma linha do tempo, um processo, uma coleção.)
3. **Divisão permanente em dois painéis**: 50/50 ou 38/62 fixo; um painel fica preso, o outro rola. (um arquivo com índice ao vivo.)
4. **Sequência de slides**: slides de viewport inteira com encaixe, cada um uma composição diferente. (uma monografia, um look-book.)
5. **Objeto em pedestal**: um único assunto central de herói, com marginália orbitando. (uma casa de produto único: um relógio, uma garrafa, um prato.)
6. **Narrativa fixada (scrollytelling)**: uma seção de 2 a 4 telas fica fixa enquanto o conteúdo avança por estados. Usada uma vez, como peça central. (um processo, um perfil de missão.)
7. **Navegação horizontal**: a rolagem principal é horizontal, as seções se leem da esquerda para a direita.
8. **Barra lateral + coluna**: uma barra lateral fixa que não rola (navegação e metadados) + a coluna é o site.
9. **Portões de capítulo**: divisores de viewport inteira entre zonas tonais; a página muda de caráter conforme você desce.
10. **Livro-razão / registro**: a página como documento (manifesto, registro); linhas de tabela dominam.
11. **Colagem / quebra de grade**: assimetria de revista com rupturas deliberadas (sangrias enormes, citações destacadas cruzando as calhas).
12. **Objeto único, sem moldura**: só o assunto + uma frase. Sem navegação, sem rodapé.
13. **Lousa de interface de produto**: o hero simula a própria interface do produto (para ferramentas cujo produto É uma interface).
14. **Grade de blocos de painel**: a página como painel com sensação de tempo real (contadores, minigráficos, indicadores).
15. **Linha do tempo de conversa**: a página reproduz uma transcrição ou ligação conforme se rola.

**Escolha pelo fato central do cliente**, não por um modelo. Rejeite qualquer conceito usado pelo
site anterior nesta sessão. Escreva o conceito + uma frase de justificativa antes de qualquer
marcação.

**Dentro do conceito:** quebre a grade de propósito (largura total e depois coluna estreita; divisões
assimétricas 60/40 e 70/30; imagens sangrando para fora da tela; elementos sobrepostos cruzando os
limites das seções; rótulos fixos acompanhando a rolagem). Espaço em branco é sinal de luxo: `8rem`+
entre seções. Linhas de tabela estilo livro-razão para listas, não grades de cards. Campos de
formulário como partes de um documento editorial (rótulos monoespaçados acima, só borda inferior),
nunca um formulário de SaaS.

**Variedade de navegação (uma falha silenciosa):** não adote por padrão a barra superior
`auto 1fr auto` com mix-blend-mode. Escolha a navegação que pertence à marca e ao DNA estrutural:
nenhuma navegação; navegação embutida numa barra lateral fixa; uma barra de comandos inferior
(`⌘K`); logotipo centralizado em linha com uma faixa de abas; um índice de rolagem horizontal que
também é navegação; um letreiro corrido; navegação vertical à esquerda; uma navegação em barra de
status com indicador ao vivo.

**Ajuste a estética ao ramo, sem cair por padrão no editorial de luxo** (fundo creme + Fraunces +
acento latão). Isso é certo para alta-costura, perfumaria e alta gastronomia, e errado para
tecnologia, IA e SaaS. **Se o ramo é tecnologia**, incline-se para fundos de branco puro ou quase
preto, grotesca neutra como título, monoespaçada usada como título, bordas com brilho em gradiente,
capturas da interface entregue, blocos de painel, teclas em etiquetas, blocos de código como hero.
Estude os líderes da categoria: alguns reais, citados como direção, não copiados.

---

## Mídia do hero: a pilha de geração PRÓPRIA do Etna (substitui qualquer 3D/banco de imagens de terceiros)

O diferencial premium é um **hero guiado por mídia**, e no Etna essa mídia é **gerada e própria**,
nunca incorporada de outro lugar. É aqui que esta skill se combina com a família cinema/site.

**Decida o tratamento do hero pelos provedores de mídia configurados** (`etna_midia_provedores`):

| Provedores ativos | Tratamento do hero | Como (pipeline próprio) |
|---|---|---|
| **vídeo** | Um hero animado: peça central em laço, guiada por movimento | `etna-cinema-shot` gera o quadro-chave e o clipe (`etna_imagem_gerar` → `etna_video_gerar`); `etna-site-encode` deixa o arquivo seguro para a web (mp4 h264+faststart, webm vp9, pôster, laço contínuo mudo); incorpore como `<video autoplay muted loop playsinline poster>`. Para heros com rolagem controlada, use `etna-site-scrub` (sequência de imagens ligada à rolagem). |
| **só imagem** | Um hero de imagem estática gerada (ou objeto em pedestal) | `etna-cinema-shot` → `etna_imagem_gerar` para uma imagem estática literal ao tema e na identidade da marca; trate-a como o assunto em cena. Para um layout inteiro, cada espaço de imagem (cards, galeria) ganha a própria imagem gerada: abra em paralelo, um worker por espaço. |
| **nenhum** | Um hero tipográfico / CSS-SVG | Escreva o hero em código: tipografia gigante, gradientes cônicos/lineares, SVG, atmosfera em canvas. Determinístico, próprio, sem rede. |

**Regras da mídia própria (rígidas):**
- **Literal ao tema, não metafórico.** Gere o que a marca É: uma salsicha para a barraca de cachorro-quente, uma garrafa para a perfumaria. Teste dos dois segundos: sem legenda, quem vê nomeia o assunto.
- **Tratamento de cor da marca.** Paleta e luz da mídia gerada precisam combinar com o fundo do site (sem cara de colado por cima). Conduza o gerador com os tokens de design ou a cena-chave (veja cinema-shot).
- **Nenhum recurso de terceiros, nunca.** Não incorpore cena 3D nem qualquer recurso que você não possua, não puxe URL de recurso de site ao vivo, não use foto de banco por link externo. Se não dá para gerar e não há recurso do cliente, recorra a uma ilustração em CSS/SVG; nunca tome emprestado.
- **Texto nítido fica no código.** Modelo de difusão inventa tipografia: mantenha TODOS os logotipos, títulos e números fora da geração e componha-os em CSS sobre a mídia.
- **Recursos do cliente primeiro.** Se a pessoa forneceu fotos reais do produto ou vídeo da marca, use-os antes de gerar.

Efeitos atmosféricos só em código (campo de partículas, plano de grade, canvas de poeira à deriva)
são bons como **atmosfera de fundo atrás** de um hero gerado ou tipográfico, nunca como assunto
principal.

---

## Experiência guiada pela rolagem e coreografia de movimento

A rolagem deve parecer uma jornada dirigida.
- **Técnicas:** camadas de paralaxe (multiplicadores diferentes de `scrollY`); seções de rolagem horizontal (contêiner `sticky` + `translateX` ligado à rolagem); escala conforme a rolagem (`IntersectionObserver` / `getBoundingClientRect`); revelação de texto por palavra ou linha; transições de cor ligadas à rolagem; sequências fixadas; zoom atravessando. Use de 2 a 3 técnicas distintas por site; não repita a técnica da peça central ao longo de um lote.
- **Padrão de desempenho:** marcação por rAF, ouvintes de rolagem passivos, `will-change` na camada que se move, escrita direta no DOM dentro do rAF (não estado do React a cada quadro). No Safari, prefira uma biblioteca de rolagem suave (Lenis) a `scroll-behavior`.
- **Coreografia:** tudo em cascata (nada se move ao mesmo tempo); variação de velocidade (entrada rápida de 200 a 300 ms + assentamento lento de 500 a 800 ms); a suavização define a personalidade (`cubic-bezier(0.16,1,0.3,1)` ultrapassagem suave, `(0.77,0,0.175,1)` ágil, `(0.33,1,0.68,1)` saída elegante); revelações com clip-path; texto dividido; momentos magnéticos ou que seguem o cursor.

**Microdetalhes de acabamento que sinalizam premium:** cursor personalizado; uma linha sutil de
progresso da rolagem; carregamento desenhado (esqueletos que acompanham o layout, não indicadores
giratórios); hover/ativo/foco bem pensados; border-radius usado com parcimônia e coerência (0
cortante para o editorial, ou um raio específico; nunca 8px padrão em tudo); sobreposição de
granulado/ruído em SVG para dar calor; `::selection` estilizado; barra de rolagem webkit estilizada.

---

## Implementação conforme a stack

Esta skill se adapta à stack: o acabamento é idêntico, e o destino da saída segue a receita ou o
briefing:

- **Página única publicável (PADRÃO)**: `index.html` + `style.css` + um pequeno `script.js`, mais a mídia gerada em `assets/`. Publicável em qualquer lugar, leve, sem build. É o padrão para negócio local ou página de captura (e combina com a receita de site do Etna). Variáveis CSS para os tokens; fontes carregadas cedo por `<link>`/`@import` com uma pilha de reserva de verdade.
- **React / Next**: quando a receita ou o briefing pedir um app ou portfólio com interação mais rica. Exportação padrão, sem props obrigatórias; `import React` junto dos hooks; variáveis CSS para o tema; `IntersectionObserver` por `useRef`/`useEffect`. Evite fragmentos JSX onde o ambiente não os interpreta.

```css
:root {
  --color-bg: #FAF9F6; --color-text: #1A1A1A; --color-text-muted: #6B6B6B;
  --color-accent: #C8553D;
  --font-display: 'Instrument Serif', Georgia, serif;
  --font-body: 'DM Sans', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --space-unit: clamp(1rem, 2vw, 2rem);
}
```

Bibliotecas quando for React: `lucide-react` para ícones (com parcimônia: excesso de ícones é sinal
de IA); `recharts`/`d3` para gráficos; uma biblioteca de rolagem suave para o trabalho de rolagem.
**Nenhuma dependência de incorporação de mídia de terceiros**: a mídia é gerada e hospedada por
você em `assets/`.

---

## O briefing deve ser um checklist, não um parágrafo

O briefing interno de uma construção premium (o `prompt.md` / `[ESCOPO]` que o worker escreve
antes de construir) só está "pronto" quando cada item tem resposta concreta. Respostas vagas
("paleta quente", "algum movimento") são rejeitadas.

1. **Ramo e assunto**: o setor + o produto ou assunto específico; por que é uma marca real e plausível.
2. **Plano de mídia própria**: o tratamento do hero conforme o nível de provedores (vídeo / imagem / código); para mídia gerada, o assunto literal ao tema + o tratamento de cor (paleta e luz combinando com o fundo); a lista de todo espaço de imagem que precisa de geração própria (o site inteiro, não só o hero).
3. **DNA estrutural**: o conceito escolhido, pelo nome; o DNA do site anterior; confirmação de que é distinto.
4. **Direção de design**: de 3 a 5 referências de categoria nomeadas (direção, não cópia); o único movimento tomado de cada uma.
5. **Paleta**: 4 a 6 cores hex com papéis (fundo / tinta / acento / secundária).
6. **Pilha de fontes**: título / corpo / monoespaçada, pelo nome; nenhuma da lista proibida.
7. **Padrão de navegação**: qual variante; explicitamente não a barra superior padrão, a menos que seja realmente a certa.
8. **Voz da marca**: de 3 a 5 frases; o que esta marca NÃO diz.
9. **Estrutura, toda seção**: nome, posição, conteúdo, extensão (um briefing de 6 seções → um site de 6 seções).
10. **Ganchos de texto**: ≥3 linhas literais (título do hero, uma citação destacada, uma frase de fechamento).
11. **Movimento**: 1 entrada do hero + 1 comportamento de rolagem + 1 microinteração; sem repetir o do último site.
12. **Jogadas proibidas**: cores, estruturas e padrões que este site NÃO pode usar.
13. **Ponto de conferência da renderização**: a captura de tela a tirar depois de construir e o modo de falha a vigiar.

---

## Processo

1. **Absorva o briefing, começando pelo ramo.** Marca, público, propósito, ramo. Peça fotos do produto, vídeo da marca ou outros recursos do cliente antes de gerar.
2. **Escolha o DNA estrutural pelo nome**, no catálogo; confirme que difere do site anterior desta sessão; escreva-o com uma frase de justificativa.
3. **Planeje a mídia própria.** Consulte `etna_midia_provedores`; escolha o nível do hero (vídeo / imagem / código). Para mídia gerada, passe para a `etna-cinema-shot` (+ `etna-site-encode` para vídeo, ou `etna-site-scrub` para heros de rolagem) com um prompt literal ao tema e na identidade da marca. Cada espaço de imagem (hero + cards + galeria) é uma geração própria: abra em paralelo, nunca um worker só em laço.
4. **Monte o sistema tipográfico e a paleta**: fontes adequadas ao ramo (fora da lista proibida) + uma paleta contida com um único momento de contraste.
5. **Monte a estrutura** na stack escolhida (HTML de página única por padrão, ou React/Next), com a grade quebrada de propósito e espaço em branco generoso.
6. **Coreografe rolagem e movimento**: de 2 a 3 técnicas distintas, marcadas por rAF, em cascata.
7. **Seja obsessivo com os microdetalhes**: cursor, seleção, barra de rolagem, granulado, estados bem pensados.
8. **Verifique a renderização. Não é opcional.** Suba a pré-visualização, espere a mídia carregar, **tire a captura e olhe**: a mídia gerada está na identidade da marca, proporcional, inteira, com o tratamento de cor combinando com o fundo; todo espaço de imagem renderizou; links e chamadas para ação funcionam. Conserte antes de dizer que terminou.

Nunca narre "pesquisando concorrentes" ou "gerando mídia"; simplesmente execute com acabamento. O
design fala por si.

---

## Origem (por que esta skill é limpa)

Esta skill é **original do Etna**. Reescreve, na nossa voz, uma doutrina de acabamento em design
web premium e **troca toda dependência de mídia de terceiros** (incorporações 3D proprietárias,
captura de URL de cenas de sites ao vivo, banco de imagens por link externo) pela **pilha de
geração própria** do Etna (`etna_imagem_gerar` / `etna_video_gerar`, pelas skills de
cinema/rolagem/codificação) e por visuais escritos em código. Marcas reais aparecem só como
*direção de estudo*, nunca copiadas. Nenhum recurso externo é incorporado, copiado ou usado por
link externo; assim a entrega é distribuível e livre de problemas de propriedade intelectual.
