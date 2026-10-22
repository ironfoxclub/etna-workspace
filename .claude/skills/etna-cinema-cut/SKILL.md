---
name: etna-cinema-cut
description: "Use when a squad worker must ASSEMBLE generated clips into a finished video — Bash ffmpeg concat in beat order, last-frame extraction for sequential continuity (feeds the next shot’s imageUrl), and pre-delivery QA (runtime-sum invariant, 2-second-stillness cut landing, double-contrast cut grammar). Bind to an editor / executor worker that has Bash. Triggers: stitch clips, assemble video, ffmpeg concat, final cut, video editing, frame extraction, runtime check."
---

# etna-cinema-cut — O editor (montagem + QA)

O worker que é dono do ffmpeg: ele costura os clipes do Seedance já renderizados num corte final, extrai os
últimos quadros para dar continuidade sequencial, põe a trilha de narração por cima e roda o portão de QA antes
da entrega. Os painéis de renderização gerram; esta skill monta.

> **Divisão de camadas (lei que rege tudo).** Esta skill é dona da **inteligência de montagem e do portão de QA**:
> ordem de corte, extração de quadros, a invariante da soma de duração. As ferramentas do Etna cuidam da geração.
> Você não escreve prompts do Seedance aqui (isso é do **etna-cinema-shot** para imagens e do **etna-cinema-plan**
> para movimento); não gera narração aqui (isso é do **etna-cinema-voice**). Você recebe caminhos de mp4 + uma
> trilha de áudio e produz `final.mp4` com o ffmpeg no Bash. Não existe editor não linear do Etna: a montagem é
> ffmpeg puro, sempre.

Esta skill fica ligada a um **worker editor / executor** com Bash. Ela roda em dois pontos do grafo do time: (1) **no
meio do caminho**, em cada aresta SEQUENCIAL, extraindo o último quadro do plano N-1 para que o próximo worker de
renderização o passe como `imageUrl`; (2) **no fim**, como a passada de montagem: concatena na ordem do corte,
põe o áudio e faz o QA.

---

## O que entra / o que sai

| Entra | Origem |
|---|---|
| Caminhos dos mp4 dos workers (um por plano, mudos) | `handoff_list`: coletados do `handoff_submit` de cada worker de renderização |
| Ordem de corte (sequência de contraste duplo) | A lista de planos do coordenador / arco de 6 cenas |
| Trilha de narração (`narration.mp3`) | **etna-cinema-voice** (`etna_voz_gerar`, TTS da ElevenLabs): trilha SEPARADA, nunca gravada no mp4 |
| Metas de duração por plano | A especificação de planos do coordenador (para a invariante da soma) |

| Sai |
|---|
| `frameN.png`: último quadro extraído, devolvido para o próximo worker SEQUENCIAL passar como `imageUrl` |
| `assembled.mp4`: concatenação muda, na ordem do corte |
| `final.mp4`: vídeo montado + trilha de narração, aprovado no QA |

---

## Tarefa 1: extração do último quadro (a aresta de continuidade sequencial)

O método de continuidade de maior alavanca para qualquer modelo de imagem-para-vídeo: **quadro final do plano A =
quadro inicial do plano B = continuidade sem emenda.** Quando o grafo tem uma aresta SEQUENCIAL (o plano N precisa
da saída do plano N-1), esta skill extrai o último quadro do plano N-1 e devolve o caminho para que o próximo worker
de renderização o passe como `imageUrl` em `etna_video_gerar`. O estilo pode mudar radicalmente de cena para cena,
enquanto personagem, objetos e física (desfoque de movimento, peso, impulso) atravessam o corte. Quadros finais
produzem composições que você nunca pediria diretamente no prompt.

A receita de extração de quadros (literal):

```bash
ffmpeg -sseof -0.1 -i shotN.mp4 -frames:v 1 -q:v 2 frameN.png
```

- `-sseof -0.1` posiciona 0,1 s antes do fim do arquivo → pega o **último** quadro (não o primeiro).
- `-frames:v 1` → exatamente um quadro.
- `-q:v 2` → qualidade de PNG quase sem perda (número baixo = qualidade alta).

Depois, `frameN.png` vira o `imageUrl` do plano N+1. Isso monta sequências longas e conectadas sem nenhum modo de
multi-plano. O worker de renderização que recebe o quadro segue a regra de **apagar a aparência para bater a
referência**: quando há uma âncora `imageUrl` em jogo, ele descreve só o que MEXE, nunca redescreve o rosto (isso é
trabalho do etna-cinema-plan, mas o editor garante que a entrega exista).

> Primeiro quadro, no lugar (raramente necessário, por exemplo para conferir se o estado inicial bate com o último
> quadro anterior): `ffmpeg -i shotN.mp4 -frames:v 1 -q:v 2 firstN.png`.

---

## Tarefa 2: montagem por concatenação (gramática de corte de contraste duplo)

### Sequencie os planos: gramática de corte de contraste duplo

