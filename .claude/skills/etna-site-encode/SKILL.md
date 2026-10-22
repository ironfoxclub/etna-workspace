---
name: etna-site-encode
description: "Use when a squad worker must ENCODE a generated clip for web delivery — transcode to mp4 (h264 +faststart) and webm (vp9), extract a poster PNG (first frame), strip audio (muted), make a background loop seamless, and emit hero aspects/sizes (16:9, 21:9, vertical). Bind to the site editor / executor worker that has Bash. Triggers: web encode, mp4 webm, faststart, poster frame, muted video, seamless loop, hero aspect, vp9 h264, ffmpeg web."
---

# etna-site-encode — Codificação para entrega na web (ffmpeg)

O worker que é dono do ffmpeg **para a web**. O worker de renderização (`etna-site-scrub`) entrega um mp4 cru; esta
skill transforma isso no arquivo que o navegador quer de fato: um herói pequeno, de início rápido, mudo, em dois
codecs, com quadro de capa. Sem editor não linear: ffmpeg puro, sempre.

> **Divisão de camadas.** O `etna-site-scrub` é dono da geração (quadros-chave + movimento Kling/Seedance). Esta
> skill é dona da **transcodificação + entrega**: codecs, faststart, capa, mudo, continuidade do loop, variantes de
> proporção e tamanho e, **para um herói de scrub, a extração de quadros numa sequência numerada de imagens** (a
> entrega rolagem → índice de quadro; um MP4 embutido rolado por `currentTime` engasga). Ela não gera quadros: ela
> condiciona o mp4 renderizado para o `<video>` (loops / clipes de capa) ou o extrai numa sequência (scrub).

---

## O que entra / o que sai

| Entra | Origem |
|---|---|
| Clipe mp4 cru (muitas vezes com áudio, sem ajuste para a web): **um por SEGMENTO (modo 3) ou por PLANO (modo 1); clipe único para o modo 2** | `etna-site-scrub` via `handoff_submit` |
| Formato(s) de saída | O briefing: herói de scrub / loop de fundo / clipe de capa |
| Proporção e tamanho finais | O layout do site (16:9, 21:9 cinematográfico, vertical 9:16) |

| Sai |
|---|
| `hero.mp4`: h264, `+faststart`, mudo (loops / clipes de capa) |
| `hero.webm`: vp9, mudo (menor; o `<source>` moderno) |
| `hero-poster.png`: primeiro quadro (aparece antes do vídeo pintar / enquanto carrega) |
| `frames/%04d.jpg`: **sequência numerada de imagens (o entregável do herói de scrub; rolagem → índice de quadro)** |
| Variantes opcionais de proporção/tamanho |

---

## Tarefa 1: a codificação web canônica (mp4 + webm + capa, mudo, faststart)

Rode as três para todo herói. O `<video>` recebe as duas fontes; o navegador escolhe.

```bash
# 1. mp4: h264, faststart (átomo moov no início → começa a tocar antes de baixar tudo), MUDO
ffmpeg -i raw.mp4 \
  -an \
  -c:v libx264 -profile:v high -pix_fmt yuv420p \
  -crf 20 -preset slow \
  -movflags +faststart \
  hero.mp4

# 2. webm: vp9, MUDO (costuma ficar 20 a 40% menor que o h264 na mesma qualidade)
ffmpeg -i raw.mp4 \
  -an \
  -c:v libvpx-vp9 -b:v 0 -crf 32 -row-mt 1 \
  hero.webm

# 3. capa: primeiro quadro em PNG (o marcador <video poster=...>)
ffmpeg -i raw.mp4 -frames:v 1 -q:v 2 hero-poster.png
```

- **`-an`**: tira o áudio. Heróis web são mudos por contrato (o navegador já bloqueia autoplay com som). Inegociável.
- **`-movflags +faststart`**: move o átomo moov para o início do arquivo, para o navegador começar a tocar / **rolar** antes de o arquivo inteiro chegar. **Obrigatório para um herói de scrub**: sem ele, as buscas de `currentTime` travam esperando o moov no fim.
- **`-pix_fmt yuv420p`**: o único subamostragem de croma que o Safari/iOS decodifica num `<video>`. Sem isso, o clipe fica preto no iPhone.
- **`-crf 20` (h264) / `-crf 32` (vp9)**: visualmente quase sem perda, num tamanho sensato. Suba o CRF (arquivo menor) para loops de fundo; baixe para um scrub cheio de detalhe.

