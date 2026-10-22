---
name: etna-cinema-shot
description: "Use when a squad worker must WRITE and GENERATE a cinematic shot — a Seedance video prompt via etna_video_gerar, or a still / hero / product / character image via etna_imagem_gerar. Covers the six-slot Seedance formula, camera / lens / shot-size / lighting / color-grade vocabulary, the mandatory content-filter lint gate, image-to-video via imageUrl, and shot-level troubleshooting. Bind to the render-video / render-image worker. Triggers: cinematic video prompt, Seedance, shot prompt, product shot, hero image, AI video generation, AI image generation, image-to-video, camera move, color grade."
---

> **Mídia no Etna (vale sobre qualquer outra menção neste arquivo).** Ferramentas MCP do Etna: `etna_imagem_gerar(prompt, outPath, provider?, imageUrl?, formato?)`, `etna_video_gerar(prompt, outPath, provider?, imageUrl?, endImageUrl?, formato?, segundos?)`, `etna_voz_gerar(prompt, outPath, voiceId?)` e `etna_midia_provedores()` (quem está pronto, a escolha da pessoa e o modelo de cada um; nunca mostra chave). Provedores: imagem = `antigravity` (padrão, plano do Google, sem chave) | `higgsfield` | `gemini` | `openai` | `fal`; vídeo = `higgsfield` (Seedance) | `fal` (Kling: o único que respeita `endImageUrl`, e o Etna já o escolhe sozinho quando você passa `endImageUrl`); voz = `elevenlabs`. Não passe `provider` a menos que a tarefa exija: vale a IA que a pessoa escolheu em Configurações › Imagem e vídeo. O Antigravity NÃO gera vídeo. `outPath` é relativo à pasta do painel. Sem provedor pronto a ferramenta diz o que falta: pare e avise a pessoa; nunca troque de motor em silêncio. Os nomes antigos (`google-image`, `openai-image`, `replicate-video`, `selectedModel`/`enabledModels`) = `antigravity`/`gemini`, `openai`, `fal` e o campo `modelo` de `etna_midia_provedores`.


# Fotografia de cinema: a skill do DP

> **Scrub / herói web?** Esta skill traz só o **vocabulário** (movimentos de câmera, lentes, correções de cor, lint). A
> skill DONA de um herói de rolagem, de um loop de fundo ou de um clipe web é **`etna-site-scrub`**: ela tem o *contrato*
> do scrub e o lint de antes da geração. **Carregue o `etna-site-scrub` primeiro**; puxe esta para montar a string do
> prompt. Não rode um herói web só com esta skill.

O kit completo do diretor de fotografia: escrever o prompt visual, passar pelo lint e disparar a renderização. Esta skill
é DONA da string do prompt e da decisão, no nível do plano, do que entra nela. As ferramentas do Etna são DONAS da
execução. A skill nunca inventa parâmetro de ferramenta: não há nenhum além de `prompt` / `imageUrl` / `outPath`.

Esta é a skill do worker de renderização. Ligue-a ao painel worker `render-video` / `render-image`. Skills irmãs do cinema:
**etna-cinema-plan** escreve a lista de planos e distribui os planos para você; **etna-cinema-cut** faz a extração de quadros
com ffmpeg e a montagem por concatenação; **etna-cinema-voice** põe em camada de pós a trilha de TTS da ElevenLabs. Você
escreve o plano e chama a ferramenta de renderização.

> **Convenção desta skill:** os textos entre crases, os exemplos de prompt e os nomes de movimento de câmera ficam em
> **inglês**, porque é isso que vai ao modelo e é isso que o filtro de conteúdo lê. As explicações, regras e instruções
> de processo são em português.

---

## Superfície de execução: as três ferramentas (fixas, nunca reinvente)

| Camada | Ferramenta | Recebe | Devolve |
|-------|------------|--------|---------|
| Vídeo | `etna_video_gerar(prompt, outPath, provider?, imageUrl?, endImageUrl?, formato?, segundos?)` | Seedance via Higgsfield (padrão) ou Kling via fal.ai. Texto-para-vídeo; imagem-para-vídeo quando `imageUrl` é um caminho de png. | caminho do mp4 (assíncrono, **mudo**) |
| Imagem | `etna_imagem_gerar(prompt, outPath, provider?, imageUrl?, formato?)` | `antigravity` (nano-banana: cinematográfico / personagem / pintura) / `openai` (gpt-image: layout / texto / marca). Texto-para-imagem; imagem-para-imagem / edição / reestilização quando `imageUrl` é um caminho de png ou uma URL. | caminho do png |
| Áudio | `etna_voz_gerar(prompt, outPath, voiceId?)` | Só TTS da ElevenLabs. Sem música / efeito sonoro / BGM / sincronia labial. | caminho do áudio (quem cuida disso é o etna-cinema-voice) |

**O fato que molda todo prompt:** `etna_video_gerar` recebe `prompt`, `outPath`, `provider?`, `imageUrl?`, `endImageUrl?`, `formato?` e `segundos?`.
**Não há parâmetro de fps nem de resolução.** Esses vão no **corpo do prompt como linguagem de estilo** (24 fps, 4K...).
Proporção e duração: passe `formato` e `segundos` E reforce no prompt. A skill nunca inventa um parâmetro que não existe.

```
etna_video_gerar(
  prompt: "<prompt de seis campos, com proporção/duração/fps como linguagem de estilo no corpo>",
  imageUrl?: "<caminho do png: quadro inicial / referência do personagem / quadro de continuação extraído>",
  outPath?: "<onde o mp4 vai cair>"
)
```

---

## A fórmula CSLA (MCSLA sem o M)

A fórmula da ferramenta de referência anterior era **MCSLA**: Modelo, Câmera, Sujeito, Look, Ação. No Etna você NÃO escreve o
modelo no texto do prompt, mas também NÃO presume qual motor é. **Chame `etna_midia_provedores` e leia o `modelo` do
provedor de vídeo**: esse é o motor REAL que você tem (normalmente o Seedance; o Kling entra quando você passa `endImageUrl`).
Você escolhe o motor pelo parâmetro `provider` da ferramenta, nunca no texto. O que
sobrevive no corpo do prompt é o **CSLA**.

| Letra | Elemento | Descrição | Exemplo |
|--------|---------|-------------|---------|
| ~~**M**~~ | ~~Modelo~~ | **FORA DA STRING DO PROMPT**: nunca escreva "use Kling/Veo/Sora" no texto. Mas o motor é o que estiver LIGADO (confira em `etna_midia_provedores`), não o Seedance presumido. Precisa de uma capacidade que só o Kling tem (`endImageUrl` com 2 quadros-chave, animação de rosto real)? Só sinalize lacuna se nenhum Kling estiver ligado; se um estiver, selecione-o pelo `model`. | — |
| **C** | Câmera | Controle de câmera nomeado, em linguagem simples | "FPV Drone shot weaving through the alley" |
| **S** | Sujeito | Quem / o quê + aparência | "A woman in a sand-colored suit, sharp eyes" |
| **L** | Look | Estilo + cor + luz | "Cinematic, golden hour, anamorphic flare" |
| **A** | Ação | O que acontece na cena | "She turns slowly, wind lifting her coat" |

Ordem de peso dos tokens: **Sujeito → Ação → Câmera → Estilo** é a ordem mais confiável. Os primeiros tokens carregam peso
desproporcional. Os nomes de câmera agora são linguagem simples, não predefinições do host: não existe Painel de Diretor
para clicar; o Seedance lê o corpo do prompt.

---

## A fórmula de seis campos do Seedance

Todo prompt do Seedance deve acertar estes seis campos, nesta ordem:

```
[Movimento de câmera] + [Sujeito] + [Ação] + [Cenário] + [Estilo] + [Luz]
```

Tecnicamente os seis são opcionais, mas um prompt com os seis quase nunca é marcado, porque o filtro tem todo o contexto
para interpretar cada palavra. Um prompt que falta 3 ou mais campos é de onde saem as marcações.

**Prompt mínimo viável (~30 palavras):**

> **Slow dolly-in on a figure in a dark overcoat standing alone at the end of a rain-slick alley. Cold teal shadows, single practical streetlamp, shallow depth of field.**

Câmera ✓ Sujeito ✓ Ação ✓ Cenário ✓ Estilo ✓ Luz ✓: os seis campos, passa no filtro porque a cena é totalmente legível.

### Níveis de delegação (tamanho do prompt conforme a ambição)
- **L1**: até 30 palavras, domínios conhecidos: deixe o modelo dirigir.
- **L2**: 30 a 100 palavras: sujeito + ação + ambiente + nota de câmera + âncora de estilo.
- **L3**: 100 a 300 palavras: segmentado por tempo (`0–3s: ...`).
- **L4**: 300 a 1000+ palavras: coreografia completa.

---

## Tipos de prompt: T2V / I2V / Continuação

### Texto-para-vídeo (T2V)
Comece do zero. Chame `etna_video_gerar(prompt)` **sem** `imageUrl`. Melhor para planos de estabelecimento, ambientes e
conceitos abstratos sem personagem específico.

