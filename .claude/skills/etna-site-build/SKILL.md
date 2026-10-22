---
name: etna-site-build
description: "Use when a squad worker must BUILD the front-end that CONSUMES a scrub hero's image-sequence — the production canvas scroll→frame engine (preload + loading bar, DPR scaling, cover-fit, mobile 1.3×), Lenis Safari-safe smooth scroll + lerp + requestAnimationFrame ticking, the scroll-length(vh)↔N-frames formula, perf hardening (passive/will-change/direct-DOM), mobile consumption fallback, and optional scroll-synced annotation overlays. Consumes frames/ + manifest from the editor; does NOT generate or encode media. Stack pinned Next 16 / React 19 / Tailwind v4 / Framer Motion / Lenis. Bind to the site builder / executor worker that has Bash + file-write. Triggers: front-end build, scroll-driven site, sticky canvas, frame sequence engine, Lenis smooth scroll, scrollytelling site, hero scrub component, image-sequence consumer, Next.js scroll hero."
---

# etna-site-build — Construção do front-end (consome a sequência de imagens)

O worker que constrói o **site** que toca o scrub. O editor (`etna-site-encode`) extraiu `frames/%04d.jpg` + um
manifesto dos clipes renderizados; esta skill escreve o código React/Next que **consome** essa sequência: um
`<canvas>` sticky cujo índice de quadro acompanha a rolagem, com rolagem suave, pré-carga, endurecimento de
desempenho e uma alternativa para celular. **Esta é a última perna do time: briefing → plano → quadros-chave +
movimento → codificação + quadros → site.**

> **Divisão de camadas: você NÃO gera nem codifica.** O `etna-site-scrub` é dono da geração (quadros-chave +
> movimento Kling). O `etna-site-encode` é dono da transcodificação + **extração de quadros** (`frames/` +
> manifesto). Esta skill é dona **só do motor de front-end** que lê esses quadros. Se você se pegar usando
> `etna_imagem_gerar`, `etna_video_gerar` ou ffmpeg, está na skill errada: devolva à etapa anterior. Você consome;
> nunca produz quadros.

---

## O que entra / o que sai

| Entra (do `handoff_submit` do editor) | |
|---|---|
| `frames/%04d.jpg`: a sequência numerada de imagens (o entregável do scrub) | ordem numérica estrita, nunca renomeada |
| `manifest`: número de quadros `N` + padrão de caminho (+ variante mobile opcional) | comanda a pré-carga e o mapa rolagem → índice |
| O trecho de ligação rolagem → índice de quadro | a troca ingênua de `<img>`: você a substitui pelo motor de canvas de produção |

| Sai |
|---|
| O componente React `Hero` (ou `ScrubHero`): canvas sticky, rolagem → quadro, pré-carga + barra de progresso, DPR, cover-fit, 1,3× no celular |
| O `SmoothScrollProvider` (Lenis, seguro no Safari) envolvendo o app |
| A ligação da página (altura da seção em vh, o herói composto na página) |
| Opcional: sobreposições de anotação sincronizadas com a rolagem |

**A estética não é sua.** Paleta, tipografia, sombras, espaçamento, o sistema de design: delegue para
**`frontend-design`** / **`premium-web-design`** (skills do repositório). Esta skill é dona do **mecanismo de
rolagem + desempenho + Lenis**, nunca dos tokens de design. Siga o `design-system.md` do projeto, se existir (regra
global: sistema de design > skill).

---

## A stack (fixada: decisão do projeto, não se desvie)

| Camada | Pacote | Por quê |
|---|---|---|
| Framework | `next` 16 (App Router, RSC) | rota e metadados em componentes de servidor; `"use client"` em tudo que usa hooks |
| UI | `react` 19 | concorrente |
| Estilo | `tailwindcss` v4 | `@import "tailwindcss"` + `@theme inline` (NÃO o `@tailwind` da v3) |
| Revelações | `framer-motion` | revelações e molas de seção: NÃO no caminho quente da rolagem (ali, transições CSS) |
| Rolagem suave | `lenis` | rolagem suave com física, segura no Safari |

> O Next 16 tem mudanças incompatíveis em relação às versões 13/14: seus dados de treinamento podem estar
> defasados. Leia `node_modules/next/dist/docs/` antes de escrever qualquer rota, metadado ou configuração de
> imagem. `"use client"` em todo componente que usa `useEffect`/`useRef`/`useState`/Framer: o erro de hidratação
> nº 1 é esquecer isso.