O marcador que consome a saída:

```html
<video autoplay muted loop playsinline poster="hero-poster.png">
  <source src="hero.webm" type="video/webm">
  <source src="hero.mp4"  type="video/mp4">
</video>
```

> Para um **herói de scrub**, tire `autoplay loop` e ligue o `currentTime` à rolagem em JS; mantenha `muted playsinline
> poster` e `+faststart` (o faststart importa *mais* no scrub: cada busca passa pelo moov).

---

## Tarefa 2: loop de fundo contínuo

Um loop de fundo não pode dar um salto visível na volta. Duas alavancas, em ordem de preferência:

**A. O clipe foi autorado para fazer loop** (último quadro ≈ primeiro quadro: o `etna-site-scrub` fez isso). Aí basta
codificar; a volta já é invisível. Confira:

```bash
ffmpeg -i raw.mp4 -frames:v 1 -q:v 2 first.png
ffmpeg -sseof -0.1 -i raw.mp4 -frames:v 1 -q:v 2 last.png
# compare first.png com last.png a olho: quase idênticos → a emenda é invisível
```

**B. Crossfade na volta** (quando as pontas não batem). Sobreponha a cauda sobre o início com um xfade curto, para o
ponto de loop se dissolver:

```bash
# D = duração do clipe, X = segundos do crossfade (ex.: 0.5). OFF = D - X.
ffmpeg -i raw.mp4 -filter_complex \
  "[0]split[a][b];[b]trim=start=${OFF},setpts=PTS-STARTPTS[tail];\
   [a]trim=end=${OFF},setpts=PTS-STARTPTS[head];\
   [head][tail]xfade=transition=fade:duration=${X}:offset=$(echo "$OFF - $X" | bc)" \
  -an looped.mp4
```

**C. Fade em JS** (quando o loop toca no `<video>` e a volta ainda aparece). Em vez de um xfade do ffmpeg, o *site*
faz o crossfade no ponto de loop: quando o clipe se aproxima do fim, a opacidade cai e uma segunda camada (ou a mesma,
reiniciada) entra, então o corte seco se dissolve no navegador. É o truque de "loop contínuo" do mercado para vídeo de
fundo: vive na página, não no arquivo:

```js
// loop de fundo contínuo: desvanece os últimos ~0,4 s na volta
const v = document.querySelector('#bg-loop'), FADE = 0.4;
v.addEventListener('timeupdate', () => {
  const left = v.duration - v.currentTime;
  v.style.opacity = left < FADE ? (left / FADE).toFixed(2) : 1; // desvanece a cauda
});
v.addEventListener('seeked', () => { v.style.opacity = 1; });    // restaura quando o loop reinicia
```

Prefira A: conserte a emenda na hora da geração (`etna-site-scrub`), não na edição. B (xfade do ffmpeg) grava a
dissolução no arquivo; C (fade em JS) é a opção na página, quando você não pode renderizar de novo e quer que a
dissolução fique com o site.

---

## Tarefa 3: proporções e tamanhos do herói

Heróis saem em algumas formas. Recorte / redimensione a partir da origem em vez de gerar de novo, quando o conteúdo
permitir (uma composição centrada e segura recorta limpo).

```bash
# recorte cinematográfico 21:9 (letterbox) a partir de 16:9 (recorte, não esmague)
ffmpeg -i raw.mp4 -vf "crop=iw:iw*9/21" -an -c:v libx264 -crf 20 -movflags +faststart hero-21x9.mp4

# vertical 9:16 (recorte central de uma origem 16:9 → herói de celular)
ffmpeg -i raw.mp4 -vf "crop=ih*9/16:ih" -an -c:v libx264 -crf 20 -movflags +faststart hero-9x16.mp4

# reduz para uma largura de entrega (ex.: 1920 de largura), mantém a proporção, dimensões pares para h264
ffmpeg -i raw.mp4 -vf "scale=1920:-2" -an -c:v libx264 -crf 20 -movflags +faststart hero-1920.mp4
```