```
[Sujeito + aparência].
[Ambiente: lugar, hora, tempo, atmosfera].
[Ação: o que acontece e como].
[Câmera: movimento nomeado, em linguagem simples].
[Look: estilo + correção de cor].
```

**Exemplo:**
```
A lone astronaut stands on the surface of a red desert planet, helmet visor reflecting
twin moons rising on the horizon. Dust spirals slowly in the thin atmosphere.
She turns to face the camera, gloved hand raised in a slow salute.
Camera: slow Crane Up revealing the vast emptiness behind her.
Style: desaturated orange and deep blue, letterboxed anamorphic composition.
16:9, 10s, 24fps.
```

### Imagem-para-vídeo (I2V)
Anime uma imagem fornecida. A imagem é o quadro inicial. Chame `etna_video_gerar(prompt, imageUrl)` em que `imageUrl` é um
**caminho de png**, normalmente um quadro-chave que você montou antes com `etna_imagem_gerar`. Melhor para consistência de
personagem, fotos de produto, animação de retrato, dar vida a um storyboard e continuação.

```
[A imagem fornecida é o primeiro quadro: NÃO a redescreva].
[Descreva o que deve mover, mudar ou animar, não o que já está visível].
[Câmera: movimento nomeado].
[Pistas de estilo / atmosfera].
```

**Exemplo:**
```
The provided image is the first frame.
The woman's hair lifts gently in the wind. She blinks slowly and turns her gaze
slightly to the left, a faint smile forming.
Camera: subtle Dolly In toward her face.
Style: warm afternoon light, shallow depth of field.
```

**I2V: a regra mais desrespeitada.** NÃO redescreva o que já está na imagem. Descreva só o que deve *mudar* ou *animar*.
Descrever demais os elementos estáticos confunde o modelo e faz a identidade derivar. Existe exatamente **UM** slot de
`imageUrl`: nada de `@Image1`/`@Image2` em vários slots. Identidade do personagem, figurino e ambiente entram todos nesse
único png de quadro-chave, antes de você chamar o vídeo. Abertura de I2V: `Starting from the provided image as the first frame.`

### Continuação (continuidade sequencial): cadeia de extração de quadros
Para o plano N+1 continuar sem emenda o plano N, extraia o último quadro do plano N como png e passe-o como `imageUrl` do
plano N+1. É um **passo de ffmpeg no Bash** (o etna-cinema-cut é dono da cadeia), não uma ferramenta:

```bash
ffmpeg -sseof -0.1 -i shotN.mp4 -frames:v 1 -q:v 2 frameN.png
```

Depois, `etna_video_gerar(promptDoPlanoN+1, imageUrl="frameN.png")`. A regra do I2V vale: o quadro é o primeiro quadro;
descreva só o movimento novo.

#### As cinco regras de continuação
1. **Âncora no último quadro.** Abra com uma frase descrevendo o que o último quadro do clipe anterior mostra: pose, posição no quadro, direção do olhar. Isso diz ao modelo por onde começar a renderizar.
2. **Âncora de identidade colada literalmente.** Cole o Bloco de Identidade do personagem **sem alterações** no prompt de continuação. Não parafraseie, não encurte. As fronteiras de continuação são onde a identidade deriva.
3. **Clipe anterior como memória secundária.** Nomeie o que acabou de acontecer numa frase de referência ("following her glance back", "after the door opening"). Não redescreva a ação.
4. **Continuação imediata.** Comece no quadro seguinte ao último quadro do clipe anterior. Sem salto de tempo, fade ou corte implícito, a menos que seja pedido.
5. **Sem repetir a ação.** Estenda, não faça loop. Se o clipe anterior terminou com ela sacando a arma, a continuação descreve o que ela faz com a arma A SEGUIR, não o saque.

**O que precisa atravessar o corte:** identidade do personagem (rosto, corpo, marcas), figurino (cada peça e acessório),
ambiente (arquitetura, qualidade da luz, tratamento de cor, partículas) e carga emocional (o estado em que ela estava no último
quadro ainda tem que aparecer no corpo dela na abertura da continuação).

**Biblioteca de frases anti-repetição** (escolha a cujos verbos batem com o clipe anterior): `start immediately after the final frame` / `do not repeat the previous fight` / `do not restage the earlier beat` / `continue forward into the new action` / `preserve the same fatigue state and emotional carryover`.

---

## Papéis de referência: o que cada `imageUrl` representa

Você tem **um** slot de `imageUrl` por chamada. O sistema de múltiplas alças `@Image1..4 / @Video / @Audio` da ferramenta de
referência não existe aqui: lacuna de capacidade (sem múltiplas referências, sem vídeo de referência de movimento, sem
referência de áudio). A única imagem cumpre um de quatro papéis semânticos por plano:

| Papel | O que trava | Como escrever |
|---|---|---|
| **Personagem** | Identidade do personagem principal: rosto, porte, marcas | `The image is the main character. [Bloco de identidade, literal.] [Ação.]` |
| **Último quadro** | Onde a continuação começa a renderizar | `Continuing from the prior clip — [o que o último quadro mostra]. [Nova ação.]` |
| **Ambiente** | O mundo / cenário: arquitetura, luz, atmosfera | `The image is the environment. [Sujeito + ação.] [Lighting consistent with the image.]` |
| **Adereço** | Um objeto recorrente: peça marcante do figurino, objeto de assinatura, veículo | `The image is the prop. [Sujeito interage com ele.] [Mesma geometria/material da imagem.]` |

**Regra que sustenta tudo: a referência sustenta a memória; o texto define a ação.** O `imageUrl` carrega as propriedades
persistentes que precisam continuar consistentes; o texto do prompt dirige o que acontece nesta geração. A imagem não
conduz ação nova; o texto não substitui o que a imagem carrega. As duas camadas ficam no seu lugar.

Para a maior consistência de personagem numa sequência, gere UM png canônico do personagem uma vez (`etna_imagem_gerar`,
provedor `antigravity`) e reutilize esse mesmo caminho como `imageUrl` em todo plano que precisa do personagem.

---

## A regra de separação entre identidade e movimento

Quando um personagem precisa continuar consistente entre planos, **sempre divida o prompt em dois blocos rotulados**:

**Bloco de Identidade**: SÓ descritores visuais estáticos: traços do rosto, tom de pele, tipo de corpo, marcas, roupa,
acessórios, paleta. NADA de movimento, câmera ou linguagem temporal.

**Bloco de Movimento**: SÓ temporal + câmera: movimento de câmera, coreografia da ação, velocidade, movimento do ambiente,
mudanças atmosféricas. NADA de repetir aparência.

**RUIM (misturado: a identidade deriva):**
```
A woman with sharp cheekbones and auburn hair in a blue trench coat runs through a
rain-soaked alley, her coat flapping, sharp cheekbones catching the neon light, camera
chasing her, auburn hair streaming behind her.
```
**BOM (separado):**
```
Identity Block: The character — sharp cheekbones, auburn hair shoulder-length, blue
trench coat with silver buttons, lean athletic build.
Motion Block: She runs through a rain-soaked alley, coat flapping. Camera: low behind,
matching pace (Action Run). Neon reflections streak across wet concrete. Style:
cold blue shadows, warm neon accents.
```

POR QUÊ: o rosto deforma no meio do clipe porque o modelo relê os descritores de rosto enquanto processa o movimento.

**Tabela de roteamento de descritores:**

| Bloco de Identidade | Bloco de Movimento |
|---|---|
| Formato do rosto / tom de pele / cor dos olhos | Nome do movimento de câmera |
| Penteado / cor / comprimento | Verbos de ação (corre, vira, senta) |
| Tipo de corpo / altura / porte | Movimento do ambiente (vento, chuva, luzes) |
| Roupa / acessórios / joias | Sinais de velocidade e tempo |
| Cicatrizes / tatuagens / marcas | Mudanças atmosféricas (trocas de luz, névoa) |
| Paleta de cores do personagem | Estilo e correção de cor da cena |

**Substituto de continuidade de personagem no Etna** (a ferramenta de referência tinha Soul ID + `@Element`; o Etna não tem
nenhum dos dois: lacuna de capacidade): gere UM quadro-chave de herói / personagem com `etna_imagem_gerar` e alimente esse
mesmo png como `imageUrl` em todo plano. O Bloco de Identidade vira o prompt do quadro-chave; o Bloco de Movimento vira o
prompt do vídeo. No time, todo painel de worker aponta para o **mesmo** png de herói: esse ativo compartilhado é como a
identidade se mantém quando os planos renderizam de forma independente e em paralelo.

**Regra de identidade no I2V:** quando o png de referência já carrega a identidade, redescrevê-la cria conflito. ERRADO:
`[image] — A woman with curly brown hair and green eyes in a red jacket walks through the park.` CERTO:
`[image] — She walks through the park, pausing to look up at falling leaves. Camera: slow tracking alongside.`

---

## CÂMERA: vocabulário de movimentos (~70, prosa descritiva, sem macros)

Cada entrada é **prosa descritiva, não uma macro.** A ferramenta de referência tinha menus de predefinição em que um *nome*
disparava um efeito. O Seedance não tem predefinições: você coloca o *comportamento descrito* no corpo do prompt. O nome é para
VOCÊ achar a entrada; a prosa vai na string.