Ordene os planos montados de modo que clipes vizinhos **contrastem em dois eixos ao mesmo tempo** (por exemplo,
aberto → fechado *e* parado → em movimento, ou paleta fria → quente *e* lento → rápido). Um corte que muda duas coisas
de uma vez lê como **edição intencional**; um corte que muda uma só lê como **tremida de continuidade**. A
arquitetura de 6 cenas já alterna tamanho de plano e energia: preserve essa alternância ao sequenciar as saídas dos
workers. Em sequências de ação, em especial, alterne planos de rosto com referência travada e planos de ação só
com texto; o cérebro de quem assiste preenche a continuidade entre os cortes.

### Os cortes caem na imobilidade, não no movimento

Todo worker de renderização é obrigado, por contrato, a emoldurar o plano com um **momento de ~2 segundos parado ou
quase parado no INÍCIO e no FIM de cada plano** (um olhar mantido, uma pose assentada, uma respiração segurada antes
ou depois do movimento). O meio pode ser tão cinético quanto o roteiro exigir; as bordas é que ganham os cortes. O
trabalho do editor é **verificar** que essa imobilidade de borda existe (veja o QA) e fazer cada corte **cair nela**:
os cortes do demuxer de concatenação são cortes secos nas fronteiras dos clipes, e é a imobilidade que torna a
emenda invisível. Se um clipe chega com movimento até o último quadro, o corte vai estalar: devolva ao worker de
renderização (etna-cinema-plan) para pôr uma moldura de imobilidade; não tape isso na edição.

### Passada do demuxer de concatenação

Colete os caminhos dos mp4 com `handoff_list`, escreva uma lista de concatenação na ordem da gramática de corte e
rode o demuxer:

```bash
# concat.txt: uma linha por plano, na ordem do corte de contraste duplo, com caminhos absolutos:
#   file '/abs/path/shot1.mp4'
#   file '/abs/path/shot2.mp4'
#   file '/abs/path/shot3.mp4'
ffmpeg -f concat -safe 0 -i concat.txt -c copy assembled.mp4
```

- `-c copy` → cópia de fluxo, sem reencodar (rápido, sem perda): funciona quando todos os clipes têm o mesmo
  codec/resolução/fps (e têm: todos os mp4 do Seedance).
- `-safe 0` → permite caminhos absolutos na lista.
- Se um clipe tiver um fluxo diferente e o `-c copy` gerar falhas numa emenda, reencode essa passada: tire o
  `-c copy` e deixe o ffmpeg normalizar (`-c:v libx264 -pix_fmt yuv420p`). Reencode é plano B, não o padrão.

### Ponha a trilha de narração

Os mp4 do Seedance são **mudos**: o áudio nunca vem gravado. A narração chega como um `narration.mp3` separado,
vindo do **etna-cinema-voice**. Ponha por último:

```bash
ffmpeg -i assembled.mp4 -i narration.mp3 -c:v copy -c:a aac -shortest final.mp4
```

- `-c:v copy` → não mexe na imagem.
- `-c:a aac` → codifica a faixa de áudio.
- `-shortest` → termina a saída no mais curto dos dois fluxos.

---

## Tarefa 3: portão de QA antes da entrega

Diagnostique antes de enviar. O portão de QA é binário (provado / lacunas catalogadas): escreva-o antes de montar,
para não haver racionalização depois.

### A invariante da soma de duração

**A duração montada TEM que ser igual à soma das durações dos planos** (dentro do arredondamento). Se o
`assembled.mp4` for mais curto que `Σ duração dos planos`, um clipe foi perdido, cortado ou a lista de concatenação
está sem uma linha. Confira:

```bash
# Duração de cada plano:
for f in shot*.mp4; do
  ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"
done
# Total montado: tem que ser igual à soma acima:
ffprobe -v error -show_entries format=duration -of csv=p=0 assembled.mp4
```

Se os totais divergirem: a lista de concatenação está errada (linha faltando ou duplicada), ou um clipe de origem
está corrompido. Conserte a lista; **não** renderize de novo para "encher" a duração.

### Checklist de QA (rode antes de entregar o `final.mp4`)

- [ ] **Invariante da soma de duração vale**: duração do `assembled.mp4` == Σ duração dos planos (dentro do arredondamento).
- [ ] **Número de planos bate com a lista de planos**: a lista de concatenação tem exatamente uma linha por plano planejado, na ordem do corte.
- [ ] **Cortes caem na imobilidade**: cada clipe está quase parado nos primeiros e nos últimos ~0,5 s (a moldura de 2 segundos de imobilidade). Passe nas emendas; corte em movimento estala.
- [ ] **Gramática de corte de contraste duplo**: clipes vizinhos contrastam em dois eixos (tamanho + energia, ou paleta + velocidade). Nenhum corte muda uma coisa só.
- [ ] **Continuidade vale nas arestas SEQUENCIAIS**: o início do plano N+1 bate visualmente com o último quadro do plano N (a entrega do `imageUrl` aconteceu).
- [ ] **Áudio presente e em sincronia**: o `final.mp4` tem a trilha de narração; o `-shortest` não cortou a imagem cedo; a narração não ficou gravada num vão mudo.
- [ ] **Fluxos uniformes**: todos os clipes têm a mesma resolução / fps / codec (assim o `-c copy` é válido); se não tiverem, reencode a passada de concatenação.
- [ ] **Nenhum artefato de texto nítido**: qualquer cartão de título / logo / faixa inferior / revelação de número é um segmento do Remotion, não um quadro do Seedance alucinado (veja a fronteira abaixo).