- **`scale=W:-2`**: `-2` mantém a proporção E força uma altura par (o h264 exige dimensões pares).
- **Recorte, não esmague.** Mudar a proporção escalando distorce o sujeito; `crop` mantém a geometria. Para um sujeito fora do centro, acrescente `:x=...:y=...` ao recorte.
- Larguras comuns: `1920` (herói de desktop), `1280` (tablet), `768` (celular). Entregue o tamanho que o layout usa, não um arquivo 4K que o navegador reduz.

---

## Tarefa 4: sequência de imagens para um herói de scrub (rolagem → índice de quadro)

**O herói de scrub sai como sequência numerada de imagens, NÃO como `<video>` embutido.** Um MP4 cru buscado por
`currentTime` a cada tique de rolagem engasga e atrasa no navegador; por isso os builds de referência do mercado
convergiram para rolar quadros. Extraia quadros numerados do(s) clipe(s); a página troca os quadros conforme a posição
da rolagem. Esta é a entrega canônica do scrub; o `<video>` serve só para loops de fundo / clipes de capa que apenas
tocam.

**Extraia quadros numerados** do(s) clipe(s) renderizado(s):

```bash
# um clipe → uma sequência numerada (com zeros à esquerda, ordenada). fps controla o número de quadros.
ffmpeg -i raw.mp4 -vf "fps=30,scale=1920:-2" -q:v 3 frames/%04d.jpg
# → frames/0001.jpg, 0002.jpg, … em ordem estrita. NÃO renomeie: o player indexa pelo número.

# SCRUB COM VÁRIOS CLIPES: junte conforme o MODO, DEPOIS extraia.

# Modo 3 (plano-sequência contínuo, PADRÃO): concatenação simples dos segmentos encadeados.
# Os segmentos já estão encadeados (fim do seg k = início do seg k+1), então as fronteiras são
# continuações sem emenda: NÃO precisa de dissolução, nem xfade, nem corte.
ffmpeg -i seg0.mp4 -i seg1.mp4 -i seg2.mp4 -i seg3.mp4 \
  -filter_complex "[0][1][2][3]concat=n=4:v=1:a=0[v]" \
  -map "[v]" -an mode3.mp4
ffmpeg -i mode3.mp4 -vf "fps=30,scale=1920:-2" -q:v 3 frames/%04d.jpg
# → uma sequência numerada contínua; rolar pela fronteira é uma continuação sem emenda.

# Modo 1 (montagem de corte seco): concatenação de corte seco (os cortes são intencionais: cada corte é uma fronteira de quadro).
ffmpeg -i shot0.mp4 -i shot1.mp4 -i shot2.mp4 -i shot3.mp4 -i shot4.mp4 \
  -filter_complex "[0][1][2][3][4]concat=n=5:v=1:a=0[v]" \
  -map "[v]" -an mode1.mp4
ffmpeg -i mode1.mp4 -vf "fps=30,scale=1920:-2" -q:v 3 frames/%04d.jpg
# → cada corte é uma fronteira nítida de quadro na sequência numerada.

# Modo 2 (plano-sequência simples): clipe único; extraia direto (não há o que juntar).
```

- **Número de quadros = resolução do scrub.** 90 a 180 quadros é um scrub de desktop suave; menos para celular. `fps=N` ou `-frames:v` define isso.
- **Ordem numérica estrita: nunca renomeie.** O player mapeia rolagem → índice; uma reordenação quebra o arco.
- **JPEG, não PNG, para quadros fotográficos**: bem menor; a sequência é a maior carga da página. `-q:v 3` fica visualmente limpo; reduza para a largura do layout.
- **Emita um manifesto** (número de quadros + padrão de caminho) para o site pré-carregar: a sequência tem que ser baixada / decodificada antes de o scrub ficar suave.