### Dolly
| Movimento | O que faz | Frase para o prompt |
|------|-------------|---------------|
| Dolly In | movimento linear em direção ao sujeito | "Camera dollies in toward her face" |
| Dolly Out | movimento linear para longe | "Camera dollies out revealing the empty square" |
| Dolly Left/Right | travelling lateral | "Camera tracks left alongside the runner" |
| Dolly Zoom In | dolly para a frente + zoom para trás ao mesmo tempo (Vertigo) | "Dolly-zoom: subject stays the same size as the background rushes away" |
| Super Dolly In/Out | corrida / recuo rápido exagerado | "A fast aggressive push straight onto the handprint" |
| Truck Left/Right | translação lateral (= dolly lateral) | "Camera trucks right, sliding parallel to her profile" |

### Grua / vertical
Crane Up `crane up from the soldier's hands to the war-torn landscape` · Crane Down `crane down from skyline to the lone figure` · Crane Over The Head `top-down view directly over the crowd` · Levitation `the camera floats upward from her feet to her serene face` · Pedestal Up/Down `camera pedestals up from snow level to eye-level` · Tilt Up/Down `camera tilts up from her boots to the mountain peak`.

### Órbita / arco
360 Orbit `camera orbits a full circle around the boxer` · Arc `camera arcs slowly around the two detectives` · Lazy Susan `slow turntable rotation around the antique watch` · Robo Arm `a precise mechanical arc sweeping from headlights over the roof`.

### Zoom
Crash Zoom In/Out `crash zoom snapping onto the bloody handprint` · Rack Focus `rack focus from the sword in foreground to her face behind`.

### Acompanhamento / ação
FPV Drone `FPV-drone weaving through the warehouse chasing the motorcycle` · Action Run `camera low behind him, matching his sprint` · Handheld `handheld, jostling with the crowd, subtle shake, not chaotic` · Head Tracking `camera locked to his head as the boxer staggers` · Snorricam `camera rigged to her body, the room swaying behind her`.

### Especiais
Bullet Time `time freezes, camera sweeps around the leaping assassin` · Dutch Angle `dutch angle, tilted horizon, as the conspirators whisper` · Fisheye `fisheye lens, curved barrel distortion` · Whip Pan `whip-pan blur from the thief to the officer` · Overhead `overhead top-down of the dancers forming patterns` · Flying `camera glides freely through open air over the valley`.

### Baseados em tempo
Hyperlapse `hyperlapse down the boulevard from dawn to dusk` · Timelapse Human `time-lapse, fixed camera, people rushing the subway platform` · Timelapse Landscape `time-lapse of the mountain valley sunrise to dusk` · Low Shutter `slow-shutter motion blur smearing the spinning dancer's silhouette`.

### Através de objeto e veículo
Through Object In/Out `camera glides through the keyhole into the dusty study` · Mouth In `camera enters the storyteller's open mouth into the fantasy world` · Car Chasing `camera hugs the side of the black car through the streets` · Car Grip `camera fixed to the hood, shaking on every bump` · Buckle Up `violent shaking as the car skids around the corner`.

### Biblioteca de frases confiáveis
| Intenção | Frase |
|--------|--------|
| Sem movimento de câmera | `locked-off static camera, no movement` |
| Aproximação lenta | `slow dolly push from medium shot to tight close-up over 8 seconds` |
| Seguir o sujeito | `handheld tracking following the subject, subtle shake, not chaotic` |
| Revelar escala | `crane shot rising from ground level to overhead` |
| Circular o sujeito | `smooth 180-degree orbit at eye level, constant distance` |
| Zoom dramático | `crash zoom from wide to extreme close-up on impact` |
| Movimento em primeira pessoa | `FPV camera weaving through the environment at walking pace` |

### A regra de um só movimento (estrutural: causa nº 1 de tremedeira / geração falha)
Para qualquer plano, especifique **UM movimento de câmera principal.** NÃO empilhe movimentos (dolly para a frente + panorâmica
para a esquerda + inclinação para cima). Errado: `dolly push forward while panning left and tilting up to reveal the skyline`.
Certo: `slow dolly push from medium shot to tight close-up`. Se precisar de vários movimentos, **divida em planos separados**
(chamadas `etna_video_gerar` separadas, costuradas pelo etna-cinema-cut).

- **Panorâmica parada x travelling:** uma câmera que **panorama** gira a partir de uma posição fixa; uma câmera que **desliza** se translada pelo espaço. Diga qual dos dois você quer.
- **Sequenciado x simultâneo:** a regra de um só movimento governa o movimento *simultâneo*. Movimento *sequenciado* é aceitável com o tempo declarado: `Camera holds 0–3s tracking the character, then pushes in on the face 4–8s`, renderizado como fases discretas.
- **Combinações compatíveis:** Dolly In + Dutch Angle (revelação de vilão); Crane Up + 360 Orbit (escala épica + isolamento); FPV Drone + Crash Zoom In (clímax de perseguição); Handheld + Action Run (fuga).
- **Anti-deriva:** nunca combine câmera travada + na mão, órbita + panorâmica, inclinação + empurrão de dolly. Para sujeitos que se movem em relação à câmera (andando de moto, voando): `CAMERA MOUNTED ON [SUBJECT], LOCKED-ON SHOT`.

### Ângulos de câmera (inclinação e perspectiva)
Ângulo baixo (poder / domínio) · Ângulo alto (vulnerabilidade) · Altura dos olhos (neutro) · Vista de cima (onipotente) · Vista de rés do chão (escala imponente) · Nível do chão (impacto) · Holandês / inclinado (desconforto) · Oblíquo estático (desconforto estilizado) · OTS (diálogo, plano / contraplano) · POV / primeira pessoa (imersão) · Dois personagens (relação) · Plano cowboy (confronto, da metade da coxa para cima) · Ângulo de selfie (casual de rede social).

### Tamanhos de plano (a escada de enquadramento)
EWS/ELS (sujeito minúsculo, escala / isolamento) · LS/WS (corpo inteiro + ambiente) · Plano inteiro (da cabeça aos pés, figurino / apresentação) · MLS/Cowboy (da metade da coxa para cima, postura / confronto) · MS (da cintura para cima, diálogo) · MCU (do peito / ombros para cima, emocional) · CU (rosto preenche o quadro, emoção crua) · ECU (um traço só, tensão) · Macro (textura) · Insert (detalhe de objeto).

### Distância focal / abertura
8 mm ultra-grande-angular, distorção imersiva (POV de ação / desorientação) · 14 mm grande-angular, escala ambiental (estabelecimento) · 35 mm campo de visão humano natural (documentário / dois personagens) · 50 mm retrato clássico, compressão (CU de personagem / produto) · 75 mm retrato apertado, compressão (reação / clímax emocional). Abertura: f/1.4 profundidade rasa, bokeh cremoso (intimidade) · f/4 equilibrado e versátil · f/11 profundidade grande, tudo nítido (produto / paisagem).

### Predefinições de câmera por gênero (Principal | Secundária | EVITAR)
- Produto / e-commerce: órbita / empurrão lento / estática | revelação com grua para baixo | na mão, panorâmica rápida.
- Estilo de vida / social: na mão / estática / panorâmica lenta | dolly ao lado | ângulo holandês, zoom brusco.
- Drama / narrativa: empurrão lento / recuo com dolly / acompanhamento | grua para cima | movimentos rápidos, zoom estalado.
- Clipe musical: panorâmica rápida / zoom estalado / acompanhamento rápido | órbita de 360° | estática.
- Terror: aproximação lenta (dolly para dentro) / plano parado / ângulo holandês | grua para baixo | acompanhamento rápido.
- Ação / perseguição: drone FPV / acompanhamento / corrida na mão | zoom brusco | estática, órbita lenta.
- Paisagem / viagem: grua para cima / panorâmica lenta / sobrevoo de drone | revelação com recuo do dolly | na mão, planos fechados.
- Comédia / social: estática (cara de paisagem) / zoom estalado | panorâmica rápida | movimentos lentos e dramáticos.

---

## Sincronia câmera-emoção: 6 registros

A câmera é o duplo emocional do personagem focal. Escolha movimento / lente / duração pelo estado emocional do personagem, e não pelo que parece "cinematográfico" de forma abstrata.

| Emoção do personagem focal | Prescrição de câmera (escreva no prompt) |
|---|---|
| Raiva / fúria / tensão | Respiração na mão, trêmula / instável: ritmo de respiração quebrado, microtremores nos dois eixos, amplitude pequena, ritmo irregular. Sem estabilizador. |
| Calma / controle / confiança | Respiração na mão, suave: ritmo de respiração constante, microamplitude regular. Estabilizador leve, mas vivo. |
| Tristeza / vulnerabilidade | Na mão, lenta, baixa: frequência de respiração mais baixa, leve deriva para baixo, peso maior. |
| Choque / revelação | Estática + empurrão / recuo muito lento: congelamento seco no momento, depois movimento mínimo de 0,5 a 2 s. |
| Ação | 60 fps, obturador de 180°: desfoque de movimento limpo preso ao obturador; evite o desfoque puxado. |
| Batida final / veredito | Congelamento de vista de cima, 0,3 a 0,5 s: diretamente acima, o tempo para, posições travadas. |
| Colapso emocional / precisa de espaço | Recuo lento de médio / fechado para aberto: "deixe o personagem em paz". |