**O motor é um módulo puro e isolado.** Ponha a matemática de rolagem → quadro (`scrollProgress`, `frameIndex`,
`coverFit`, `lerp`) num `lib/scrubEngine.ts` simples, com **zero imports de React/Next**: testável e portável. O
componente é uma casca fina `"use client"` que liga as referências do DOM às funções puras. O framework é fixo; o
motor não depende de framework.

---

## O motor de canvas de produção (substitui a troca ingênua de `<img>`)

O trecho do editor é `<img>.src = frames/000X.jpg` a cada tique de rolagem: pisca, não tem pré-carga, nem DPR, nem
RAF. Substitua por um motor de `<canvas>`. **Cinco pontos inegociáveis**, todos do build de referência do mercado:

1. **`<canvas>` + `drawImage`, não `<img>.src`.** Decodifique uma vez, desenhe o quadro atual. Cover-fit centralizado
   (`object-fit: cover` feito à mão); no **celular (≤768px) multiplique a largura e a altura do desenho por 1,3**: o
   sujeito aparece maior em telas pequenas.
2. **RAF + referência de tique.** Nunca toque no canvas de forma síncrona no handler de rolagem. Proteja com um RAF
   por vez usando `tickingRef.current`; faça o desenho dentro dele e limpe a flag no fim. Um gesto de rolagem dispara
   30+ eventos por quadro: sem a proteção, eles se acumulam e travam.
3. **DOM direto no caminho quente: zero estado do React por quadro.** Desenho do canvas, opacidade de texto,
   transformações: tudo via referências (`ref.current.style.opacity = …`). O `setState` do React serve SÓ para coisas
   discretas que mudam em limiares (qual cartão de anotação está visível), e só quando o conjunto realmente muda.
4. **Pré-carregue TODOS os quadros + uma barra de progresso real** antes de liberar o scrub. Quadro não carregado =
   canvas em branco = site com cara de quebrado. Dirija um overlay de progresso por `loadedCount / N` (leia `N` do
   manifesto). Espere cada `img.onload` antes de `loaded = true`.
5. **Escala de DPR.** `canvas.width = innerWidth * devicePixelRatio` (resolução interna);
   `canvas.style.width = innerWidth + "px"` (exibição). Pular isso = borrado na tela retina.

```tsx
// ScrubHero.tsx: "use client". A matemática mora em lib/scrubEngine.ts (puro).
const FRAMES = manifest.count;                          // N, vindo do manifesto do editor
const tickingRef = useRef(false), curRef = useRef(0);   // curRef = o índice JÁ SUAVIZADO (lerp)

const onScroll = () => {                                // listener passivo
  if (tickingRef.current) return;
  tickingRef.current = true;
  requestAnimationFrame(() => {
    const target = scrollProgress(sectionRef.current);  // 0..1, puro
    curRef.current += (target * (FRAMES - 1) - curRef.current) * 0.1;  // suaviza o índice
    drawCoverFit(ctx, framesRef.current[Math.round(curRef.current)]);  // DOM direto
    heroTextRef.current.style.opacity = String(Math.max(0, 1 - target / 0.08)); // direto
    tickingRef.current = false;
  });
};
```

```tsx
// a estrutura sticky: a seção em vh dirige a rolagem; o filho fixa na tela
<section ref={sectionRef} style={{ height: "var(--hero-vh)" }} className="scrub">
  <div className="sticky top-0 h-screen"
       style={{ willChange: "transform", transform: "translateZ(0)" }}>
    <canvas ref={canvasRef} className="h-full w-full" />
    {/* sobreposições de anotação, posicionadas em absoluto aqui */}
  </div>
</section>
```

`scrollProgress = clamp(-rect.top / (section.offsetHeight - innerHeight), 0, 1)` → `frameIndex = round(progress * (N-1))`.
**N quadros é a resolução do scrub** (90 a 180 no desktop), então cada fração da rolagem cai num quadro real autorado.

---

## Rolagem suave: Lenis + a suavização do índice (duas suavizações, as duas importam)

São duas suavizações distintas. As duas vão no produto:

1. **O Lenis suaviza a POSIÇÃO da rolagem** (inércia física). Envolva o app num componente cliente
   `SmoothScrollProvider` antes de construir o herói: a matemática do scrub *sente diferente* com Lenis do que com a
   rolagem nativa, então coloque-o primeiro. **Safari/iOS é a armadilha:** os padrões nativos do Lenis engasgam no
   iPhone → suba o `lerp` (≈0,1) e desligue o `syncTouch`. Sem isso, o scrub bonito trava no Safari do celular.
