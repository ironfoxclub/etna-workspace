---
name: etna-site-scrub
description: "Use when a squad worker must PLAN and GENERATE a scroll-driven web hero — a scrub clip the user plays by scrolling, a seamless background loop, or a short hero clip for a site. Owns the scrub contract (one continuous take, zero stillness, constant pace), the 2-KEYFRAME KLING technique (start_image + end_image interpolation via etna_video_gerar's endImageUrl) for a deliberate landing state, real-subject face-ref via imageUrl, and the web-motion anti-patterns. Bind to the site DP / director worker — NOT the orchestrator. Triggers: scrub hero, scroll-driven, scrollytelling, scrubbable, background loop, hero clip, web motion, scroll = time, keyframe interpolation, start/end frame, Kling."
---

> **Mídia no Etna (vale sobre qualquer outra menção neste arquivo).** Ferramentas MCP do Etna: `etna_imagem_gerar(prompt, outPath, provider?, imageUrl?, formato?)`, `etna_video_gerar(prompt, outPath, provider?, imageUrl?, endImageUrl?, formato?, segundos?)`, `etna_voz_gerar(prompt, outPath, voiceId?)` e `etna_midia_provedores()` (quem está pronto, a escolha da pessoa e o modelo de cada um; nunca mostra chave). Provedores: imagem = `antigravity` (padrão, plano do Google, sem chave) | `higgsfield` | `gemini` | `openai` | `fal`; vídeo = `higgsfield` (Seedance) | `fal` (Kling: o único que respeita `endImageUrl`, e o Etna já o escolhe sozinho quando você passa `endImageUrl`); voz = `elevenlabs`. Não passe `provider` a menos que a tarefa exija: vale a IA que a pessoa escolheu em Configurações › Imagem e vídeo. O Antigravity NÃO gera vídeo. `outPath` é relativo à pasta do painel. Sem provedor pronto a ferramenta diz o que falta: pare e avise a pessoa; nunca troque de motor em silêncio. Os nomes antigos (`google-image`, `openai-image`, `replicate-video`, `selectedModel`/`enabledModels`) = `antigravity`/`gemini`, `openai`, `fal` e o campo `modelo` de `etna_midia_provedores`.


# etna-site-scrub — Movimento web guiado pela rolagem

A skill de ofício para **movimento web**: heróis que o visitante toca *rolando*, loops contínuos de fundo e clipes
curtos de capa. É um bicho diferente do vídeo narrativo: não há cortes, nem arco de cenas, nem molduras de
imobilidade. A posição da rolagem É a linha do tempo. Cada quadro tem que merecer a sua distância de rolagem.

> **Decida o MODO primeiro (veja a tabela de três modos abaixo).** Um scrub é ou de CORTE SECO (modo 1: clipes
> separados, com cortes editados) ou CONTÍNUO (modo 2: uma transformação simples; modo 3: um plano-sequência
> contínuo passando por várias batidas diferentes). O padrão rico para uma cena de marca é o **modo 3: um
> plano-sequência contínuo que atravessa N batidas realmente diferentes** (sala → mãos → despejo → xícara → creme),
> sem corte, sem fusão, unido por uma única jornada de câmera fluida. ZERO imobilidade do começo ao fim. As duas
> falhas a evitar: (a) fatiar UMA transformação em N "planos" (= "5 quadros do mesmo plano"); (b) inventar uma fusão
> cruzada: ela não é corte nem continuidade, não existe aqui.

---

## O que é um herói de scrub

Um **herói de scrub** é uma **sequência numerada de imagens ligada à rolagem**: a posição da rolagem mapeia para um
*índice de quadro* (`frameIndex = round(fraçãoDaRolagem * (N - 1))`) e a página troca `frames/0042.jpg` num
`<img>`/canvas conforme você rola. **NÃO é um MP4 embutido num `<video>` com `currentTime` comandado pela rolagem**:
um clipe cru buscado a cada tique de rolagem engasga e atrasa no navegador (os builds de referência do mercado
bateram nisso e todos convergiram para sequência de imagens; veja `etna-site-encode`). Os clipes que você gera são um
*intermediário* do qual você EXTRAI os quadros; o entregável web é a sequência numerada. Ela é consumida **quadro a
quadro**, então:

- **Cada posição da linha do tempo tem que mostrar um quadro diferente e significativo.** Cada fração da rolagem cai
  num quadro real e ordenado da sequência.
- **Modo 3 (padrão) = plano-sequência contínuo por N batidas diferentes.** N quadros-chave de batida (cada um um
  enquadramento / sujeito / escala realmente diferente), ligados por UMA jornada de câmera fluida; o Kling encadeia os
  segmentos (batida k → batida k+1), então a fronteira é uma continuação sem emenda, nem corte nem fusão. (Modo 1 =
  cortes secos entre clipes separados; modo 2 = uma transformação simples, 2 quadros-chave.)
