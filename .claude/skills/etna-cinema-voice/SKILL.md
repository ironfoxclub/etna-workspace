---
name: etna-cinema-voice
description: "Use when a squad worker must generate NARRATION or VOICEOVER for a video or ad via ElevenLabs TTS (etna_voz_gerar). Covers dialogue / VO writing craft, per-character voice pinning (voiceId), pacing for sync, and the hard rule that audio is a SEPARATE post-layered track. Bind to the render-audio worker. Triggers: voiceover, narration, TTS, dialogue, VO, spoken audio, voice."
---

> **Mídia no Etna (vale sobre qualquer outra menção neste arquivo).** Ferramentas MCP do Etna: `etna_imagem_gerar(prompt, outPath, provider?, imageUrl?, formato?)`, `etna_video_gerar(prompt, outPath, provider?, imageUrl?, endImageUrl?, formato?, segundos?)`, `etna_voz_gerar(prompt, outPath, voiceId?)` e `etna_midia_provedores()` (quem está pronto, a escolha da pessoa e o modelo de cada um; nunca mostra chave). Provedores: imagem = `antigravity` (padrão, plano do Google, sem chave) | `higgsfield` | `gemini` | `openai` | `fal`; vídeo = `higgsfield` (Seedance) | `fal` (Kling: o único que respeita `endImageUrl`, e o Etna já o escolhe sozinho quando você passa `endImageUrl`); voz = `elevenlabs`. Não passe `provider` a menos que a tarefa exija: vale a IA que a pessoa escolheu em Configurações › Imagem e vídeo. O Antigravity NÃO gera vídeo. `outPath` é relativo à pasta do painel. Sem provedor pronto a ferramenta diz o que falta: pare e avise a pessoa; nunca troque de motor em silêncio. Os nomes antigos (`google-image`, `openai-image`, `replicate-video`, `selectedModel`/`enabledModels`) = `antigravity`/`gemini`, `openai`, `fal` e o campo `modelo` de `etna_midia_provedores`.


# etna-cinema-voice — A skill de voz

Escreve a fala e a renderiza pelo TTS da ElevenLabs como uma trilha SEPARADA. É o menor papel do cinema: só
VOZ, encaixada na pós-produção, nunca gravada dentro do mp4 mudo do Seedance.

Este é o kit do worker de áudio de renderização. Ele é dono do **texto da narração/locução** e da **chamada de
TTS**, e de mais nada. Os irmãos: `etna-cinema-plan` escreve o prompt de vídeo do Seedance, `etna-cinema-shot`
escreve o prompt da imagem/quadro-chave, `etna-cinema-cut` monta e faz a mux com o ffmpeg. Esta skill entrega ao
`etna-cinema-cut` um arquivo de áudio; o `etna-cinema-cut` o põe por cima do mp4 mudo.

## Superfície de execução (fixa: nunca reinvente a chamada)

| Camada | Ferramenta | Recebe | Devolve |
|-------|------------|--------|---------|
| Áudio | `etna_voz_gerar(prompt, outPath, voiceId?)` | Só TTS da ElevenLabs. `prompt` = o texto falado. `voiceId` = voz opcional da ElevenLabs. | caminho do arquivo de áudio |

Não existe outro motor de áudio. Sem geração de música, sem efeito sonoro, sem BGM, sem sincronia labial, sem
ampliação. Diga isso em voz alta quando um briefing pedir qualquer um deles (veja Lacunas de capacidade).

---

## A regra firme: o áudio é uma trilha separada, em camada

O mp4 devolvido por `etna_video_gerar` (Seedance) é **MUDO**. O áudio é uma trilha separada, de pós-produção,
produzida aqui por `etna_voz_gerar` e misturada pelo `etna-cinema-cut` com o ffmpeg.

Portanto:
- **NUNCA** escreva blocos `Audio:` / `BGM:` / `SFX:` dentro de um prompt de vídeo do Seedance esperando que
  eles sejam renderizados: não serão. Esses blocos servem só como *direção de planejamento* que a camada de
  montagem lê.
- **NUNCA** presuma que a fala está "dentro" do vídeo. Ela é um arquivo à parte. A ordem das operações é: (1) o
  vídeo sai mudo, (2) você renderiza aqui o arquivo da locução, (3) o `etna-cinema-cut` faz a mux com
  `ffmpeg -i shot.mp4 -i vo.mp3 -c:v copy -c:a aac -shortest out.mp4`.
- A linha `Audio:` do corpo de 5 blocos do Seedance e qualquer fala entre aspas no prompt de vídeo são
  **direção**, não saída. Falas e linhas citadas são roteadas PARA CÁ, para `etna_voz_gerar`; notas de ambiente,
  efeito sonoro e `No music.` são só orientação de mixagem para a montagem.

---

## Ofício de escrita de diálogo / locução