**Atalho de emoção para câmera:** Percepção → dolly lento para dentro + olhos arregalando · Medo → ângulo holandês + na mão · Poder → grua para cima + órbita de 360° + postura larga · Vulnerabilidade → plano de cima + recuo do dolly + pequeno no quadro · Intimidade → dolly para dentro + profundidade rasa · Caos → drone FPV + na mão + cortes rápidos.

**Arcos emocionais num só plano:** quando a emoção muda ao longo de um take contínuo (raiva → controlada), mude a câmera de forma sincronizada, escrita como fases: fase de abertura (emoção de entrada) → fase de transição (a amplitude diminui, a deriva assenta, o empurrão desacelera) → fase de fechamento (emoção de saída). Decomponha a emoção genérica *antes* de escolher a câmera (veja abaixo).

**Escada de resolução de conflito** (quando as regras indicam movimentos de câmera diferentes): 1. A direção explícita da pessoa vence. 2. Depois o arquétipo da cena (Atmosfera → estática / empurrão lento; Ação → na mão / panorâmica rápida / FPV; Diálogo → cobertura de ombro / empurrão no rosto na emoção). 3. Por último, o registro de sincronia emocional (desempate padrão). Quando não for óbvio, **sinalize**: diga qual regra indicou o quê e por quê. Escolher em silêncio é o modo de falha.

---

## Vocabulário de LUZ

| Tipo | Descrição | Melhor para |
|------|-------------|----------|
| Hora dourada / hora mágica | Quente e direcional, sol perto do horizonte, sombras longas e macias | Romance, épico, beleza |
| Hora azul | Azul-aço frio, ambiente depois do pôr do sol | Melancolia, solidão urbana |
| Nublado / softbox | Luz suave e uniforme, sem sombras duras | Documentário, retrato |
| Neon | Artificial colorido de letreiros / telas | Cyberpunk, noite, urbano |
| Volumétrica | Raios de luz através de névoa / poeira / fumaça | Fantasia, atmosfera |
| Só práticas | Luz de fontes visíveis no quadro | Realismo, noir, íntimo |
| Luz lateral | Uma fonte forte de um lado, sombra profunda | Drama, tensão |
| Contraluz / luz de contorno | Luz atrás do sujeito, brilho na borda / silhueta | Mistério, romance, revelação |
| Luz dura | Uma fonte forte e única, sombras definidas | Confronto, exposição |
| Luz suave | Difusa, envolvente, sombras mínimas | Retrato, beleza |
| Chave baixa (low-key) | Sombras profundas, pequenas poças de luz | Noir, suspense, terror |
| Chave alta (high-key) | Clara, uniforme, sombras mínimas | Comédia, comercial, estilo de vida |
| Sol de meio-dia forte | Duro de cima, sombras definidas e fortes | Deserto, vulnerabilidade exposta |

**Montagens cinematográficas (o Seedance responde pelo nome):** Rembrandt (triângulo de luz numa bochecha sombreada, um olho iluminado) · Borboleta / Paramount (de cima, sombra embaixo do nariz: glamour) · Dividida (metade do rosto iluminada, metade na sombra: dualidade / vilão) · Claro-escuro (luz e sombra extremas: drama alto).

**Luz pela física da cena (troca adjetivos por mecanismos: o modelo reconstrói a iluminação a partir de peças nomeadas e só consegue aproximar `moody` / `dramatic`):**
- Posição da fonte: `key light from screen-left, ~30° above eye line`
- Reflexo / rebatimento: `warm bounce off the wooden floor lifting under-jaw shadow`
- Geometria da sombra: `hard shadow on screen-right wall reading the silhouette of the desk lamp`
- Densidade do ambiente: `dense ambient haze in the foreground softening contrast 6m+ from camera`

---

## Vocabulário de CORREÇÃO DE COR

| Clima | Frase de correção |
|------|-------------|
| Blockbuster | "Teal shadows, orange highlights, high contrast" |
| Thriller frio | "Teal and orange, desaturated, high contrast" / "desaturated blue-grey, crushed blacks" |
| Nostalgia quente | "Golden-hour amber, soft shadows, low contrast" |
| Cyberpunk | "Neon magenta and cyan, deep shadows, HDR" |
| Terror | "Sickly green-yellow, crushed blacks, desaturated" |
| Romance | "Soft warm pink-gold, lifted shadows, dreamy" |
| Documentário | "Neutral, natural light, no grade" |
| Fantasia épica | "Rich jewel tones, deep shadows, volumetric light" |
| Noir | "High-contrast black and white, or near-monochrome" |
| Ficção científica fria | "Ice blue and silver, stark white light" |
| Pós-apocalíptico | "Desaturated orange and brown, dust haze" |

**Regra de cor 60/30/10:** um quadro lê melhor quando 60% é uma cor dominante, 30% uma secundária e 10% um acento. Nomeie um tom dominante único + uma paleta de apoio, não cinco cores brigando.

**Emulação de filme (nome + caráter):** Kodak Portra 400 (quente, tons de pele ricos, leve grão) · Fuji Velvia (vívido, saturado, grão fino) · Kodak Vision3 500T (cinematográfico, natural, leve calor) · Ilford HP5 (P&B clássico, grão visível) · Kodak Ektachrome (brilhante, contrastado, slide limpo).

**Controle de época: nomeie materiais + luz, não a década:**
- ~~"estilo anos 70"~~ → `Kodachrome warm tones, wood paneling, orange shag carpet, tungsten bulbs casting amber light`
- ~~"noir dos anos 40"~~ → `high-contrast black and white, Venetian-blind shadows, fedora silhouettes, wet asphalt reflecting streetlamps`
- ~~"vídeo caseiro dos anos 90"~~ → `Hi8 camcorder grain, autofocus hunting, timestamp overlay, oversaturated greens`

---

## ESTILO: âncoras de aparência de filme

| Look | Coloque no prompt | Combina com |
|------|--------------------|-----------|
| Cinematográfico | (veja o aviso) polido, alto contraste, vívido, blockbuster moderno | Drama, ação, comercial |
| VHS | grão de fita de vídeo retrô, sangramento de cor, linhas de varredura, amarelos / vermelhos quentes desbotados, baixo contraste, `4:3 framing` | Nostalgia dos anos 80/90, terror, flashback |
| Super 8 mm | grão de filme quente, vinheta suave, dourado / desbotado, sensação de filme caseiro, `4:3 framing` | Romance, nostalgia, indie |
| Anamórfico | `2.35:1 letterboxed framing`, reflexos horizontais de lente, leve distorção de barril, pretos profundos | Ação, épico, guerra, paisagens amplas |
| Abstrato | não representacional, cor surreal, formas não convencionais | Clipe musical, sequência de sonho, experimental |

**Duas regras de estilo (estruturais):**
- **Uma âncora de estilo.** UMA âncora principal vale mais que cinco adjetivos. Escolha a âncora, acrescente 1 ou 2 tokens de apoio e pare. Errado: `cinematic, anamorphic, moody, atmospheric, dramatic, film grain, desaturated, noir-inspired, high contrast, vintage`. Certo: `anamorphic, subtle grain, muted palette`.
- **"Cinematográfico" não faz nada.** Todo clipe do Seedance já é cinematográfico por padrão; a palavra não acrescenta informação. Troque: ~~cinematic~~ → `shallow depth of field, warm highlights, cool shadows`; ~~cinematic look~~ → `anamorphic, letterboxed, horizontal lens flares`; ~~cinematic quality~~ → `35mm film stock, natural grain, Kodak Portra palette`.

**Proporção x registro anamórfico:** a proporção de saída é uma especificação rígida declarada no corpo do prompt (`vertical 9:16 framing`, `square 1:1 framing`). Anamórfico / 2.35:1 / cinemascope é um *registro de fotografia* (aparência com letterbox, reflexos horizontais) renderizado *dentro* do enquadramento escolhido. "16:9 anamórfico" pede duas coisas contraditórias: declare o enquadramento como especificação, e o anamórfico como aparência.

---

## Banco de frases de movimento / VFX (descreva literalmente, sem macros)

A ferramenta de referência tinha predefinições nomeadas em que um nome disparava uma macro. **Não existe macro no Seedance.** Coloque o comportamento descrito no prompt, no momento em que ele deve acontecer.

- Referência: `A swordsman draws his blade. Apply the Disintegration preset.`
- Etna: `A swordsman draws his blade; his body breaks apart into a cloud of drifting embers and ash that scatter on the wind.`

Predefinição → frase literal: Disintegration=`breaks apart into drifting particles`; Freezing=`freezes into ice`; Bullet Time=`Matrix-style frozen moment with camera sweep`; Levitation=`subject levitates upward`; Glow Trace=`moving subject leaves a glowing trail`; Flame On=`subject ignites and burns unharmed`; Earth Zoom Out=`camera pulls back from earth's surface`; Sakura Petals=`cherry blossom petals fill the air`; Glitch=`digital glitch artifacts across the image`; Portal=`a portal opens to another dimension`; Money Rain=`cash rains down from above`; Smoke Transition=`smoke fills frame then clears to new scene`. Coloque o efeito no FIM do prompt; garanta que a cena sustente logicamente o efeito.