Confira rápido se resolução e fps são uniformes:

```bash
for f in shot*.mp4; do
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,r_frame_rate,codec_name \
    -of csv=p=0 "$f"
done
# Todas as linhas têm que bater. Uma diferença → reencode aquele clipe antes da concatenação.
```

---

## A fronteira entre difusão e código: texto nítido NÃO é montado aqui

**O Seedance alucina texto.** Vídeo por difusão e motion graphics em código são motores diferentes. O editor não
tenta consertar palavras, números ou logos ilegíveis no corte: isso é usar o motor errado, não uma edição ruim.

| Vídeo de IA (Seedance) | Motion graphics em código (Remotion) |
|---|---|
| Prevê sequências de pixels | Gera código do Remotion |
| O texto pode alucinar / distorcer | O texto é sempre nítido (é código) |
| Cada mudança = renderização assíncrona completa | Edições em tempo real, sem destruir nada |
| Saída: mp4 mudo | Saída: mp4 + código-fonte publicável |
| Bom para: cenas cinematográficas | Bom para: marca, tipografia, dados, estrutura |

**Encaminhe PARA as skills de Remotion do Etna** (`remotion-best-practices` / `video-post` / `reels-editor`) sempre que
um segmento for: tipografia cinética / cartões de citação, animação de logo / intro-outro / vinheta de marca,
infográficos de contagem / números / revelação de estatística / gráficos de barra, texto na cor exata da marca em
hex, faixas inferiores / cartões de título / CTAs, cronômetros de contagem regressiva / placares. **Sintoma que quer
dizer "motor errado, não edição ruim":** alguém fica refazendo um clipe do Seedance para deixar uma palavra, número
ou logo legível. Pare de ajustar: esse segmento é renderizado no Remotion e **concatenado** como mais um arquivo no
mesmo `concat.txt`.

**Montagem híbrida é a resposta certa para a maioria dos anúncios**: o editor costura os dois motores no mesmo
demuxer de concatenação:

> 1. texto de gancho de 0 a 2 s (motion graphic do Remotion: para o scroll)
> 2. imagens do produto / estilo de vida de 2 a 8 s (vídeo gerado pelo Seedance: mostra a coisa)
> 3. CTA + cartão de oferta de 8 a 12 s (motion graphic do Remotion: leva à ação)

As três entram como linhas `file '...'` no `concat.txt`; garanta que as exportações do Remotion batam com a
resolução/fps do Seedance antes do `-c copy` (senão, reencode a passada).

---

## Lacunas de capacidade: diga com honestidade, não invente

Esta skill não consegue fabricar o que os motores não produzem:

- **Sem música / efeito sonoro / trilha** — `etna_voz_gerar` (via etna-cinema-voice) é **só TTS da ElevenLabs**. O
  editor põe uma trilha de narração e nada além disso. Se um briefing pedir cama musical ou efeitos sonoros, marque
  como fora do escopo.
- **Sem sincronia labial de verdade / apresentador falando.** Os mp4 do Seedance são mudos e não têm motor labial
  dentro do vídeo. O composto de geração por personagem + imagem-no-canto é um **contorno MANUAL, sinalizado** (os
  lábios não vão bater quadro a quadro), nunca um caminho suportado. Para sincronia labial de verdade, encaminhe a
  pessoa PARA FORA do cinema.
- **Sem ampliação / troca de elenco / troca de personagem** em vídeo já animado: reanime um quadro-chave editado
  (de volta ao etna-cinema-shot → etna-cinema-plan), em vez de pedir ao editor que "conserte" um clipe renderizado.
- **Sem entrada de referência de movimento.**

Se um clipe estiver estruturalmente quebrado (deriva, morfose, corte em movimento, fluxo incompatível), o conserto
fica a montante: devolva ao worker de renderização pelo coordenador. O editor não refaz renderizações nem inventa
filtros do ffmpeg para mascarar uma falha de geração.

---

## Skills irmãs do cinema

- **etna-cinema-shot**: gera as imagens / quadros de herói / folhas de referência (`etna_imagem_gerar`). Fornece os
  quadros-chave que a cadeia SEQUENCIAL devolve.
- **etna-cinema-plan**: escreve os prompts de movimento do Seedance (`etna_video_gerar`), é dono da moldura de
  imobilidade de 2 segundos e das regras de corte de um movimento e de densidade de batidas. O editor confere se
  essas molduras chegaram nos clipes.
- **etna-cinema-voice**: gera a trilha de narração (`etna_voz_gerar`, TTS da ElevenLabs). O editor põe o
  `narration.mp3` por último, com `-shortest`.
- **etna-cinema-cut** (esta skill): extrai os últimos quadros, concatena na ordem de contraste duplo, roda o portão
  de QA da soma de duração e entrega o `final.mp4`.