Você escreve para um motor de TTS, não para um ator de tela. Tudo o que molda a leitura tem que estar no
**texto**: não existe parâmetro separado de emoção, estilo ou sotaque. Cinco regras:

**1. Frases curtas.** O TTS degrada em frases longas e empilhadas de vírgula (prosódia de correria, respiração
perdida). Escreva frases do tamanho da fala. Uma ideia por linha. Prefira 8 a 14 palavras por frase na narração;
menos para locução enxuta.

**2. O tom emocional vai nas palavras e na pontuação**, não num parâmetro.
- Ritmo pela pontuação: ponto é parada completa, vírgula é uma pausa curta, travessão é uma pausa segurada,
  reticências são uma deriva no fim.
- Ênfase pela forma da frase e pela escolha da palavra, não por CAIXA ALTA (o TTS pode soletrar ou gritar caixa
  alta de forma imprevisível). Reestruture para que a palavra forte caia no fim da oração.
- Ponto de interrogação e de exclamação DE FATO mudam a prosódia: use com intenção e com moderação.

**3. Sotaque e variedade ficam no TEXTO**, porque isto é TTS. Não existe botão de "sotaque". Para colorir a leitura:
- Escolha um `voiceId` cujo sotaque nativo já bata (a alavanca confiável: fixe a voz, veja abaixo).
- Molde a *grafia e a frase* para a cadência: contrações e letras cortadas para registro casual (`tá`, `pra`,
  `cê`), palavras cheias e formais para registro clínico. A grafia fonética nudge a cadência, mas é uma alavanca
  fraca: a escolha do voiceId domina.
- Não espere que o motor "faça um sotaque irlandês" a partir de uma indicação de cena no prompt. Ele lê as
  palavras; não recebe direção de cena.

**4. Decomponha leituras emocionais genéricas.** Mesma disciplina da regra visual de emoção: "diga com tristeza"
diz pouco ao TTS. Escreva a linha de modo que *as palavras e o ritmo* carreguem o estado: fragmentos curtos e
reticências no fim para derrota; declarativas secas para raiva; orações ascendentes para esperança. A
interpretação vive no roteiro, não num adjetivo.

**5. Só o texto falado no prompt.** O argumento `prompt` são as palavras a serem faladas: não enfie notas de
câmera, descrição de cena nem indicações como `[narrador, sombrio]`; elas seriam lidas em voz alta. Mantenha o
prompt como texto limpo para falar.

---

## Fixação de voiceId por personagem

Para qualquer sequência com mais de um falante, **fixe um voiceId por personagem** e reutilize-o palavra por
palavra em toda linha que o personagem fala: é o análogo, no áudio, do bloco de identidade reutilizado que trava
o rosto de um personagem nos quadros.

- Um personagem = um `voiceId`, fixo no projeto inteiro. Mantenha uma tabelinha nas suas anotações de trabalho:
  `Narrador → <voiceId>`, `Protagonista → <voiceId>`, etc.
- Omita o `voiceId` só numa narração de voz única em que a voz padrão é aceitável.
- Cada linha falada é a SUA própria chamada de `etna_voz_gerar` (uma por linha / por turno de personagem). Não
  junte dois personagens num só prompt: não dá para trocar de voz no meio do prompt. Renderize cada turno à
  parte; o `etna-cinema-cut` os ordena.
- Entre os painéis do time, o `voiceId` por personagem é o contrato de continuidade do som: todo painel que
  renderiza a fala daquele personagem passa o MESMO `voiceId`, do mesmo jeito que todo painel que renderiza o
  rosto daquele personagem reutiliza o MESMO bloco de identidade / a mesma imagem do herói.

---

## Ritmo para caber na duração do plano

A locução tem que caber no plano sobre o qual ela entra. Nem a chamada de vídeo nem a de áudio tem parâmetro de
duração, então o ritmo se controla pela **contagem de palavras** e pela **pontuação**.

- Estime o tempo de leitura em cerca de **2,5 a 3 palavras por segundo** de fala natural de narração (mais lento
  para o sombrio/clínico, mais rápido para UGC enérgico). Um plano de 10 segundos ≈ 25 a 30 palavras faladas.
- Escreva para a duração do plano e depois confira: renderize a locução, leia a duração do arquivo devolvido e
  compare com a duração do mp4 mudo.
  - Locução longa demais → corte palavras (não acelere; não existe retime no app). Enxugue a frase.
  - Locução curta demais → acrescente uma batida, uma pausa segurada (travessão) ou uma oração final, ou deixe o
    `etna-cinema-cut` completar com ambiente/silêncio.
- Em sequências com vários planos, ajuste cada linha pelo SEU plano, não pelo filme inteiro. Uma linha de
  locução por plano é a unidade limpa.
- Use a pontuação para esticar ou comprimir uma contagem fixa de palavras: reticências e travessões somam tempo
  segurado sem somar palavras; declarativas com poucas vírgulas leem mais rápido.