- **ZERO imobilidade, em todo o trajeto.** Pose parada ou "quadro bonito" é rolagem morta. Câmera e sujeito avançam
  quadro a quadro do começo ao fim; nada de moldura de imobilidade (isso é hábito de corte narrativo, errado para a
  rolagem).
- **Velocidade constante.** A distância de rolagem tem que parecer linear, então o movimento avança num ritmo
  aproximadamente constante do início ao fim do plano-sequência. Sem pausa, sem voltar ao início, sem loop, sem
  easing que trava no meio de uma batida.

> **Cheiro de falha de scrub:** "tosca, parada, sem ação": uma cena estática e sem graça. Se quem revisa pode pausar em
> qualquer ponto e ela parece igual a qualquer outro momento, não dá para rolar. Um clipe descrito como "ela está na
> sala de servidores, luzes brilhando" é **um quadro esticado por N segundos**: replaneje como movimento progressivo
> contínuo antes de gerar.

### Os três formatos de movimento web

**Um herói de scrub é UM de TRÊS modos. O diretor escolhe por UMA pergunta: corte seco ou continuidade?**

| Modo | Corte? | Ligação / realização | Quadros-chave |
|---|---|---|---|
| **1: montagem de cortes** | cortes SECOS | N clipes **independentes**, cortados secos na edição, extraídos numa sequência numerada (cada corte é uma fronteira de quadro) | cada plano = 2 quadros-chave (INÍCIO + FIM); N planos ⇒ 2N quadros-chave, N clipes |
| **2: plano-sequência simples** | não: continuidade | UMA transformação contínua de um sujeito; 1 clipe, o Kling interpola INÍCIO→FIM | **2** (INÍCIO + FIM) |
| **3: plano-sequência de várias batidas (PADRÃO para cena rica)** | não: continuidade | UM plano-sequência contínuo passando por N batidas **diferentes**; N quadros-chave de batida (cada um img2img ← a scene-key para a correção de cor), N−1 segmentos Kling ENCADEADOS (fim do seg k = início do seg k+1 = o quadro-chave compartilhado), concatenados SEM fusão e SEM corte → uma jornada contínua | **N** batidas (kf1…kfN) |
| **Loop de fundo** | n/a | `loop muted autoplay playsinline` | contínuo: último ≈ primeiro |
| **Clipe de capa** | n/a | `autoplay muted playsinline` (toca uma vez) | um movimento sustentado |

Toda ligação de scrub = sequência numerada de imagens (`frame = round(fraçãoDaRolagem·(N−1))` → troca de `<img>`/canvas).
A **regra de decisão:**
- **Quer corte seco?** → Modo 1 (clipes separados, cortes editados).
- **Continuidade, uma transformação simples?** (o café, de grão a brilho) → Modo 2 (2 quadros-chave).
- **Continuidade, várias batidas diferentes?** (uma jornada de câmera contínua: ombro → voo → pouso; ou o café: sala →
  mãos → despejo → xícara → creme) → **Modo 3**: o padrão rico para uma cena de marca.

> **NÃO existe modo de fusão cruzada.** Um scrub é ou de CORTE SECO (modo 1) ou CONTÍNUO (modos 2/3). A fusão cruzada
> não é nenhum dos dois: não a introduza.

Esta skill planeja e gera todos esses. A **codificação** para a web (mp4 + webm + capa, mudo, faststart, para loops e
clipes de capa; e **extração de quadros → sequência numerada** para o scrub) é do `etna-site-encode`.

---

## ESCREVA O PROMPT DE EXECUÇÃO PRIMEIRO (Camada 2): antes de qualquer chamada de geração