### A hierarquia de movimento em 4 camadas
Nomeie cada uma explicitamente, para evitar a falha de sobrecarga de movimento (borrão / deformação). Uma camada sem nome é uma camada que o modelo inventa.
1. **Movimento do sujeito**: anda, vira, levanta a mão.
2. **Movimento interno**: respiração, deriva do cabelo, tecido, movimento dos olhos, microexpressão.
3. **Movimento da câmera**: panorâmica, dolly, empurrão, parada.
4. **Movimento do ambiente**: chuva, folhas, trânsito, mudança de luz.

### Densidade de batidas (governa toda ação)
O Seedance aguenta **1 a 2 batidas de ação distintas a cada 5 segundos.** Borrado / tremido / deformando = ações demais num tempo curto demais.

| Janela | Batidas | Exemplo |
|--------|---------|---------|
| 3 a 5 s | 1 a 2 | Pular + pousar |
| 5 a 8 s | 2 a 3 | Pular + pousar + sacar a arma |
| 8 a 12 s | 3 a 5 | Pular + pousar + sacar + atirar + se abrigar |
| 12 a 15 s | 4 a 6 | Sequência completa: divida em vários planos |

**Uma ação por clipe** + 1 a 2 secundárias no máximo. Descreva INTENÇÃO e CONSEQUÊNCIA, não quadro a quadro. `She raises her arm, energy gathering in her palm until it erupts in a blinding flash; sparks scatter` — e não `at 0s arm at 0°, at 1s arm at 45°`. Divida ação densa em chamadas `etna_video_gerar` separadas (o etna-cinema-cut concatena).

### Linguagem de física e ritmo em três atos
Use consequências físicas concretas, não palavras de humor:
- ~~"powerful punch"~~ → `fist connects, sweat flies off in slow motion, opponent's head snaps back`
- ~~"dramatic entrance"~~ → `door slams open, dust erupts from the frame, light floods the dark room`
- ~~"fast car"~~ → `tires spin, gravel sprays backward, chassis drops as acceleration kicks in`

Descreva a **ação**; deixe o modelo renderizar o **impacto**: não descreva o impacto antes da ação. Arco da ação: **carga** (a tensão sobe) → **explosão** (a ação estoura) → **rescaldo** (as consequências físicas se desenrolam).

**Advérbios de grau:** `slowly, dramatically, violently, gently, frantically, deliberately, cautiously, explosively`. Para a *velocidade* do movimento, prefira uma analogia física ou uma âncora de tempo: `like dust suspended in honey` / `like embers floating in still air` / `one full revolution across the entire 10-second clip` / `roughly 6 degrees per second`.

**Padrão: in medias res.** As cenas começam já em andamento, a menos que a pessoa diga "começa com…". Abra na ação.

---

## Vocabulário de microexpressão (19 pontos nomeados)

Direções de atuação: combinações dos 8 canais abaixo. Use a predefinição quando uma servir; decomponha a partir dos primeiros princípios quando nenhuma servir.

| Expressão | Descrição |
|-----------|-------------|
| Neutro seco (deadpan) | Afeto chapado, nenhuma emoção visível |
| Foco feroz | Olhar intenso e travado, atenção total |
| Sorriso reprimido | Segurando um sorriso, canto da boca tremendo |
| Devastação silenciosa | Olhos vidrados, mandíbula tensa, segurando a barra |
| Cálculo frio | Olhos varrendo, nada vaza, clínico |
| Diversão amarga | Sorriso de canto só de um lado, olhos que não sorriem |
| Choque congelado | Boca levemente aberta, olhos fixos, corpo parado |
| Raiva fervendo | Mandíbula cerrada, narinas abertas, olhar fixo |
| Abertura vulnerável | Olhos suaves, lábios entreabertos, sem defesa |
| Percepção | Olhos se arregalando, entendimento lento (combina com dolly lento para dentro) |
| Medo | Olhos bem abertos, respiração congelada (combina com ângulo holandês, na mão) |
| Desafio | Queixo erguido, mandíbula firme, olhar direto |
| Luto | Testa franzida, boca virada para baixo, olhos marejados |
| Nojo | Nariz franzido, lábio superior levantado |
| Desprezo | Lábio levantado de um lado, olhos semicerrados |
| Alívio | Ombros soltos, mandíbula amolecendo, olhos meio fechados |
| Antecipação | Inclinado para a frente, sobrancelhas levantadas, respiração presa |
| Determinação | Olhar firme, respiração assentada, mandíbula quadrada |
| Exaustão | Pálpebras pesadas, mandíbula frouxa, reações atrasadas |

### Emoção como comportamento visível: 8 canais
Decomponha emoção abstrata ("ela está com medo", "ele está com raiva") em comportamento observável que o modelo consegue encenar. As expressões nomeadas são o que esses canais produzem.
- **Respiração**: ritmo, profundidade, pausa, caráter da expiração
- **Comportamento dos olhos**: fixação, taxa de piscada, direção do olhar
- **Tensão da mandíbula**: cerrada, frouxa, trabalhando, travada
- **Perda de foco**: olhar à deriva, atenção escapando, atraso na resposta
- **Padrão de varredura**: direção da varredura dos olhos / cabeça, alvo acompanhado
- **Recuperação atrasada**: intervalo entre o estímulo e o retorno ao normal
- **Tentativa de controle**: esforço visível de supressão / regulação
- **Resíduo emocional depois do pico**: o que fica no corpo depois da batida dominante

### Decomposição de emoção genérica: "que tipo de X?"
Nunca deixe uma emoção genérica no prompt. "Triste" / "com raiva" / "surpreso" / "com medo" / "pensativo" / "apaixonado" cada um
tem de 3 a 4 realizações físicas diferentes; o modelo renderiza uma versão diferente a cada nova geração, e a aderência do lote
cai. Decomponha em movimentos musculares específicos, respiração, olhos, pele. Se não conseguir decompor com segurança, pergunte à
pessoa qual escolher. Modelo de pergunta (ofereça quando, do contrário, você inventaria o detalhe):

> Que tipo de surpresa?
> (a) Leve e positiva: sobrancelhas sobem, lábios se abrem de leve, inspiração lenta, nenhum outro movimento.
> (b) Choque: inspiração brusca pela boca, olhos arregalam, o corpo congela, a mão sobe ao peito.
> (c) Descrença: piscada lenta, a cabeça inclina um pouco, os lábios se apertam, uma sobrancelha sobe.
> (d) Surpresa com alegria: o brilho do olhar muda, o sorriso cresce aos poucos, os ombros relaxam.

**Emoção em camadas** (dois registros empilhados): estado dominante no ROSTO, estado de fundo na RESPIRAÇÃO / POSTURA / ESTADO DA MÃO, sinal visível nos OLHOS. *Determinação ansiosa* = mandíbula travada + olhar fixo (determinação) com respiração curta no peito + uma mão abrindo e fechando (ansiedade por baixo). **Composto de detalhe pequeno:** emoção base + uma pista específica (`the man is very upset, and his lower lip trembles`) rende melhor que decomposição excessiva. Não se decomponha demais.

---

## Geração de imagem: `etna_imagem_gerar`

**Texto-para-imagem OU imagem-para-imagem.** `etna_imagem_gerar(prompt, outPath, provider?, imageUrl?, formato?)`. Passe `imageUrl` (uma URL http(s) ou um caminho local de png) para editar / reestilizar / usar como referência uma imagem existente: o Gemini a roteia como uma parte inlineData (edição nano-banana), a OpenAI pela `/images/edits` (edição gpt-image). Não há parâmetro separado de máscara / inpaint ou de remoção de fundo: descreva a edição no prompt. Escolha do provedor: `antigravity` (nano-banana: quadro único cinematográfico / personagem / pintura) x `openai` (gpt-image: denso em layout / texto / marca: mockups de interface, layouts de anúncio, infográficos, folhas de referência). Só desempate para o registro de layout quando a saída tiver regiões discretas / cromo / texto.

**Padrão base:**
```
[Palavra-chave do plano] de [descrição do personagem] + [pose/ação] + [detalhe do ambiente] + [luz/atmosfera]
```

**Fórmula completa em camadas (a mais forte):**
```
[Tamanho do plano] + [Ângulo] + [Palavra-chave de movimento] de [personagem].
[Pose, expressão ou ação].
[Ambiente: local, clima, atmosfera].
[Luz: hora do dia, fonte, qualidade].
[Estilo: tipo de filme, correção de cor].
```

**Exemplo completo:**
```
Medium close-up, low angle, slow dolly in toward the warrior.
She stares past the camera with narrowed eyes, jaw set, braids over one shoulder.
A frozen battlefield stretches behind her, smoke rising from distant fires.
Golden-hour backlight rims her silhouette.
Style: 35mm film, Kodak Vision3 500T, desaturated teal shadows, warm highlights.
```