2. **A suavização do índice (lerp) suaviza o NÚMERO do quadro** (a lacuna que o teste só de texto apontou). Não
   cravar `frame = round(progress·(N-1))` direto da rolagem crua: suavize o índice rumo ao alvo a cada RAF:
   `cur += (target - cur) * 0.1; draw(round(cur))`. Elimina o engasgo e o tremor por tique, mesmo quando a rolagem é
   grosseira. Faça o desenho **por RAF**, não por evento de rolagem.

```tsx
// SmoothScrollProvider.tsx: "use client"
<ReactLenis root options={{ lerp: 0.1, syncTouch: false /* seguro no iOS */ }}>{children}</ReactLenis>
```

> O Lenis tem o próprio loop de RAF; deixe o ticking de RAF protegido do scrub correr ao lado dele: não precisa de
> ponte especial, só mantenha o desenho do canvas dentro do próprio RAF protegido.

---

## Dimensionamento: a fórmula altura da rolagem (vh) ↔ N quadros

Os dois números têm que concordar, senão o scrub engasga ou arrasta. O `N` vem do editor (fixado na extração); você
define a **altura da seção** para casar: ou, se você controla a densidade da extração, deriva o `N` de uma altura
escolhida.

- **Distância rolável:** uma seção de `heroVh` sobre uma viewport de `100vh` rola `(heroVh − 100)` alturas de viewport
  → `scrollablePx = (heroVh − 100)/100 × innerHeight`.
- **Ritmo confortável:** cerca de **uma mudança de quadro a cada ~18px** de rolagem (suave, sem degraus, sem
  lentidão). Então:

```
N  ≈  scrollablePx / 18                     # quadros necessários para uma altura dada
heroVh ≈ 100 + (N × 18 / innerHeight) × 100  # altura necessária para um N dado
```

- **Faixa sensata:** **90 a 180 quadros** no desktop. Com innerHeight ≈ 900: `300vh → ~150 quadros`, `400vh → ~200`
  (teto 180), `200vh → ~90`. Os builds de referência do mercado ficam em 106 / 97 / 120: a mesma faixa.
- **Dado o `N` do editor, resolva o `--hero-vh`** e fixe. Alturas responsivas encurtam a rolagem em telas pequenas:
  `400vh → 350vh (≤1024) → 300vh (≤768)`.

---

## Planos ↔ duração: heurística de quantos PLANOS o diretor deve planejar

`S` planos/batidas ⇒ quadros-chave ⇒ clipes Kling ⇒ uma sequência (modo 3: concatenação simples dos segmentos
encadeados, sem fusão; modo 1: concatenação de corte seco; modo 2: clipe único). Cada plano tem 2 quadros-chave
(INÍCIO + FIM), nunca mais. Essa decisão é do diretor / DP, mas o construtor confere o comprimento da rolagem contra
ela:

| Sensação da rolagem (altura da seção) | Número recomendado de planos S |
|---|---|
| Giro de objeto único (uma transformação, ~200 a 250vh) | 1 (INÍCIO + FIM, clipe único) |
| Cena padrão (~300 a 400vh) | 3 a 5 planos |
| Épico / rolagem longa (~500vh+) | 5 a 7 planos |

Mais planos = cena mais rica, mas mais geração (2 quadros-chave + 1 clipe cada). Se o editor entregou `N` quadros
mas a cena é de fato um plano monótono só, a rolagem arrasta (nada muda): sinalize; não tape um arco de um plano só
com uma seção alta. Riqueza vem de mais PLANOS, nunca de mais quadros-chave por plano.

---

## Endurecimento de desempenho (lado do navegador: checklist)

Espelhe as regras do caminho quente do mercado; é isso que separa o suave do travado:

- [ ] **Listeners de rolagem passivos**: `addEventListener("scroll", h, { passive: true })`.
- [ ] **RAF + referência de tique**: um callback enfileirado por quadro (acima).
- [ ] **DOM direto via referências no caminho quente**: canvas / opacidade / transformação nunca passam por `setState`.
- [ ] **`setState` só quando um conjunto discreto muda**: compare os ids dos cartões visíveis por string ordenada; pule se não mudou (limiar ~0,01 em valores tipo opacidade).
- [ ] **Pré-carga + barra de progresso**: todos os `N` quadros decodificados antes de o scrub ficar interativo.
- [ ] **Escala de DPR**: resolução interna ×devicePixelRatio, CSS em px.
- [ ] **`will-change: transform` + `translateZ(0)`** no contêiner sticky / canvas: camada própria na GPU. Não exagere: cada camada promovida custa memória de GPU.
- [ ] **Transições CSS > Framer Motion no caminho quente da rolagem**: cartões de anotação alternam por classes `transition-all`, não por `motion.div` (o loop do Framer pesa quando alterna muitas vezes por segundo). O Framer serve só para revelações de seção que acontecem uma vez.
- [ ] **Build de produção testado**: `next build && next start`; alguns bugs de rolagem só aparecem depois do build.
- [ ] **Lighthouse**: mire 85+ no desktop / 70+ no celular.

---

## Alternativa de consumo para celular

O editor pode entregar um conjunto menor de quadros para o celular; consuma-o:

- **Seções mais baixas**: `350vh` (≤1024) / `300vh` (≤768) via CSS, para o scrub não virar uma rolagem sem fim numa página alta de celular.
- **Zoom de 1,3× no canvas**: o sujeito aparece maior em telas pequenas (em `drawCoverFit`).
- **Menos quadros se o manifesto oferecer uma variante mobile**: pré-carregue o conjunto mais leve (a sequência é a maior carga da página; não mande um conjunto desktop de 180 quadros para um celular). Sem variante mobile, reduza os quadros do desktop para a largura do layout ao decodificar.

---

## Sobreposição de anotação (opcional: narrativa sincronizada com a rolagem)

Legendas / cartões que aparecem em pontos da rolagem sobre o herói (texto legível surgindo conforme você rola). **Todo
texto nítido fica AQUI no código**, nunca na geração (a difusão alucina tipografia; o contrato do scrub mantém as
palavras fora do clipe).

- Cada cartão tem um limiar de `show`/`hide` na rolagem (`{ show: 0.10, hide: 0.30 }`). Só faça `setState` no conjunto
  visível quando ele realmente mudar (compare os ids ordenados); senão você re-renderiza a cada tique.
- Alterne com **transições CSS** (`transition-all duration-400`, `translate-y` + opacidade), não com Framer: é o caminho quente.
- **Máscara de gradiente CSS** para o texto surgir a partir do herói: `mask-image: linear-gradient(to bottom, black 60%, transparent)`. (Esse vocabulário de composição é compartilhado com o `etna-site-scrub`; o construtor o aplica em código.)

---

## Passagem do editor (a fronteira)

O `handoff_submit` do editor traz: o caminho e o padrão de `frames/`, o manifesto (`count` + padrão, + variante mobile
se houver) e o trecho de ligação ingênuo. Você recebe os quadros; NÃO extrai nem recodifica de novo. Se o manifesto
estiver **faltando ou sem `count`**, SINALIZE: nunca chute o número de quadros (um `N` errado dessincroniza o scrub
inteiro). Devolva ao editor para obter o manifesto.

## Entrega de volta

Via `handoff_submit`: o(s) caminho(s) do componente (`ScrubHero.tsx`, `SmoothScrollProvider.tsx`,
`lib/scrubEngine.ts`), o `--hero-vh` que você fixou e o `N` que ele casa, as dependências a instalar (Next 16 / React
19 / Tailwind v4 / framer-motion / lenis) e uma linha sobre o que foi delegado à skill de design (paleta / tipo /
sombras). Anote qualquer tratamento de variante mobile. Informe o comando de desenvolvimento (`next dev`) e, se você
rodou, que o build de produção (`next build && next start`) foi verificado.

## Lacunas de capacidade: sinalize, não finja

- **Nenhuma geração ou codificação de quadros aqui.** `frames/` faltando ou curto, ou um arco fino → devolva à etapa anterior (`etna-site-scrub` / `etna-site-encode`); não sintetize quadros.
- **Sem manifesto → nenhum `N` seguro.** Não chute a contagem: um `N` errado quebra o mapa rolagem → índice. Exija o manifesto.
- **Tokens de design não são seus.** Paleta / tipo / sombra / espaçamento → `frontend-design` / `premium-web-design` / o `design-system.md` do projeto. Esta skill é o motor de rolagem, não a aparência.
- **`<video currentTime>` é o consumidor errado.** Um scrub é uma sequência de imagens ligada a um índice de quadro (este motor), NÃO um MP4 buscado na rolagem (engasga). Loops de fundo e clipes de capa continuam saindo como `<video>`, mas isso não é trabalho desta skill.