> **A falha de processo nº 1.** Um scrub vai do briefing direto para o `etna_imagem_gerar` com um prompt fino de uma
> linha → quadros-chave fracos → herói tosco, com cara de estático. **Nunca dispare uma ferramenta de mídia com um
> prompt de uma linha. Você escreve o prompt cinematográfico de execução completo primeiro, mostra, e DEPOIS gera.**
> Isso espelha a disciplina da Camada 2 da equipe de cinema: a Camada 1 é o briefing em prosa ("um caderno que se abre
> num mundo de código vivo"); a **Camada 2 é o prompt de execução no nível de plano de filme**, e a ferramenta de
> geração só recebe a Camada 2.

O vocabulário de ofício da Camada 2 é o do **`etna-cinema-shot`**: o catálogo de movimentos de câmera (~70 movimentos
nomeados), as escadas de lente e tamanho de plano, o vocabulário de luz, a tabela de correção de cor e o portão de
lint. Use-o. Não reinvente o ofício de prompt; esta skill é dona do *contrato do movimento web*, e o cinema-shot é dono
da *string do prompt*.

**Antes de gerar QUALQUER coisa, escreva e MOSTRE três prompts de execução:**

1. **Prompt do quadro-chave de INÍCIO (o estado de 0%).** Prompt completo de imagem: tamanho de plano + ângulo + sujeito + cenário + luz + correção de cor. Concreto, de marca, sem clichê.
2. **Prompt do quadro-chave de FIM (o estado de 100%).** Escrito como uma edição img2img a partir do INÍCIO: nomeie só o que *mudou/avançou* (a câmera atravessou, a luz subiu, o mundo se acendeu). Mesmo mundo, muito mais adiante.
3. **Prompt de MOVIMENTO (o vídeo).** Só a transição: o **movimento de câmera nomeado** (do catálogo do cinema-shot), a nota de lente/tamanho de plano, o que avança monotonicamente entre os dois quadros, a correção de cor. NADA de redescrever a composição estática (os quadros-chave já a fixam).

Cada prompt nomeia, explicitamente: **movimento de câmera (nomeado)** · **lente / tamanho de plano** · **luz** · **composição** · **correção de cor** e, para o par, **o arco INÍCIO↔FIM numa linha**. Rode o **portão de lint** do cinema-shot em cada prompt antes de disparar.

```
Fase 1a: ESCREVER (sem chamadas de ferramenta): para CADA plano escreva o prompt de INÍCIO, de FIM e de MOVIMENTO
         (+ o prompt da scene-key, para uma montagem). Mostre todos. Faça o lint de cada um.
Fase 1b: GERAR: [montagem] scene-key primeiro; depois, por plano: kf_inicio (img2img ← scene-key),
         kf_fim (img2img ← kf_inicio). [1 plano] kf_inicio (novo/ancorado), kf_fim (img2img ← kf_inicio).
         Exatamente 2 quadros-chave por plano: nunca 5. PARE para aprovação humana de todos os quadros-chave.
Fase 2:  MOVIMENTO: com a aprovação, UM clipe Kling por plano:
         etna_video_gerar(imageUrl=kf_inicio, endImageUrl=kf_fim, prompt=MOVIMENTO). N planos ⇒ N clipes.
```

**Regra firme: nunca dispare `etna_imagem_gerar` / `etna_video_gerar` com um prompt de 1 linha. Escreva primeiro o
prompt cinematográfico de execução (Camada 2), mostre, faça o lint e só então dispare.**

---

## O ARCO TEM QUE SER UMA TRANSFORMAÇÃO: início ≠ fim (a regra do arco dramático)

Um scrub em que 0% e 100% parecem *o mesmo plano levemente ajustado* (por exemplo, "um notebook, com a tampa um pouco
mais aberta") é um **arco fracassado**: não há nada para rolar. INÍCIO e FIM têm que ser **visivelmente, dramaticamente
distintos**: um estado de luz diferente, uma escala diferente, um mundo diferente revelado. Quem rola do topo ao fim
tem que sentir uma *transformação* cinematográfica de verdade, e **um movimento de câmera marcado** tem que carregá-la.

**O arco precisa DOS DOIS:**
1. **Uma transformação visual**: o FIM é um estado visual diferente, não um ângulo diferente. Luz: escuro → ardente.
   Escala: objeto externo → por dentro dele. Estado: adormecido → vivo / aceso / montado.
2. **Um movimento de câmera marcado** que faz a viagem: escolha UM, nomeado (catálogo do cinema-shot): **atravessar
   empurrando para dentro da tela** (`Through Object In`), **zoom brusco** até o núcleo, **revelação de grua** subindo
   sobre o mundo, **travelling pela fresta / costura de luz**. Não um "empurrão lento" tímido: um movimento com destino.

**Três exemplos de arco forte (use como modelo):**

| 0% (INÍCIO) | Movimento de câmera | 100% (FIM) |
|---|---|---|
| Um notebook escuro e fechado sobre a mesa, uma borda fria de luz ao longo da fresta da tampa, quadro quase preto | **Travelling pela fresta de luz** (`Through Object In`): a câmera mergulha na rachadura que se abre | A câmera já atravessou a tela e entrou num mundo vasto e vivo de luz de código quente e fluindo; a mesa escura sumiu |
| Extra-aberto: uma figura minúscula na entrada de um corredor escuro de servidores, um brilho ciano distante | **Zoom brusco + grua descendo** o corredor até o brilho | Fechado no núcleo luminoso, as paredes do corredor agora em fluxos de dados ardendo e passando rápido: a escala colapsou de plano extra-aberto para primeiríssimo plano |
| Um único componente adormecido sobre concreto fosco, luz de céu nublado e chapada | **Empurrão / mergulho macro** no componente | Dentro de uma máquina luminosa e intrincada no meio da montagem, peças travando umas nas outras, luz subindo de fria para quente |

Cada INÍCIO↔FIM é uma transformação genuína, não um ângulo de tampa. O movimento de câmera é a espinha; a mudança do
mundo é a carga útil. Fixe os dois extremos como quadros-chave (Kling de 2 quadros, abaixo) para que a chegada
dramática seja autorada, não torcida.

---

## COMO CADA MODO É REALIZADO (a espinha)

> **DECIDA O MODO PRIMEIRO: corte seco ou continuidade?** (tabela completa no topo.) Depois NUNCA fatie UMA
> transformação em N "planos": um conceito que é uma transformação contínua de um sujeito só (café sendo despejado;
> um grão se dissolvendo; um logo se formando) é **modo 2: 1 plano, 2 quadros-chave**, e o Kling interpola. Cortar isso
> em "5 planos" gera 5 quadros quase idênticos = **"5 quadros pro mesmo plano"** (a falha do café "O Rito"). Várias
> batidas **realmente diferentes** (sala → mãos → despejo → xícara → creme) = modo 1 (corte) ou **modo 3 (plano-sequência
> contínuo)**. **Teste de distinção: se duas batidas podem ser quadros do mesmo zoom contínuo, são a mesma batida.**

> **REGRA CARDINAL: um render nunca está a mais de 2 gerações da scene-key, e você escala adicionando BATIDAS/PLANOS,
> nunca quadros-chave por plano.** Modo 2 = 2 renders. Modo 1 = 2 quadros-chave × N planos. Modo 3 = N quadros-chave
> de batida. Renderizar 5 imagens paradas de UM plano é o erro desperdiçador e propenso a deriva.

**A scene-key fixa a CORREÇÃO DE COR (todo modo).** Gere-a PRIMEIRO (`etna_imagem_gerar`, nova; rosto real → ancore na
foto real via `imageUrl`): identidade do sujeito, paleta, linguagem de luz, proporção. Todo quadro-chave é img2img **a
partir da scene-key** (profundidade ≤ 2; para um quadro FINAL no modo 1/2, a partir do próprio INÍCIO). **NUNCA
encadeie um quadro-chave a partir do quadro de outra batida**: é a deriva que fez o café virar cara de IA. A scene-key
é o que faz N batidas diferentes parecerem UM mundo só.

### Modo 3: plano-sequência contínuo de várias batidas (o padrão rico)

```
scene-key                         (nova: correção de cor: identidade, paleta, luz, proporção)
  ├─ kf1 = img2img ← scene-key    (enquadramento da batida 1: sala ABERTA)
  ├─ kf2 = img2img ← scene-key    (enquadramento da batida 2: mãos MÉDIO)   ← cada batida a partir da scene-key, NÃO de kf1
  ├─ …
  └─ kfN = img2img ← scene-key    (enquadramento da batida N)
segmentos (ENCADEADOS, continuidade): seg_k = Kling(imageUrl=kf_k, endImageUrl=kf_{k+1})
  → quadro final de seg_k = início de seg_{k+1} = o quadro-chave compartilhado kf_{k+1} (a ponte de continuidade)
```

1. **Ordene as batidas para que a câmera possa FISICAMENTE VIAJAR entre elas** (sala → empurra até o balcão → desce até
   o despejo → sobe até a xícara → desce sobre o creme). Batidas consecutivas precisam ser ligáveis por câmera: é isso
   que faz a interpolação do Kling ler como uma jornada crível, e não como uma metamorfose.
2. **Gere N quadros-chave de batida, cada um img2img a partir da scene-key**: enquadramento / sujeito / escala diferentes
   por batida, mesma correção de cor. (Profundidade 1 a partir da scene-key: ainda mais seguro que a profundidade 2 do
   modo 1.)
3. **Encadeie N−1 segmentos Kling.** `seg_k = etna_video_gerar(imageUrl=kf_k, endImageUrl=kf_{k+1}, prompt="<o movimento de câmera que LIGA a batida k → k+1>")`. O quadro compartilhado é a ponte de continuidade: seg_k termina exatamente onde seg_{k+1} começa.
4. **O editor concatena os segmentos SEM fusão e SEM corte** (`etna-site-encode`): como as pontes já alinham, é concatenação simples → uma sequência numerada contínua `0000.jpg … NNNN.jpg`.
5. **Ligue rolagem → índice de quadro.** `frameIndex = round(fraçãoDaRolagem * (N-1))`; troque o `<img>`/canvas. A rolagem inteira é um voo de câmera contínuo pelo mundo da marca.

### Modo 1: montagem de cortes (clipes separados)

Cada plano é independente: `inicio_plano` (img2img ← scene-key) + `fim_plano` (img2img ← o próprio `inicio_plano`) + UM
clipe Kling por plano. O editor CORTA SECO os clipes em sequência (cada corte é uma fronteira de quadro) e extrai uma
sequência numerada única. Use quando se quer uma sensação editada e marcante em vez de continuidade.

### Modo 2: plano-sequência simples (uma transformação)

`kf_inicio` (novo ou img2img ← scene-key) + `kf_fim` (img2img ← kf_inicio) + UM clipe Kling. O Kling interpola
INÍCIO→FIM. A execução honesta de uma única transformação contínua: 2 renders, nunca 5.

> **Por que isso acaba com os bugs antigos:** todo quadro-chave fica a no máximo 2 gerações da scene-key (sem deriva
> acumulada → sem colapso para cara de IA), as batidas são realmente diferentes (sem "5 quadros do mesmo plano") e a
> continuidade (modo 3) é gerada pela interpolação encadeada do Kling, não forjada por uma fusão.

---

## A TÉCNICA KLING DE 2 QUADROS-CHAVE (movimento controlado para UM plano)

É assim que você gera o movimento controlado de **um plano/batida**: os quadros intermediários entre o INÍCIO e o FIM
dele. UM clipe por plano/batida; um scrub de vários planos encadeia N desses, unidos conforme o MODO pelo editor (modo 3:
concatenação simples dos segmentos encadeados, sem fusão; modo 1: concatenação de corte seco). É **possível** porque
`etna_video_gerar` tem um parâmetro `endImageUrl`.

> `etna_video_gerar(prompt, outPath, imageUrl, endImageUrl)`
>
> Os modelos Kling (`kwaivgi/kling-v3-video`, `kling-v3-omni`, `kling-v2.1`) aceitam **imagem inicial + imagem final** e
> interpolam um movimento **controlado** do quadro inicial até o quadro final. Passe os DOIS `imageUrl` (INÍCIO) e
> `endImageUrl` (FIM) e o modelo pousa num estado final **deliberado**: sem deriva, sem surgimento brusco, sem final
> aleatório. `endImageUrl` é **ignorado por modelos que não são Kling**.

**O fluxo (use em qualquer scrub ou herói com que você se importe):**

```
1. Gere o quadro-chave INÍCIO  → etna_imagem_gerar → inicio.png   (o estado de 0%)
2. Gere o quadro-chave FIM     → etna_imagem_gerar(imageUrl=inicio.png, ...)  → fim.png
       img2img A PARTIR do início para que o visual / a identidade / o enquadramento se mantenham → o FIM é o MESMO mundo, avançado
3. Gere o movimento            → etna_video_gerar(
                                    imageUrl=inicio.png,
                                    endImageUrl=fim.png,
                                    prompt="<SÓ o que MEXE entre os dois quadros>")
```

**Por que fim.png é img2img de inicio.png, e não uma geração nova.** Os dois quadros-chave têm que ser *o mesmo mundo em
dois estados*: mesmo sujeito, mesma paleta, mesma lente, mesmo cenário, avançado. Gerar o FIM do zero (texto-para-imagem)
rerola identidade e enquadramento, e a interpolação então faz metamorfose entre dois mundos diferentes. Ancore o FIM no
INÍCIO com `imageUrl=inicio.png` e mude só a única coisa que progride (a câmera avançou; a máquina se montou; a luz
subiu; o logo se formou).

**O prompt descreve SÓ o MOVIMENTO.** Os dois extremos já estão fixados pelos quadros-chave. O prompt é a *transição*:
"empurrão contínuo e lento; a estrutura se monta peça por peça; a luz sobe de fria para quente". NÃO redescreva a
composição estática de nenhum dos quadros: isso briga com os quadros-chave e faz o modelo reencenar.

> **Resultado:** um clipe que começa num quadro que você escolheu, termina num quadro que você escolheu e se move entre
> eles num arco controlado e monotônico: UM plano/batida realizado. No giro do modo 2, esse clipe único É o scrub
> inteiro. No modo 3, gere um segmento por par de batidas (kf_k→kf_{k+1}) e o editor concatena simples os segmentos
> encadeados numa sequência numerada (sem fusão: as pontes já alinham); no modo 1, o editor concatena com corte seco os
> clipes de cada plano. Essa extração, e não um único MP4 embutido, é o entregável web.

**Quando você só tem um início (sem fim definido):** passe só `imageUrl` com um prompt forte de movimento contínuo. Você
ganha um arco monotônico, mas a chegada é escolha do modelo: aceitável para um loop de fundo, arriscado para um scrub em
que o quadro final importa. Prefira dois quadros-chave sempre que o estado final for estrutural.

---

## Sujeitos reais: rosto via imageUrl, vídeo via Kling

Quando o herói traz uma **pessoa real** (um fundador, um rosto de foto):

1. **Ancore o rosto.** Passe a foto real (ou uma imagem gerada do personagem) como `imageUrl`: o quadro-chave de INÍCIO carrega a identidade. Nunca descreva um rosto real em texto-para-vídeo e torça; não será aquela pessoa.
2. **Provedor de vídeo = Kling.** O Kling anima um rosto real sem problema. **O Seedance modera rostos reais e devolve E005** ("moderação de conteúdo" / rejeição de rosto): não mande clipe de sujeito real para o Seedance. (O Seedance serve para heróis de objeto/produto/abstrato sem rosto.)
3. **A identidade fica nos quadros-chave, o movimento fica no prompt.** A mesma divisão da equipe de cinema: o PNG carrega o rosto; o prompt carrega só o que se move. Reler descritores de rosto no meio do clipe deforma o rosto.

| Sujeito no herói | Provedor de imagem dos quadros-chave | Provedor de vídeo |
|---|---|---|
| Pessoa real / rosto real | `openai` ou `antigravity` para a imagem fixa, ancorada na foto real via `imageUrl` | **Kling** (`fal`): anima rostos reais, sem E005 |
| Produto / objeto / abstrato / tipo / UI | qualquer um dos provedores de imagem, pelo visual | Seedance OU Kling (Kling se quiser controle de 2 quadros) |

> O Kling roda pelo provedor `fal`: com `endImageUrl` o Etna já o escolhe sozinho.
> **Confira antes de sinalizar qualquer coisa: chame `etna_midia_provedores` e veja se o `fal` está pronto e qual o `modelo`.**
> Se o fal já estiver pronto, NÃO há lacuna: diga isso ao worker de renderização para que o `endImageUrl` seja respeitado, e filme.
> **Use só modelos ligados: só SINALIZE uma lacuna quando o modelo ligado realmente não consegue fazer o plano (por
> exemplo, você precisa da interpolação de 2 quadros com `endImageUrl` mas nenhum Kling está ligado); nunca troque em
> silêncio por outra versão do Kling (ou por qualquer outro modelo).** "Disponível" ≠ "ligado", e "já existe um Kling
> ligado" ≠ "bloqueio": não invente uma lacuna de "troque seu modelo" contra um modelo que você nunca conferiu.

---

## Câmera = UM movimento contínuo que nunca para

A câmera é a espinha da legibilidade do scrub. **Um** movimento suave e contínuo, velocidade constante, nunca estaciona:

- **empurrão / travelling para dentro** (push-in / dolly-in): a profundidade cresce conforme você rola.
- **travelling / plano lateral** (dolly / truck): o mundo desliza por você.
- **atravessar com paralaxe** (parallax push-through): o primeiro plano e o fundo se separam em ritmos diferentes (lê como "rolar = viajar", o mais forte).
- **órbita / arco lento**: revela a forma do sujeito por um ângulo contínuo.
- **grua para cima / para baixo** (crane up / down): revelação vertical.

Nunca empilhe movimentos (nada de "empurrão e depois panorâmica rápida"): isso são duas tomadas fingindo ser uma só, e
quebra a sensação de velocidade constante. Nunca deixe a câmera parar: câmera estacionada no meio do scrub é rolagem
morta.

O **movimento do sujeito** (se houver) cresce de forma monotônica junto com a câmera: montagem, revelação,
transformação, aproximação, ignição, crescimento. Só avança; nunca volta ao início.

---

## Antipadrões (são falhas de processo para web: devolva-os)

| Antipadrão | Por que é errado para web | Conserto |
|---|---|---|
| **Cena estática / "quadro bonito"** | Nada para rolar: rolagem morta o tempo todo | Replaneje como movimento progressivo contínuo (câmera e sujeito avançando) |
| **Arco fraco: INÍCIO ≈ FIM** (por exemplo, "a tampa abre um pouco mais") | O mesmo plano levemente empurrado → nenhuma transformação para rolar | Faça 0% e 100% dramaticamente distintos (mudança de luz / escala / mundo) + UM movimento de câmera marcado: veja a regra do arco dramático |
| **Prompt fino de uma linha disparado na ferramenta** | Briefing → geração sem Camada 2 → quadros-chave fracos, herói chapado | Escreva o prompt de execução completo (movimento de câmera nomeado, lente, luz, composição, correção de cor) PRIMEIRO, mostre, faça o lint, e SÓ ENTÃO gere |
| **Fatiar UMA transformação em N "planos"** | 5 imagens paradas do mesmo sujeito / movimento = "5 quadros pro mesmo plano": chapado, monótono, E encadeia até virar cara de IA (a falha do café "O Rito") | Uma transformação = modo 2 (1 plano, 2 quadros-chave). Para riqueza, use batidas DIFERENTES (modo 3), nunca N fatias de uma |
| **Encadeamento entre renders (uma batida ← quadro de outra batida)** | A deriva se acumula; na 4ª–5ª geração o mundo pula para outro estilo / proporção (café KF4 → brilho abstrato) | Profundidade ≤ 2: todo quadro-chave ← a scene-key (um FIM ← o próprio INÍCIO). Nenhuma batida é gerada a partir de outra |
| **Fusão cruzada entre planos** | Uma fusão não é corte seco nem continuidade verdadeira: é um truque que não existe neste modelo | Modo 1 = corte SECO (clipes separados). Modo 3 = CONTÍNUO (segmentos Kling encadeados, sem fusão). Escolha um |
| **Batidas que não são ligáveis por câmera (modo 3)** | Se batidas consecutivas não podem ser unidas por um movimento de câmera crível, o Kling metamorfoseia em vez de viajar | Ordene as batidas como uma jornada física de câmera (sala → balcão → despejo → xícara → creme); cada par ligável |
| **Um único take monótono para uma CENA de marca** | Um empurrão só num sujeito só não sustenta uma história; parece barato | Modo 3: um plano-sequência contínuo por várias batidas DIFERENTES. Take único (modo 2) só para uma transformação literal |
| **MP4 embutido num `<video>` rolado por `currentTime`** | O clipe cru busca a cada tique de rolagem → travamento / atraso no navegador | A saída web = sequência numerada de imagens (rolagem → índice de quadro); o MP4 é um intermediário de extração |
| **Surgimento brusco de elementos discretos** | Elementos piscam para existir → parece quebrado, não autorado | Use Kling de 2 quadros para que os elementos estejam presentes / se formando nos dois quadros e interpolem suavemente |
| **Clichê de capuz de hacker / chuva estilo Matrix / "tecnologia" genérica** | Visual de cara de IA com molde; sinal de pouco esforço | Descreva um mundo específico, concreto e de marca: cenário real, luz real, sujeito real |
| **t2v sem âncora (texto-para-vídeo, sem imageUrl)** | O sujeito deriva; um rosto real não vai ser a pessoa; o fim é aleatório | Ancore sempre: `imageUrl` no início (+ `endImageUrl` no fim, para controle) |
| **Moldura de imobilidade (hábito de corte narrativo)** | Início e fim parados = faixa de rolagem morta nas posições mais vistas do scrub | Movimento do quadro 1 até o último; zero momentos parados |
| **Loop que volta ao início no meio do clipe** | O scrub volta para trás; lê como glitch | Só arco monotônico; para um loop de *fundo*, faça o último quadro ≈ o primeiro com movimento cíclico suave, não um retorno brusco |
| **Ligação errada para o modo** | Misturar modos (uma fusão, ou um corte dentro de um plano-sequência contínuo) quebra a leitura | Modo 1 = cortes secos (intencionais). Modo 3 = contínuo, segmentos encadeados, SEM corte e SEM fusão. Nunca misture os dois |

---

## Autoverificação antes de disparar (o lint do scrub)

Antes de gastar uma geração, confirme:

- [ ] **Prompt de execução escrito primeiro**: o prompt completo da Camada 2 (movimento de câmera nomeado, lente / tamanho de plano, luz, composição, correção de cor) está escrito e mostrado ANTES da chamada da ferramenta. Nada de uma linha.
- [ ] **Arco dramático**: INÍCIO e FIM são visivelmente distintos (mudança de luz / escala / mundo), não o mesmo plano empurrado. Um movimento de câmera marcado carrega a transformação.
- [ ] **Modo escolhido (1/2/3)**: corte seco (modo 1), plano-sequência simples (modo 2) ou plano-sequência contínuo de várias batidas (modo 3, o padrão rico). NÃO uma fusão cruzada (ela não existe aqui).
- [ ] **Quantidade certa de quadros-chave para o modo**: modo 2 = 2 quadros-chave; modo 1 = 2 por plano (2N); modo 3 = N quadros-chave de batida. NUNCA 5 imagens paradas de um plano.
- [ ] **Batidas distintas (modo 1/3)**: as batidas são realmente diferentes (enquadramento / sujeito / escala); o teste de distinção passa (duas batidas não podem ser quadros do mesmo zoom). No modo 3, batidas consecutivas são ligáveis por câmera.
- [ ] **Profundidade de âncora ≤ 2 (sem encadeamento)**: todo quadro-chave é img2img a partir do **caminho da scene-key** (um FIM a partir do próprio INÍCIO). Nenhum quadro-chave é gerado a partir do quadro de outra batida. Se foi, regere a partir da scene-key.
- [ ] **Saída web = sequência de imagens (não MP4 embutido)**: o entregável do scrub ligado à rolagem é uma sequência numerada de quadros (`frame = round(fraçãoDaRolagem·(N−1))` → troca de `<img>`/canvas), NÃO um MP4 em `<video>` com `currentTime` pela rolagem. O(s) MP4 são intermediários dos quais se extraem os quadros.
- [ ] **Um movimento de câmera, nunca estacionado**: um único movimento contínuo nomeado, em velocidade constante.
- [ ] **Monotônico**: nada volta ao início; o arco só avança.
- [ ] **Ancorado**: `imageUrl` definido (rosto real → a foto real); para um pouso que sustenta o plano, `endImageUrl` definido também (img2img do início).
- [ ] **Provedor de vídeo certo**: rosto real → Kling (Seedance = E005); objeto → qualquer um.
- [ ] **Prompt = só movimento**: nenhuma redescrição da composição estática que os quadros-chave já fixam.
- [ ] **Nenhum texto nítido na tela**: nenhuma marca, título ou número (por exemplo "R$1M ARR") em nenhum dos prompts de INÍCIO / FIM / MOVIMENTO. A difusão alucina tipografia; TODO texto nítido é composto em código (CSS/Remotion) por cima do clipe mudo. Se o briefing traz texto, mantenha-o FORA da geração.
- [ ] **Proporção fixada na proporção declarada**: o quadro INÍCIO é gerado na proporção que o diretor declarou (por exemplo 16:9). Se voltar outra razão (retrato / quadrado), regere na proporção certa ANTES do FIM e do vídeo: nunca leve uma proporção errada para a geração de movimento, que é cara.
- [ ] **Nada de clichê**: nada de capuz / chuva estilo Matrix / tecnologia genérica; um mundo concreto e de marca.
- [ ] **Mudo por desenho**: heróis web são silenciosos; nenhum plano de áudio aqui (a codificação tira o áudio de qualquer forma).

---

## Vocabulário de composição web (no código, por cima do herói: sem nova geração)

Além do próprio scrub, o visual de herói do mercado é finalizado com **composição de código** barata por cima do clipe /
sequência mudos: nenhuma geração extra, aplicada pelo editor. Conheça estes e cite-os no plano:

- **Máscara de gradiente CSS no herói**: a base do herói passa de sólida a transparente, e o texto por cima "surge do nada" conforme você rola (profundidade falsa 3D + legibilidade). `mask-image: linear-gradient(to bottom, black 60%, transparent)`. É também **onde o texto nítido mora** (a difusão não renderiza tipografia): título / logotipo / contador de ARR são compostos em código por cima do herói mascarado, nunca na geração.
- **Revelação ao passar o mouse (spotlight)**: uma segunda sequência / vídeo fica sob uma máscara radial que segue o cursor (`mask: radial-gradient(circle at var(--mx) var(--my), black 0 120px, transparent 121px)`), revelando um estado escondido sob o ponteiro. Um *formato* de web além do scrub: detalhe no briefing quando o herói quiser revelação interativa.
- **Loop contínuo com fade em JS**: para um *loop de fundo* cuja volta ainda aparece, o site esmaece a cauda no reinício (sem corte seco). A técnica mora no `etna-site-encode` (Tarefa 2, opção C): cite-a no plano; o editor a liga.

> Os três são **composição, não geração**: não custam créditos e rodam sobre o que já foi renderizado. O DP planeja;
> o editor aplica. Mantenha TODO o texto nítido nessa camada.

## Entrega de volta

Via `handoff_submit`: o MODO (1/2/3), o(s) caminho(s) do mp4 em ordem, o PNG da scene-key e os caminhos de todos os
quadros-chave (na ordem de plano / batida), o(s) prompt(s) finais de movimento, o modelo de vídeo usado (Kling ou
Seedance) e por quê, e uma linha por plano / batida (enquadramento + movimento + o que avança). A **codificação para
formatos web** (e, no scrub, a **junção por MODO: modo 3 = concatenação simples dos segmentos encadeados, sem fusão;
modo 1 = concatenação de corte seco** + **extração dos quadros numa sequência numerada** (o entregável rolagem → índice
de quadro)) é trabalho do próximo worker: veja `etna-site-encode`.

## Lacunas de capacidade: sinalize, não finja

- **`endImageUrl` é exclusivo do Kling.** Uma renderização do Seedance ignora sem avisar: você fica só com deriva a partir do início. Se precisa de um pouso controlado, TEM que usar um modelo Kling.
- **O Seedance recusa rostos reais (E005).** Não é problema de prompt: é um portão de moderação. Mande clipes de sujeito real para o Kling; não tente o Seedance de novo.
- **Os provedores de imagem são texto-para-imagem / img2img**: `imageUrl` é a única entrada de imagem. Não há chamada de inpaint nem de máscara; refine um quadro-chave reescrevendo o prompt (aperte uma cláusula, regere).
- **Nenhum texto nítido na tela dentro do clipe.** A difusão alucina tipografia. Um scrub com logotipo / título compõe o texto em código (CSS/Remotion) por cima do clipe mudo: mantenha as palavras fora da geração.
- **A saída web de um scrub é uma sequência numerada de imagens, não um `<video>`.** Embutir o MP4 e rolar o `currentTime` engasga e trava no navegador; extraia os quadros (`etna-site-encode`) e ligue rolagem → índice de quadro. O(s) MP4 são intermediários. (Loops de fundo e clipes de capa continuam saindo como `<video>`: só o scrub é uma sequência.)