**Fórmula de 6 elementos (nano-banana):** 1 Sujeito (quem / o quê); 2 Composição (enquadramento: ECU, ângulo baixo, aberto); 3 Ação (preparando café, vapor subindo); 4 Local (café quente âmbar); 5 Estilo (fotorrealista, film noir, aquarela); 6 Câmera / luz (profundidade rasa f/1.8, contraluz de hora dourada, correção teal discreta).

**Contraponto para textura de plástico (fixas do antigravity):** acrescente no FIM: `light atmospheric haze, film grain, crush blacks, shadow depth`.

**Contrato de material CGI** (2 a 4 propriedades por superfície para evitar "brilho de plástico"): Base (metal / vidro / tecido / cerâmica / madeira / couro) · Rugosidade (fosco / acetinado / brilhante / espelho) · Imperfeição (arranhões / poeira / desgaste / digitais / pátina) · Borda (chanfrada / afiada / arredondada / com bisel). Exemplo: `A matte ceramic vase with hairline cracks and a subtle patina, soft rounded rim, resting on rough-hewn oak.`

**Método de eficiência do quadro-herói** (economia com imagem barata primeiro): (1) gere de 5 a 10 variações baratas com `etna_imagem_gerar` → ache a mais próxima; (2) refine essa única imagem → acerte exatamente; (3) anime UMA VEZ com `etna_video_gerar(imageUrl=...)` a partir do quadro-herói perfeito. Gaste na geração de imagem barata, bem menos na de vídeo.

**Cauda de zona segura do gpt-image (literal):** `Safe zones: keep the top 10% and bottom 10% of the frame free from text, logos, icons, buttons, and UI elements — photographic content such as hands, arms, or product edges entering the frame is fine.`

---

## O PORTÃO DO LINT: obrigatório antes de toda chamada de renderização

O filtro de conteúdo do Seedance é um **LLM que lê a intenção da cena inteira**, não uma lista de palavras proibidas; mas ele marca
com segurança um punhado de padrões de superfície, e as gerações de vídeo rodadas pelo provedor são jobs assíncronos
em que uma reprovação instantânea desperdiça uma geração de verdade. Rode este portão na string do prompt **antes** de chamar
`etna_video_gerar` / `etna_imagem_gerar`. As mesmas regras de FALHA valem para os dois provedores e para os prompts de quadro-semente
enviados como `imageUrl`.

**Ordem de execução, em todo plano:** 1. Rascunhe o prompt → 2. Rode o lint → PASSA / AVISO / FALHA → 3. **FALHA** = NÃO chame a
ferramenta; reescreva, refaça o lint → 4. **AVISO** = reforce o ponto fraco, siga → 5. **PASSA** = chame a ferramenta. Num time,
todo painel de worker roda este portão por conta própria antes da chamada de geração: um plano ruim não pode gastar uma rodada
paralela do provedor.

**Agregação do veredito:** qualquer FALHA → **FALHA**; senão qualquer AVISO → **AVISO**; senão **PASSA**.

Uma cópia executável e determinística de cada regra abaixo fica em **`scripts/seedance_lint.py`** (saída 0 = PASSA / só AVISO,
saída 1 = qualquer FALHA):
```bash
python3 scripts/seedance_lint.py "<prompt text>"
echo "<prompt>" | python3 scripts/seedance_lint.py
python3 scripts/seedance_lint.py --file prompt.txt
```
O checklist em linha é o **portão padrão**; o script é o equivalente opcional.

### Regras de FALHA: NÃO gere se qualquer uma acertar

**FALHA 1: nome-de-pessoa-real.** Qualquer nome de figura pública real.
> elon musk, donald trump, joe biden, kamala harris, vladimir putin, xi jinping, barack obama, keanu reeves, tom cruise, brad pitt, dicaprio, taylor swift, beyoncé, rihanna, kanye, ye *(não "ye olde")*, kim kardashian, drake *(não "drake's equation")*, travis scott, messi, ronaldo, lebron, michael jordan, mr beast, mrbeast

**Conserto:** `Replace the name with an archetype: age range, build, hair, wardrobe, expression.`

**FALHA 2: marca-ou-IP.** Qualquer marca, franquia, IP, personagem registrado.
> nike, adidas, puma, gucci, prada, louis vuitton, coca-cola, pepsi, mcdonald's, starbucks, apple *(não pie/tree/orchard/falls/juice)*, iphone, macbook, google, microsoft, windows *(não "are/were/of/into")*, tesla, ferrari, lamborghini, porsche, rolex, marvel, dc comics, disney, pixar, dreamworks, spider-man, batman, superman, iron man, captain america, thor, hulk, black widow, wolverine, deadpool, harry potter, hogwarts, pokémon, pikachu, mario, sonic, star wars, jedi, sith, darth vader, james bond, 007

**Conserto:** `Describe visual traits only — geometry, color, material. Never name the brand, franchise, or character.`

**FALHA 3: verbo-de-violência.** Verbos crus de violência / dano. **O filtro marca o VERBO, não o conceito**: represente de forma cinematográfica pelo rescaldo / física.
> kill(s/ed/ing), murder, assassinate, stab, shoot / shot, slash, behead, decapitate, torture, rape, blood / bloody, gore / gory, gutted, dismember, mutilate, fight, attack, punch, beat / beating *(não "beat the rug/eggs/drum/heat/path/odds")*

**Conserto:** `Describe aftermath, tension, force, or direction — not the act. E.g. "driven into the car, metal buckling" instead of "punches".`

**FALHA 4: substantivo-de-arma.** Armas nomeadas são lidas como intenção.
> gun, rifle, pistol, shotgun, handgun, machine gun, ak-47, m16, uzi, knife, dagger, sword *(não "sword fern/fish/dance")*, bomb, grenade, explosive

**Conserto:** `Describe the standoff / silhouette / prop geometry, not the weapon by name.`

**FALHA 5: marcador-de-idade.** Qualquer marcador de idade / menor. **O Seedance é cego para idade.**
> child(ren), kid(s/dies), baby, infant, toddler, boy(s), girl(s), teen(ager/aged), young man/woman/boy/girl, little boy/girl/kid/child, minor *(não "chord/key/scale/league/issue/detail")*, schoolboy, schoolgirl, preschool(er)

**Conserto:** `Seedance is age-blind. Describe by role + clothing + action: "a figure in a wool cloak", "the rider", "the traveler".`

**FALHA 6: excesso de tamanho.** `word_count > 220` costuma derrubar o codificador de texto.
**Conserto:** `Cut to 30–180 words. Keep Style & Mood + camera + action; trim the rest.`

### Regras de AVISO: provavelmente passa, reforce antes de gerar

**AVISO 1: anti-clichê.** Adjetivos de texto publicitário se correlacionam com marcações (sinalizam intenção vaga).
> breathtaking, stunning, epic, mesmerizing, awe-inspiring, masterfully, meticulously, exquisitely, beautifully crafted, cinematic masterpiece, visual feast, seamlessly, effortlessly, flawlessly, cutting-edge, state-of-the-art, mind-blowing, jaw-dropping

**Conserto:** `Replace with observable, measurable details.`

**AVISO 2: longo.** `word_count > 180`. **Conserto:** `Trim least essential details before generating.`

**AVISO 3: curto demais.** `word_count < 15`. O filtro não tem cena. **Conserto:** `Add at least Style & Mood + camera + setting so the shot is legible.`

**AVISO 4: sem estilo-humor.** Sem cláusula de estilo / humor / luz / paleta. Lista de pistas: style, mood, palette, color grade, lighting, atmosphere, golden hour, blue hour, overcast, neon, practical, noir, desaturated, teal and orange, high contrast, low-key, anamorphic, vhs, super 8, cinematic. **Conserto:** `Add one sentence naming the palette, lighting, and atmosphere.`

**AVISO 5: sem câmera.** Sem movimento de câmera. Lista de pistas: camera, dolly, tracking, pan, tilt, crane, steadicam, handheld, aerial, drone, pov, push-in, pull-out, orbit, whip-pan, low-angle, high-angle, overhead, wide shot, medium shot, close-up, ecu, ots, over the shoulder. **Conserto:** `Name an exact movement: "slow dolly-in", "low-angle tracking", "static medium". Not "the camera moves".`

**AVISO 6: sem cenário.** Sem local concreto. Lista de pistas: room, hall, street, alley, forest, desert, beach, kitchen, bedroom, office, warehouse, studio, stage, city, town, village, rooftop, stairwell, parking, interior, exterior, indoor, outdoor, at night, by day, at dawn, at dusk. **Conserto:** `Add a location (interior/exterior, room type, time of day).`

**AVISO 7: contradição interna.** Duas diretivas mutuamente exclusivas num plano. Pares verificados: (moving fast + frozen) · (bright + pitch black) · (dolly in + dolly out) · (crane up + crane down) · (zoom in + zoom out). **Conserto:** `Pick one — split into two shots if you need both.`

### Doutrina da janela de tamanho
| Palavras | Veredito |
|---|---|
| `< 15` | AVISO: curto demais |
| `15 – 180` | **OK** (ideal **30 – 180**) |
| `> 180` | AVISO: longo |
| `> 220` | **FALHA**: excesso de tamanho |