---

## Lacunas de capacidade: diga em voz alta

`etna_voz_gerar` é **TTS da ElevenLabs = SÓ VOZ**. Diga isso com honestidade; não invente contornos:

1. **SEM música.** Nada de BGM, trilha ou jingle. A música vem de fora desta skill, por completo.
2. **SEM efeito sonoro.** Nada de whoosh, impacto, cama ambiente nem foley. O desenho de som é obtido ou produzido em
   outro lugar; o mp4 é mudo e continua mudo, exceto pela trilha de voz que você acrescenta.
3. **SEM sincronia labial.** Não existe ferramenta de lip-sync. **Apresentador falando para a câmera está FORA do
   escopo.** A boca de um clipe do Seedance não vai bater com os fonemas da fala do TTS.
   - O ÚNICO contorno documentado é um **truque MANUAL e sinalizado, não um caminho suportado**: gere um clipe por
     personagem, renderize a fala à parte aqui, e componha a cabeça falante como imagem-no-canto sobre um plano
     aberto no ffmpeg/Remotion (via `etna-cinema-cut`). **Os lábios não vão bater com os fonemas.** Avise a pessoa
     dessa limitação ANTES de prometer qualquer entrega de apresentador falando.
4. **SEM música/efeito mesmo quando um bloco `Audio:` do Seedance pedir**: esse bloco é só direção e nunca é
   renderizado.

Quando um briefing pedir música ou efeito, diga com clareza: "Música e desenho de som estão fora do escopo desta
ferramenta: eu consigo renderizar a narração; a cama de áudio precisa ser obtida à parte." Não deixe o pedido cair
em silêncio nem finja que existe um contorno.

---

## Exemplos trabalhados

**Narrador único, anúncio de produto (plano de ≈10 s, ≈28 palavras):**
```
etna_voz_gerar(
  prompt: "Algumas manhãs pedem mais. A xícara que guarda o calor — e o silêncio.
           Despeje devagar. Deixe começar.",
  voiceId: "<voiceId-do-narrador>"
)
```
Guiado por ponto, travessão para uma batida segurada, declarativas curtas. O tom está nas palavras.

**Dois personagens, anúncio estilo entrevista ou DM: DUAS chamadas separadas, voz fixa por falante:**
```
etna_voz_gerar(prompt: "Espera, você já experimentou de verdade?",
                         voiceId: "<voiceId-do-amigo>")
etna_voz_gerar(prompt: "Eu estava desconfiado. Depois, não estava mais.",
                         voiceId: "<voiceId-do-protagonista>")
```
Cada turno é uma chamada própria; o `etna-cinema-cut` ordena e espaça. Nunca um prompt só para os dois.

**Registro casual de UGC (sotaque na grafia e na frase, não num botão):**
```
etna_voz_gerar(
  prompt: "Tá, eu não ia postar isso, mas... pois é. Esse é o certo.",
  voiceId: "<voiceId-do-ugc>"
)
```

---

## Checklist antes da chamada de TTS

1. **Prompt só com fala**: o `prompt` é texto limpo e falável; sem indicações de cena, notas de câmera nem rótulos
   entre colchetes que seriam lidos em voz alta.
2. **voiceId fixo**: cada personagem mapeado para um `voiceId` fixo, reutilizado palavra por palavra; uma chamada
   por turno de personagem.
3. **Ritmo do plano**: contagem de palavras ≈ segundos do plano × 2,5 a 3; confira contra a duração do mp4 mudo
   depois de renderizar.
4. **Tom no texto**: emoção e sotaque carregados pela escolha das palavras, pela pontuação e pelo voiceId, não por
   um parâmetro (que não existe).
5. **Trilha separada confirmada**: a saída é um arquivo de áudio entregue ao `etna-cinema-cut` para a mux com
   ffmpeg; nada foi escrito dentro do prompt do Seedance esperando que fosse renderizado.
6. **Lacunas sinalizadas**: se o briefing sugeriu música / efeito / sincronia labial / apresentador falando, a
   limitação foi dita à pessoa, não contornada em silêncio.

---

## Referências cruzadas

- `etna-cinema-plan`: escreve o prompt de vídeo do Seedance; o bloco `Audio:` e as falas entre aspas ali são
  DIREÇÃO que roteiam para esta skill, não saída que o mp4 renderiza.
- `etna-cinema-shot`: o análogo da continuidade visual: o reaproveitamento do bloco de identidade / da imagem do
  herói trava o rosto, do mesmo jeito que o reaproveitamento do `voiceId` por personagem trava a voz.
- `etna-cinema-cut`: recebe o arquivo de áudio da locução e o mistura sobre o mp4 mudo com o ffmpeg; é dono do
  composto de apresentador em imagem-no-canto (o truque manual e sinalizado de sincronia labial) e de qualquer
  preenchimento/ajuste de tempo da trilha de voz em relação ao corte.