**Ligação (posição da rolagem → índice de quadro):**

```js
// N quadros em frames/0001.jpg … ; mapeia o progresso da rolagem sobre o herói para um quadro.
const N = 120, img = document.querySelector('#hero-seq');
function onScroll() {
  const p = Math.min(1, Math.max(0, scrollProgressOverHero()));   // 0..1
  const i = Math.round(p * (N - 1)) + 1;
  img.src = `frames/${String(i).padStart(4, '0')}.jpg`;
}
```

- **Troca de `<img>`**: a mais simples; defina `img.src` a cada quadro da rolagem (pré-carregado, sem piscar).
- **`<canvas>` com `drawImage`**: mais suave para muitos quadros; decodifique uma vez, desenhe o quadro atual.
- **Folha de sprites**: empacote os quadros numa grade e desloque o `background-position`; uma requisição HTTP só, sem busca por quadro (bom para até ~60 quadros).

> **Por que isto e não `<video currentTime>`:** buscar um MP4 a cada tique de rolagem espera os quadros-chave e o átomo
> moov → travamento e atraso visíveis. Uma sequência de imagens decodificadas tem acesso aleatório por índice → exata
> quadro a quadro, sem travar. Esse é o conserto de atraso que o mercado descobriu: MP4 pesado rolado é o antipadrão;
> sequência de imagens é a cura.

## QA antes da entrega

- [ ] **Mudo**: `ffprobe` não mostra fluxo de áudio (`-an` funcionou). O autoplay na web exige isso.
- [ ] **faststart**: moov no início (`ffprobe -v trace ... 2>&1 | grep -n moov` mostra cedo); obrigatório para scrub.
- [ ] **yuv420p**: `ffprobe ... -show_entries stream=pix_fmt` mostra `yuv420p` (reprodução no iOS).
- [ ] **Os dois codecs**: `hero.mp4` (h264) E `hero.webm` (vp9) existem; o webm é menor.
- [ ] **A capa bate com o quadro 1**: `hero-poster.png` é o primeiro quadro do clipe (sem piscada entre capa e play).
- [ ] **Emenda do loop invisível** (só loops): primeiro ≈ último quadro, ou o xfade fecha limpo.
- [ ] **Dimensões pares**: largura e altura pares (o h264 recusa dimensões ímpares).
- [ ] **Sequência do scrub contínua e ordenada** (heróis de scrub): `frames/0001.jpg … NNNN.jpg`, sem buracos, nunca renomeada; um manifesto (número + padrão de caminho) vai junto para a pré-carga.

Checagem rápida:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,pix_fmt,duration \
  -of default=noprint_wrappers=1 hero.mp4
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 hero.mp4   # NÃO pode listar "audio"
```

## Entrega de volta

Via `handoff_submit`: para loops / clipes de capa, os caminhos codificados (`hero.mp4`, `hero.webm`, `hero-poster.png`,
variantes), os tamanhos dos arquivos e o trecho do `<video>`; **para um herói de scrub, a sequência `frames/` (número +
padrão de caminho + manifesto) e o trecho de ligação rolagem → índice de quadro** no lugar do `<video>`. E, num scrub
com vários clipes, anote o MODO e a junção aplicada (Modo 3: concatenação simples dos segmentos encadeados, sem
dissolução; Modo 1: concatenação de corte seco). Sinalize se um clipe de origem não foi autorado para fazer loop e
você precisou de crossfade (renderizar de novo a montante é mais limpo).

## Lacunas de capacidade

- **Sem streaming adaptativo HLS/DASH**: só arquivo único mp4/webm. Uma escada de múltiplas taxas de bits está fora do escopo de um herói.
- **Texto nítido na tela não é codificado aqui**: ele é composto em código (CSS/Remotion) por cima do vídeo mudo; o ffmpeg não conserta tipografia alucinada.
- **O loop com crossfade é plano B, não conserto**: uma emenda que precisa de xfade quer dizer que o clipe não foi autorado para fazer loop; prefira renderizar de novo com movimento cíclico no `etna-site-scrub`.