### As três cláusulas obrigatórias (correlação positiva com passar)
Um prompt que passa tem as três; a ausência de qualquer uma → AVISO: (1) Estilo / humor / luz / paleta, (2) movimento de câmera explícito (termo exato, não "the camera moves"), (3) cenário concreto (interior / exterior, local, hora do dia).

### Passe de voz: "Cineasta, não amigo"
Mesmo com todos os tokens de risco removidos, prompts são marcados se a voz estiver errada. Um prompt que soa como **um cineasta descrevendo um plano** tende a passar; um que soa como **um recado para um amigo** tende a falhar. Faça este passe em todo prompt:
1. **Acrescente uma cláusula de Estilo e Humor no início** (paleta, lente, luz, atmosfera): nunca pule. Diz ao filtro "isto é um plano".
2. **Nomeie o movimento de câmera** ("slow dolly-in", não "the camera moves forward").
3. **Descreva física, não emoção** ("jaw clenches, nostrils flare", não "looks angry").
4. **Descreva força e direção, não sequência de destruição** ("driven into the car, metal buckling", não "thrown into door, glass shatters, sweep leg").
5. **Presente, voz ativa** ("she turns", não "she is turning").
6. **Corte as palavras de anti-clichê.**

### Playbook de reescrita: FALHA → PASSA
| Gatilho | Antes → Depois |
|---|---|
| **nome real** | `Keanu Reeves` → `a lean man in his late 50s, dark shoulder-length hair, stubble, intense calm expression, dark suit` |
| **marca / IP** | `Spider-Man` → `blue-and-red form-fitting suit, face masked with white eye-shaped lenses, web fired from wrists`; `a Coca-Cola can` → `a slim red aluminium can, white ribbon graphic, condensation beading` |
| **verbo de violência** | `he punches the man` → `the figure is driven into the car, metal buckling`; `blood drips from his hands` → `his hands tremble at his sides, something dark stains his sleeve` |
| **substantivo de arma** | `he raises a gun` → `he raises a dark L-shaped object, arm locked, the other figure freezes` |
| **horror / escuro** | sangue → `unsettling`, `something is wrong`, `dread`; descreva movimento / luz no momento de horror, nunca a lesão explícita |
| **marcador de idade** | `a young boy runs` → `a small figure in a wool cloak runs`, `the rider`, `the traveler` |
| **upload de rosto real** | Não alimente com foto real. Gere antes um personagem sintético com `etna_imagem_gerar` → passe o png devolvido como `imageUrl`. |

**Conversão para restrição positiva** (o Seedance / fal não tem campo de prompt negativo: dobre as exclusões dentro do prompt positivo): `no shaky camera` → `locked-off static camera, no movement`; `no blur` → `sharp focus throughout, deep depth of field`; `don't make it dark` → `bright, evenly lit, overcast daylight`; `avoid jittery motion` → `smooth, fluid motion, one action per shot`; `no extra limbs` → `anatomically correct, all limbs naturally positioned`; `don't change the character` → `consistent character appearance, same outfit and features throughout`.

---

## Falha instantânea x falha tardia: o diagnóstico

`etna_video_gerar` é assíncrono. Quando volta com falha, o **momento** da falha é o diagnóstico mais útil:

| Momento da falha | Significado | O que fazer |
|----------------|---------|------------|
| **< 10 segundos** (instantânea) | Reprovação pelo filtro de conteúdo: o prompt nunca chegou à GPU | Reescreva a voz + tire os tokens de risco. NÃO chame de novo sem mudança. |
| **> 30 segundos** (tardia) | Infraestrutura / tempo esgotado / complexidade: o prompt passou no filtro, a renderização falhou | Simplifique a densidade de ação, corte o tamanho, tente de novo. |

**Falhas instantâneas em loop = problema de filtro, nunca da GPU.** Pare de chamar a ferramenta antes da reescrita. Chamar de
novo com o mesmo prompt mudando uma palavra é o loop que desperdiça chamadas.

---

## Catálogo de falhas de renderização: quando a renderização em si quebra (falha tardia)

São falhas de renderização (o prompt passou no filtro; a saída está errada), distintas das reprovações do filtro. Cada uma: sintoma → mecanismo → contraponto no prompt.

**Deriva de fps.** Reprodução picotada, quadros consecutivos duplicados. O Seedance reduz a taxa sob carga e preenche com repetições. Contraponto: declare a taxa de quadros **no corpo do prompt**: `The video runs at 24 fps. No frame is repeated.` (Não há parâmetro de fps na ferramenta: o corpo do prompt é o *único* lugar onde o fps vive.)

**Falso positivo de NSFW.** Um prompt limpo volta reprovado como NSFW. Especificidade de anatomia / vocabulário de figurino / frase sensual-mas-limpa dispara o classificador em conteúdo inocente. Contraponto: (1) generalize detalhes de anatomia (`her bare shoulders` → `her shoulders`; `tight-fitting dress` → `fitted dress`); (2) troque adjetivos de registro sensual (`sultry` → `composed`; `seductive` → `direct`); (3) refaça o lint. Não chame de novo sem mudança.

**Invenção de quadro-chave.** O prompt exige um elemento ausente da `imageUrl` de origem (`pulls a Polaroid off the fridge`) e o Seedance fabrica ele E a posição, contradizendo a geometria. Contraponto: declare a ausência: `The Polaroid is not visible on the fridge in the source frame; it appears when the character lifts their hand from below the frame.`

**Deriva de física (objeto vizinho).** Um objeto se comporta errado quando um objeto vizinho se move (o ímã voa junto com a Polaroid). Não há simulação de física imposta. Contraponto: declare o invariante: `The magnet stays attached to the fridge surface throughout. Only the Polaroid moves.`

**Sobrecarga de movimento múltiplo.** Movimentos empilhados (na mão + subida + empurrão + troca de foco) lêem como instabilidade. Contraponto: **um movimento dominante por plano.** Para um movimento composto, declare as fases em sequência com tempo: `Camera rises 0–3s, holds, then pushes in 4–8s`.

**Falhas de percepção espacial.** Planos de entrada por porta / corredor / atravessar móveis falham mais que os estáticos. Geometria mal especificada → padrão plausível que discorda da intenção. Contraponto: trave a geometria com um Bloco de Layout Espacial antes da ação: `Camera inside the room, facing the closed door. The couch sits between the character and the camera. The character walks around the couch from screen-left to screen-right.`

---

## Solução de problemas no nível do plano: sintoma → causa → conserto

O Seedance produz **cerca de 90% de saída utilizável** quando o prompt está limpo. **Se a saída está CONSISTENTEMENTE ruim em várias tentativas, o PROMPT é o problema, não o modelo.** Uma saída ruim isolada é ruído (refaça uma vez). Um *padrão* é sinal (conserte a string); refazer na força bruta queima outro job assíncrono e reproduz o defeito.

### O diagnóstico em 6 passes (rode em ordem, pare no primeiro acerto)
```
Saída ruim?
├── 1. Borrada / tremida / deformando → prompt > 100 palavras?
│      ├── Sim → corte para 30–100 palavras; troque 50+ palavras de descrição por uma âncora imageUrl
│      └── Não → densidade de batidas alta (>2/5s)? → divida em vários planos
├── 2. Câmera caótica / girando → quantos movimentos de câmera?
│      ├── Vários → reduza a um movimento principal (regra de um só movimento)
│      └── Um      → nomeie exatamente em linha própria: "Camera: Dolly In"
├── 3. Personagem / produto não bate → o prompt descreve a aparência dele?
│      ├── Sim → APAGUE toda descrição física; mantenha só ação + emoção (a âncora carrega a identidade)
│      └── Não → imagem de âncora fraca → refaça a âncora (frontal + 3/4 + perfil, luz uniforme)
├── 4. Ação fraca / dura → há linguagem de física?
│      ├── Não → acrescente advérbios de grau + consequências físicas
│      └── Sim → reduza a densidade de batidas (1–2 batidas/5s)
├── 5. i2v parado / quase não mexe → redescrevendo o que já está na imagem?
│      └── Sim → descreva SÓ o que muda / move + movimento de câmera explícito + movimento atmosférico
└── 6. "Só ruim" (vago) → rode o linter anti-clichê
       ├── Achou clichê → troque por detalhes observáveis e mensuráveis
       └── Limpo → tente outro enquadramento de estilo / gênero, ou reforce a âncora imageUrl
```

A ordem dos passes é o peso dos tokens: Sujeito → Ação → Câmera → Estilo → Áudio → Saída. A maioria das falhas cai nos passes 1 / 2,
porque os tokens do começo do prompt dominam. Se você chegar ao passe 4 sem mexer no resultado, o prompt precisa de reescrita estrutural,
não de mais iteração.

### Tabela de sintomas
| Sintoma | Conserto (reescreva o prompt) |
|---|---|
| Rosto do personagem inconsistente / deformando | Passe uma âncora `imageUrl`; remova linhas de aparência contraditórias. No i2v, não redescreva o rosto. |
| Personagem / produto não bate com a âncora | **Apague TODAS as descrições físicas. Descreva SÓ ação e emoção. A âncora carrega a identidade.** |
| Movimento de câmera genérico | Use um movimento nomeado exato, em linha própria: `Camera: Dolly In`. |
| Câmera caótica / girando | UM movimento principal por plano; divida o resto em planos separados. |
| Prompt ignorado / não bate | Corte para menos de 200 palavras. Remova contradições. Comece com Sujeito → Ação → Câmera → Estilo. |
| Borrado / tremido / deformando | Corte para 30–100 palavras; troque 50+ palavras por uma âncora `imageUrl`. |
| Estilo visual errado / genérico | Acrescente um estilo nomeado (VHS / Super 8 / Anamórfico) + correção de cor + luz; declare a proporção como linguagem. |
| Ação dura | Acrescente advérbios de grau + consequências físicas (`dust erupts`, `sparks fly`). |
| Efeito de VFX não aparece | Descreva o efeito literalmente no FIM; garanta que a cena sustenta o efeito. |
| VFX caricato | Acrescente `photorealistic, physically accurate`. |
| i2v quase não mexe | Descreva SÓ o que muda; acrescente movimento de câmera explícito + movimento atmosférico. **Conserto nº 1 do i2v.** |
| Foto de produto barata / com luz estourada | Especifique a superfície do fundo + luz específica + pista de textura. |
| Horror / escuro bloqueado | Descreva resultados, não atos (`aftermath`, `dread`); linguagem de atmosfera (`unsettling`, `wrong`). |
| "Não era o que eu queria" (vago) | Rode o linter anti-clichê. |

### Regras estruturais (literais)
- **Regra de um só movimento**: UM movimento de câmera principal por plano; vários → divida em vários planos.
- **Divisão por densidade de batidas**: 1–2 batidas/5s; >2/5s → divida em vários planos.
- **Apague a aparência para bater com a referência**: `imageUrl` de âncora em jogo → apague TODAS as descrições físicas; descreva SÓ ação e emoção.
- **Linter anti-clichê**: troque `beautiful`/`stunning`/`epic`/`amazing`/`dynamic` por detalhes observáveis e mensuráveis. **O teste da mensurabilidade**: uma câmera, um fotômetro ou um cronômetro consegue medir essa palavra? Se não → apague.
- **Conserto de excesso de especificação**: corte para 30–100 palavras; use âncora no lugar de 50+ palavras. Teto: menos de 200 palavras.
- **Ordem de abertura**: Sujeito → Ação → Câmera → Estilo.
- **Iteração de uma variável só**: mude exatamente UMA coisa por nova rodada. Senão você não consegue atribuir a melhora e desperdiça jobs assíncronos. (Exceção: depois que o prompt estiver travado e você variar só para explorar estilo, agrupar é aceitável.)
- **Regra dos 80%**: se 80% da geração estava certa, mantenha esses 80% (sujeito, estilo, câmera, luz); conserte só o erro.

### Escalada para conteúdo bloqueado
Se três reescritas de atmosfera ainda forem bloqueadas, o conceito está fora da política: pare e diga à pessoa. Não force variações na marra.

---

## Formato de saída para um prompt do Seedance

Proporção / duração / fps são **conteúdo do prompt**, não parâmetros da ferramenta:
```
Aspect ratio: 16:9. Duration: 10s. 24 fps, no repeated frames.

Style & Mood: [paleta, lente, luz, atmosfera: 1 frase]

Dynamic Description: [movimento de câmera + sujeito + ação, presente, plano a plano se houver vários cortes: o bloco principal]

Static Description: [local, adereços, detalhes do ambiente: 1 a 2 frases]

Camera: [nome exato do movimento]
```
Os rótulos de seção são opinião de ofício, não regra do motor. Use parágrafo corrido em prompts com menos de 50 palavras; use
a estrutura com seções só quando o prompt tiver batidas discretas.

**Aritmética de duração de vários planos:** a duração precisa bater na linha de metadados (`Duration: Xs`) e em cada rótulo de tempo
de plano. Rotule cada plano em linha — `Shot 1 (0–3s): ... hard cut to Shot 2 (3–8s): ...` — e os rótulos por plano têm que **somar**
o total. **Antipadrão:** rótulos de tempo a cada 3 segundos dentro de um único plano contínuo: o Seedance lê qualquer bloco de
tempo por segmento como instrução de corte. Para continuidade, tire as marcas de tempo; para cortes, rotule `Shot 1 / Shot 2 / Shot 3`
e use a aritmética.

**Checklist de autocorreção (60 a 90 s antes de cada chamada):** o fps está declarado no corpo do prompt? proporção + duração declaradas
como linguagem de estilo? tokens de anatomia / sensuais limpos? elementos que aparecem pela primeira vez marcados como ausentes da
`imageUrl` de origem? invariantes de objetos vizinhos nomeados? um movimento de câmera dominante (o composto dividido em fases)?
geometria travada com um Bloco de Layout Espacial quando há mais de um sujeito ou entrada por porta / corredor / contornando móveis?
lint aprovado (nenhuma FALHA, AVISOS tratados)? passe de voz feito?

---

## Realidade da taxa de aceitação

A produção de cinema com IA em nível de entrega fica em cerca de **1,0% de aceitação de imagem e 1,5% de aceitação de vídeo**
(confirmado quatro vezes entre sessões). O ciclo de iteração É o ofício: `iteration burn is the work, not the failure`. A âncora de
1,5% de vídeo implica ~67 tentativas para acertar um aproveitável; multiplique pelo número de planos. Um plano de estabelecimento de 10 s ≈
72 gerações (trate como teto). Um personagem que aparece em dezenas de planos justifica um adiantamento de ~800 iterações para travar a
folha de âncora; um personagem em 1 ou 2 planos não justifica. Tratar cada take recusado como fracasso encerra o projeto no dia 7.
Oriente o orçamento pelas gerações.

---

## Lacunas de capacidade: diga com honestidade, não invente

| O que a ferramenta de referência tinha | Situação no Etna |
|---|---|
| Referências com múltiplas alças (`@Image1..4`, `@Video1`, `@Audio1`) | **Lacuna.** Uma `imageUrl` por chamada, um papel de referência por plano. |
| Entrada de vídeo como referência de movimento | **Lacuna.** Descreva o movimento em texto. |
| Macros de predefinição de movimento nomeadas | **Lacuna.** Descreva o efeito literalmente. A lista de predefinições sobrevive só como catálogo de vocabulário. |
| Áudio e vídeo conjuntos nativos | **Lacuna.** O mp4 do Seedance é mudo. Áudio = trilha TTS da ElevenLabs em separado (etna-cinema-voice). Sem música / efeito sonoro / BGM. |
| Edição / reestilização / referência de imagem | **Suportado.** `etna_imagem_gerar(prompt, imageUrl=...)` faz imagem-para-imagem (edição nano-banana / edição gpt-image). Sem parâmetro discreto de máscara / inpaint: descreva a mudança no prompt. Ainda assim, texto nítido / logo / infográfico vai PARA FORA, para o Remotion (o Seedance alucina texto). |
| Expandir plano / editar plano in loco | **Lacuna.** Refilme por referência, ou encaminhe para o Remotion. |
| Sincronia labial de verdade / apresentador falando | **Fora do escopo.** Só o contorno MANUAL documentado (geração por personagem + composto de imagem-no-canto): sinalize antes de prometer. |
| Ampliação de resolução / troca de elenco | **Lacuna.** Indisponível. |
| Trava de personagem Soul ID (recurso de terceiros) | **Lacuna.** Leve o personagem por um png de referência gerado, passado como `imageUrl`, ou por um último quadro extraído. |
| Memória persistente de regras do filtro | **Adiado.** O playbook de reescrita inline é a memória por enquanto. |

**Encaminhe para fora a tipografia nítida:** qualquer intenção que seja texto legível na tela, logo, infográfico, visualização de dados, faixa inferior ou cartão de título NÃO pertence a um prompt do Seedance: encaminhe para as skills de Remotion do Etna (`remotion-best-practices`, `video-post`, `reels-editor`) e componha. O Seedance cuida de movimento e atmosfera; o Remotion cuida de tipografia nítida. Sintoma de "motor errado, não prompt ruim": a pessoa fica refazendo para um texto / número / logo renderizar legível: nenhuma correção de prompt resolve isso no Seedance.

---

## O contrato de divisão de camadas

Esta skill é a camada de **construção do prompt + disciplina de produção**. As ferramentas de mídia do Etna são a camada de execução: cuidam do envio do job, da consulta assíncrona e da devolução do caminho do mp4 / png. A skill escreve a string do prompt e decide o que entra nela; **nunca inventa parâmetro de ferramenta** (não há parâmetro de proporção / duração / fps: eles vão no corpo do prompt como linguagem de estilo).

Skills irmãs do cinema: o **etna-cinema-plan** é dono da lista de planos e da distribuição do coordenador para os workers; o **etna-cinema-cut** é dono da extração de quadros com ffmpeg (cadeias de continuação), da montagem por concatenação e do encaminhamento para o Remotion; o **etna-cinema-voice** é dono da trilha separada de narração em TTS da ElevenLabs. Você — **etna-cinema-shot** — é dono do plano: escreve, passa no lint, dispara `etna_video_gerar` / `etna_imagem_gerar`.
