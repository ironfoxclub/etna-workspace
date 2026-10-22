---
name: etna-design-dna
description: "Use quando um worker precisa ENTREGAR um pacote portátil de design system a partir de um site real, capturado AO VIVO por DOM + capturas de tela (não só pelo CSS). Entrega o contrato fiel ao Open Design: DESIGN.md (9 seções fixas), design-contract.md (evidências + manter/mudar/não copiar + portão de qualidade), implementation-handoff.md, tokens em 4 camadas com design-tokens.json + tailwind-v4.css DERIVADOS, components.html + components.manifest.json (seletores COM estados, grupos → referências de tokens, valores soltos), preview/{colors,spacing,typography}.html, assets/ + fonts/ e source/ com a proveniência. TAMBÉM captura o sistema de MOVIMENTO + EFEITOS (`@keyframes` com corpo, transições, blur/vidro/brilho/mistura com valores medidos, gatilhos de revelação, cascata, reduced-motion, canvas/WebGL, animação feita em JS) em source/motion.json + motion.css/motion.manifest.json/motion.js/preview/motion.html DERIVADOS, e DESCOBRE o vocabulário de componentes do próprio site por agrupamento estrutural, sem lista fixa de arquétipos (source/components.discovered.json, com estados de interação reais). Calibrada para landing page web, NÃO para carrossel de Instagram. Gatilhos: design system a partir de site, DNA de design, tokens de design, entrega de design, DESIGN.md, tokens.css, manifesto de componentes, design system por URL, sistema de movimento, DNA de movimento, tokens de animação, escala de easing/duração, keyframes de um site, extrair animações, extração de blur/vidro/brilho, estados de hover e foco, revelação na rolagem, cascata, extrair componentes de um site, inventário de componentes por URL."
---

# etna-design-dna v2: entrega capturada ao vivo, fiel ao Open Design

Você transforma um **site real** num pacote de design system portátil e legível por máquina, que o
construtor seguinte usa sem precisar visitar a origem de novo. **A v2 foi refeita para casar com o
mecanismo real do Open Design (`nexu-io/open-design`)**; veja `design-system/OPEN-DESIGN-REAL-ANALYSIS.md`.

> **v1 → v2, a única mudança que importa.** A v1 era **só CSS**: lia as variáveis de `:root` e
> emitia 5 arquivos chapados. Isso é cego a tudo que vive no pixel renderizado: variantes e estados
> de componentes, composição, recursos, movimento. A v2 captura **DOM + capturas de tela AO VIVO**
> e emite o **contrato completo do Open Design**. Quem faz a captura ao vivo é o agente extrator;
> você EMITE os artefatos a partir dessa evidência. **Sem captura de tela, a entrega está incompleta.**

Você NÃO constrói a página (isso é do construtor). Você EMITE artefatos em `./design-system/`.

---

## A REGRA CONTRA O GENÉRICO (inegociável, herdada da v1)

**Todo token e toda afirmação cita de onde veio, em um de três níveis de confiança** (o modelo do Open Design):

| confiança | significado |
|---|---|
| `observed` | lido do site ao vivo: um valor de `getComputedStyle()`, uma variável CSS, um pixel da captura. O padrão-ouro. Mantenha a verificação por `getComputedStyle` da v1: ela É essa camada. |
| `provided` | fornecido pela pessoa (briefing, documento de marca, recurso enviado). |
| `inferred` | reconstruído ou assumido por você, e declarado como tal. Um `clamp()` refeito a partir de mín/máx é `inferred`. |

Token ou afirmação sem confiança, ou com fonte do tipo "padrão" / "parece certo", é **PROIBIDO**.
Campo sem evidência fica como `"value": "?"`, `"confidence": "inferred"`, registrado em
**riscos/desconhecidos**, nunca inventado. Lacuna honesta vale mais que token fabricado.

---

## Calibração para WEB: descarte a camada de carrossel do Instagram

Você herda o *esquema* do Open Design, NÃO um meio de carrossel. **DESCARTE** tudo que tem formato de
carrossel (`1080×1350`, exportação `3×`, campos `slide-*`, área segura de rede social, receitas de
capa e de ensino). **MANTENHA** o que é nativo da web: tipografia fluida por `clamp(mín, vw, máx)`,
pontos de quebra CSS reais, larguras máximas de contêiner, grades em fr, estados reais de
hover/foco/ativo. Se um valor só faz sentido para uma imagem quadrada de feed, jogue fora.

---

## O contrato de saída: ~12 artefatos em `./design-system/`

| Artefato | Função |
|---|---|
| `DESIGN.md` | Prosa canônica, **9 seções fixas** (abaixo). A fonte da verdade legível por gente. |
| `design-contract.md` | Registro de decisão: tabela de evidências (confiança), manter/mudar/não copiar, posição, **riscos/desconhecidos**, checklist do portão de qualidade. |
| `implementation-handoff.md` | Instruções curtas e operacionais para o construtor ou agente de código. |
| `tokens.css` | Tokens canônicos compilados, **esquema de 4 camadas** (abaixo). |
| `design-tokens.json` | **DERIVADO** de `tokens.css` + `source/token-contract.report.json`. Não escreva à mão. |
| `tailwind-v4.css` | Bloco `@theme` **DERIVADO**. Não pode redefinir valores da origem por conta própria. |
| `components.html` | Peça de teste isolada: toda variante e todo estado de componente, construída só com os tokens. |
| `components.manifest.json` | Inventário de máquina derivado de `components.html`: classes, **seletores incluindo estados**, grupos → `tokenReferences`, `literals`. |
| `preview/colors.html` · `preview/typography.html` · `preview/spacing.html` | Pré-visualizações por dimensão, autossuficientes (zero requisições externas). |
| `source/motion.json` · `screenshots/motion/` | Evidência de movimento ao vivo: corpos de keyframe, tempos por elemento, efeitos, revelações, lacunas de canvas/JS e tiras de quadros. |
| `motion.css` · `motion.manifest.json` · `motion.js` · `preview/motion.html` | Quatro artefatos de movimento **DERIVADOS**; obrigatórios quando `source/motion.json` existe. |
| `assets/` | Logo e imagens extraídos (as marcas observadas). |
| `fonts/` | Arquivos de webfont quando uma fonte personalizada é necessária (senão o `@font-face` é documentado, não empacotado). |
| `source/evidence.md` · `source/tokens.source.json` · `source/token-contract.report.json` · `source/scanned-files.json` | Proveniência: escopo da captura, tokens brutos observados, mapa token → linha do `tokens.css`, lista de capturas e arquivos. |
| `screenshots/` | A captura ao vivo (hero, página inteira, celular, por componente, por estado). Fornecida pelo extrator e citada por todo artefato. |
| `source/motion.json` | **Passagem de movimento.** Contrato bruto de movimento e efeitos: `@keyframes` COM CORPO, transições por elemento, efeitos de superfície (`backdrop-filter`/`filter`/brilho/mistura) com valores medidos, gatilhos de revelação, passo da cascata, contagem de regras `prefers-reduced-motion`, contextos canvas/WebGL, chamadas interceptadas de `Element.animate`, tiras de quadros. |
| `motion.css` · `motion.manifest.json` · `motion.js` · `preview/motion.html` | **DERIVADOS** de `source/motion.json`. O kit reproduzível: tokens + corpos de keyframe, inventário de máquina, o executor de revelação (limiar e cascata medidos + proteção de reduced-motion) e uma pré-visualização com controle deslizante. |
| `source/components.discovered.json` | **Passagem de componentes.** O vocabulário PRÓPRIO do site, achado por agrupamento estrutural em vez de lista fixa de arquétipos: por componente, o seletor, a assinatura, o número de instâncias, as variantes, os estados de interação reais com a diferença de propriedades e uma captura. |

---

## 1. `DESIGN.md`: as nove seções fixas

Use estes títulos **exatamente**, nesta ordem (em inglês, porque o linter confere o texto):

```
## 1. Visual Theme & Atmosphere
## 2. Color
## 3. Typography
## 4. Spacing & Grid
## 5. Layout & Composition
## 6. Components
## 7. Motion & Interaction
## 8. Voice & Brand
## 9. Anti-patterns
```

Cada seção é prosa concreta, apoiada em evidência observada (cite capturas e valores calculados).
A §1 abre com um parágrafo de "parece com…" + uma lista **Key Characteristics**. A §2 nomeia as
cores com papel + hex + a variável CSS observada + uma subseção **Gradient System** (o
`linear-gradient(...)` literal, quando existir). A §5 registra a composição real (por exemplo,
"maquete como hero ocupa os ~60% inferiores", "grade de 3 colunas com divisores verticais finos"),
a camada que o CSS sozinho perdia. A §6 lista cada componente com suas variantes e os estados que
ele entrega. A §9 traz coisas exatas a evitar, não frases vagas.

---

## 2. `design-contract.md`: registro de decisão

Blocos obrigatórios (espelham o `reference-design-contract` do Open Design):

- **Goal & target**: qual superfície, qual público.
- **Tabela de evidências**: `| evidência | confiança | nota |` com `observed` / `provided` / `inferred`.
- **Tabela Manter / Mudar / Não copiar**: uma linha por referência. `Manter` = qualidades controláveis (densidade, ritmo tipográfico, temperatura de cor, atitude de movimento). `Não copiar` = capturas literais, logos, afirmações, interface proprietária.
- **Posição**: uma direção visual coerente, em um parágrafo (não 5 moodboards).
- **Riscos e desconhecidos**: todo campo `?` nomeado aqui. (É o "o que NÃO foi observado" honesto da v1, promovido.)
- **Checklist do portão de qualidade**: os portões P0 (veja a seção do Portão).

---

## 3. `implementation-handoff.md`: operacional

Curto o bastante para colar na próxima execução: arquivos a ler, restrições obrigatórias de
token/paleta/tipo/layout, regras de recursos, requisitos de responsivo e uma nota de aceite "o
primeiro artefato deve provar…".

---

## 4. Tokens: o esquema de 4 camadas (substitui a lista chapada da v1)

`tokens.css` declara os tokens por camada (do `_schema` do Open Design):

| Camada | Quem decide / se omitida | Exemplos |
|---|---|---|
| **A1-identity** | a marca decide; **obrigatória** | `--bg`, `--fg`, `--accent`, `--font-display` |
| **A1-structure** | a marca decide; **obrigatória** | escala de tipo (`--text-sm…--text-4xl`), `--container-max`, `--section-y-*` |
| **A2 (reserva)** | a marca, com uma reserva sensata | `--motion-fast`, `--success`, `--space-4`, `--font-mono` |
| **B-slot** | a marca ou um apelido do esquema (`aliasTo`) | `--fg-2: var(--fg)` (recolhido) ou valor independente (mais rico) |
| **C-extensions** | específicos da marca, em lista permitida | `--tag-bg-*`, tokens pontuais da marca |

Regras: todo token A2 / B-slot é **declarado** em `:root` (os artefatos colam o `:root` de uma marca
num único `<style>`, então uma variável faltando quebra em silêncio). O B-slot usa `aliasTo` quando
a marca não tem opinião mais rica. `design-tokens.json` e `tailwind-v4.css` são **derivados** de
`tokens.css` + `source/token-contract.report.json`: nunca editados à mão, nunca redefinindo valores
da origem.

`source/token-contract.report.json` mapeia **cada token → a linha do `tokens.css`** onde ele é
declarado, cada um com `confidence`. É aqui que o rigor do `getComputedStyle` da v1 pousa.

---

## 5. Componentes: `components.html` + `components.manifest.json` (o ponto cego da v1)

`components.html` é uma peça de teste de verdade que renderiza **todo componente, toda variante,
todo estado**, construída só com os tokens (sem valor fixo no código: o manifesto conta as violações).

`components.manifest.json` é derivado dela e traz:

- `classes`: toda classe de componente (`btn`, `btn-primary`, `btn-secondary`, `btn-icon`, `badge`, `field`, `field-error`, `tab`…).
- `selectors`: **incluindo seletores de estado**: `.btn-primary:hover`, `.btn-primary:active`, `.btn:focus-visible`, `.field input:focus-visible`, `.tab[aria-selected="true"]`, `a:hover`, `a:focus-visible`.
- `groups`: `{id, label, selectors[], classes[], elements[], tokenReferences[]}`; cada grupo de componente lista os tokens que consome.
- `literals`: `{colorExpressions, pixelValues, hardcodedFontFamilies}`: uma **contagem de valores fixos** que deveriam ser tokens. Leve isso a zero.

Ler variante ou estado só do `:root` é proibido: foi esse o bug que fez a v1 chamar o botão
secundário de "primário, menor" quando o verdadeiro era uma pílula escura fantasma. **Variantes e
estados vêm da peça renderizada e das capturas, não das variáveis CSS.**

---

## 6. Disciplina e Portão (acabamento + linter)

Trate as regras `craft/` do Open Design como obrigatórias:

- **Cobertura de estados** (`craft/state-coverage.md`): toda superfície que busca, transforma ou aceita dados renderiza **5 estados**: Loading · Empty · Error · Populated · Edge. Formulários somam **3**: Untouched · Dirty-valid · Submitted-pending. O teste é renderizar e capturar cada um. Estado faltando é a falha silenciosa nº 1 de interface feita por IA.
- **Anti-lixo-de-IA P0** (`craft/anti-ai-slop.md`): **bloqueie em P0** (1) acento = índigo padrão do Tailwind, exatamente `#6366f1`/`#4f46e5`/`#4338ca`/`#3730a3`/`#8b5cf6`/`#7c3aed`/`#a855f7`; (2) gradiente de "confiança" de dois tons no hero (roxo→azul, azul→ciano, índigo→rosa). Use o `--accent` observado; uma superfície chapada com tipografia intencional vence o gradiente.
- Puxe também `craft/color`, `craft/typography`, `craft/accessibility-baseline` e `craft/animation-discipline` como fonte de disciplina.

### Portão P0: precisa passar antes da entrega

**Rode o linter determinístico: ele transforma este portão de promessa em código de saída 0/1:**

```bash
node scripts/lint-artifact.mjs ./design-system
```

Ele lê `rules/anti-ai-slop.json` + `rules/contract.json` e valida a pasta. **Saída ≠ 0 = REJEITAR;
você NÃO pode dar `handoff_submit` com `status:"done"`.** O linter impõe as mesmas checagens abaixo
(arquivos obrigatórios, sem acento índigo, sem gradiente de confiança, todo token com fonte e
confiança como P0; seletores de estado + estados 5+3 + coerência dos derivados + camadas de token
como P1). A lista numerada é o espelho legível do que o script confere:

1. **Existem capturas de tela** e cobrem hero + página inteira + celular + cada componente-chave + cada estado. Sem evidência em captura → incompleto.
2. **`DESIGN.md`** usa exatamente os 9 títulos.
3. **`design-contract.md`** tem a tabela de evidências + manter/mudar/não copiar + riscos + portão de qualidade.
4. **Todo token carrega `confidence`**; `tokens.css` ↔ `design-tokens.json` ↔ `token-contract.report.json` em sincronia; arquivos derivados não editados à mão.
5. **`components.manifest.json`** lista os seletores de estado e os estados 5+3 estão em `components.html`.
6. **Anti-lixo P0 limpo**: sem acento índigo padrão, sem gradiente de confiança no hero.
7. **As pré-visualizações renderizam** com zero requisições externas; hexes, tamanhos e réguas reais à mostra.
8. **O portão de movimento é condicional:** se `source/motion.json` existe, rode a passagem de movimento abaixo. Pastas antigas sem ele mantêm as checagens e o comportamento de saída anteriores.

### Passagem de movimento: capturar, derivar, provar

Rode a partir desta pasta da skill, com Playwright e Chrome instalados:

```bash
node scripts/harvest-motion.mjs <url-do-site> ./design-system
node scripts/gen-motion.mjs ./design-system
node scripts/verify-motion.mjs ./design-system
node scripts/lint-artifact.mjs ./design-system
```

Capture o movimento **antes de a passagem estática congelar as animações**. O `harvest-motion.mjs`
roda separado do `harvest.mjs`; ele recorre ao Chrome com janela quando a captura sem janela esbarra
num muro anti-robô. Confira `source.captureMode` e `risks`. `--no-strips` omite a evidência em
tiras de quadros, então use o padrão para entregar.

O `gen-motion.mjs` lê só `source/motion.json` e os PNGs capturados. Ele emite:

- `motion.css`: tokens de duração/easing/atraso/efeito e todo **corpo** de `@keyframes` capturado.
- `motion.manifest.json`: proveniência, propriedades, tempos, efeitos, revelações/cascata, lacunas fora do CSS e fixtures de `preview` explicitamente marcados `inferred`.
- `motion.js`: executor de revelação com o limiar e a cascata de gatilho capturados e a proteção de reduced-motion.
- `preview/motion.html`: diagnóstico isolado com keyframes embutidos, tempos observados por animação quando existem, reproduzir/pausar/deslizar, substituições opcionais de tempo e quadros de componentes capturados embutidos. Instâncias em execução que faltam usam tempo rotulado `inferred`. A reprodução repetida, as superfícies de teste e os valores padrão das propriedades personalizadas também são `inferred`; os deslocamentos capturados ficam intactos, inclusive em keyframes de um único deslocamento.

Os diagnósticos de movimento provam a execução do CSS; **não são uma biblioteca de componentes nem
uma reconstrução da coreografia em JavaScript/canvas.** Entregue fixtures reais de componentes junto
quando a tarefa pedir componentes. Um valor de blur numa tabela não substitui o componente de
vidro em contexto.

O `verify-motion.mjs` abre o Chromium com janela e salva `source/motion-preview-proof/report.json`
mais PNGs em pares. Para **cada** amostra ele confere `getAnimations()`, reprodução automática,
reproduzir/pausar/deslizar, mudanças calculadas de propriedade e hashes de PNG diferentes em 0%/50%
do palco fixo. Confere também a simulação de reduced-motion e zero requisições externas. Se os
quadros coincidem, inspecione a propriedade, a variável ausente ou a superfície de teste; nunca
reescreva o movimento observado só para passar na checagem de imagem. Declare a lacuna não
resolvida antes de entregar.

Quando há evidência de movimento, o linter soma as checagens P0 `motion-capture-reached-site`,
`motion-derived-files`, `motion-keyframe-bodies` e `motion-no-placeholder-effects`. A prova em
tiras de quadros e a reprodutibilidade fora do CSS são checagens P1. Rode na **pasta completa do
design system**, não só numa pasta de captura de movimento. Nunca acrescente arquivos de movimento
ao contrato antigo incondicional.

---

## 7. As duas passagens ao vivo: movimento e componentes

O `harvest.mjs` é a passagem estática e é cego de propósito em dois pontos. Estas passagens são
**aditivas**: nada do caminho estático é renomeado, removido ou precisa mudar.

### `scripts/harvest-motion.mjs <url> <outdir>`: movimento e efeitos

A passagem estática CONGELA a página para fotografar um estado assentado (`harvest.mjs:209-215`
injeta `animation-duration:0s`, `transition:none` e força a exibição de `[class*="reveal"]`/`[data-aos]`).
Isso está certo para uma captura e estruturalmente cego ao movimento: apaga justamente o sistema que
deveria medir e depois relata 6 tokens com valores reserva fixos. Esta passagem roda ANTES de
qualquer congelamento e mede o que o congelamento destrói:

- **Corpos de keyframe**, não nomes. Uma entrega que diz `tilePopIn` e mais nada não diz nada ao construtor. Leia por `CSSKeyframesRule`; uma folha de outra origem lança erro em `.cssRules`, então o href dela é buscado de novo por HTTP e interpretado, em vez de descartado.
- **Ganchos instalados antes de qualquer script do site**: `HTMLCanvasElement.getContext` (quais contextos o site pediu, sem alterarmos o estado do canvas), `IntersectionObserver` (o limiar e o rootMargin REAIS da revelação) e `Element.animate` (movimento feito em JS, Framer/GSAP, que não existe no CSS).
- **Efeitos de superfície com valores medidos**: `backdrop-filter`, `filter`, sombras de brilho, misturas, gradientes animados, máscara/recorte. Efeito registrado como `[?]` é defeito, não lacuna.
- **Tiras de quadros**: cada animação é reiniciada, pausada e tem o `currentTime` fixado em t=0/.25/.5/.75/1, com captura de cada ponto. Os quadros recebem hash; quadros idênticos significam que o deslize não moveu nada e a tira é relatada como não comprovada.
- **Proteção contra muro anti-robô**: escala de `stealth-headless → Chrome com janela` e ABORTA em vez de emitir. Captura de uma tela intersticial da Cloudflare produz um design system inteiro da página de bloqueio com cada valor carimbado `observed`; falha honesta vale mais que lixo confiante.

Depois o `scripts/gen-motion.mjs <dir>` deriva o kit. O `preview/motion.html` precisa embutir os
corpos dos keyframes: ele não faz nenhuma requisição externa, então sem eles cada `animation-name`
aponta para o nada e a pré-visualização renderiza uma grade de amostras congeladas. Uma propriedade
personalizada (`--angle`) precisa de `@property` registrada ou é um texto, e texto não interpola.

### `scripts/harvest-components.mjs <url> <outdir>`: o vocabulário próprio do site

A passagem estática procura sete arquétipos que já conhece, com limite (6 botões, 4 cards, 1
navegação, 1 campo, 1 rodapé) e deduplica por `backgroundColor|borderRadius|boxShadow`; assim, duas
coisas estruturalmente diferentes com o mesmo fundo e raio viram uma entrada só, e uma transcrição
de chat, uma barra de gravação ou um cursor de agente ficam inalcançáveis por construção. Esta
passagem faz a pergunta oposta: **não "onde estão os botões", mas "o que este site repete"**:

- Agrupa por `tag + classes semânticas + esqueleto de tags filhas`, depois de remover hashes de CSS-module e utilitários do Tailwind. Utilitários de uma palavra também contam como ruído: deixá-los fez `truncate` e `underline` virarem os dois "componentes" principais de um site.
- **Os estados são sondados por interação real e só ficam se algo mudou.** Três armadilhas, todas produzem um artefato mentiroso: (1) comparar só o elemento sob o mouse perde componentes compostos em que o contêiner é inerte e o FILHO se move, então a captura cobre a subárvore e a diferença nomeia o nó; (2) ser interativo não prevê ter estado: um `li` sem `cursor:pointer` e sem foco ainda pode animar os filhos no hover, então sonde mais amplo, interativos primeiro; (3) um elemento animado gera estados FANTASMA, porque amostrar `opacity: 0.966 → 1` duas vezes é a animação assentando, não um hover. Por isso a linha de base é medida duas vezes e tudo que deriva sozinho é desqualificado de toda comparação posterior.
- `focusable` (o próprio) e `insideInteractive` (um ancestral) são campos separados: o `closest()` fazia todo `<span>` dentro de um botão alegar que recebe foco do teclado.

Medido em `x.ai/bot`: 93 grupos nomeados e 30 estruturas repetidas contra o teto antigo de 13.

## Processo

1. **Captura ao vivo** (agente extrator, via Playwright): rode o `harvest-motion.mjs` antes de congelar as animações, depois capture DOM + capturas de tela (página e elemento) + extraia logo/fontes/cores/imagens/OG/acessibilidade. As evidências caem em `screenshots/` + `source/`.
   - **1b. Passagem de movimento**: `node scripts/harvest-motion.mjs <url> <dir>` e depois `node scripts/gen-motion.mjs <dir>`. Rode ANTES de confiar na §7 do `DESIGN.md`: sem ela, essa seção é prosa sem contrapartida legível por máquina (veja a §7 desta skill).
   - **1c. Passagem de componentes**: `node scripts/harvest-components.mjs <url> <dir>`. Rode antes de escrever a §6 do `DESIGN.md`, para que a lista de componentes seja o vocabulário do site e não os arquétipos que você sabia procurar.
2. **Trave a direção**: separe as referências em Manter / Mudar / Não copiar; escolha uma posição.
3. **Organize os tokens** nas 4 camadas; marque cada um com `confidence`; registre as lacunas `?` em riscos.
4. **Remova a camada de Instagram**; converta tamanhos fixos para `clamp()` web + pontos de quebra.
5. **Emita** os artefatos; derive `design-tokens.json` + `tailwind-v4.css` de `tokens.css` + relatório; rode `gen-motion.mjs` quando houver evidência de movimento.
6. **Portão**: rode o checklist P0. Depois `handoff_submit` com todos os caminhos dos artefatos + o resultado do portão.

---

## Vícios a rejeitar (antes de emitir)

- **Extração só de CSS**: emitir tokens sem evidência em captura. Esse era o bug da v1. Capture o pixel.
- **Emitir qualquer coisa a partir de um muro anti-robô.** Se a captura caiu numa tela intersticial da Cloudflare, ABORTE. Um design system de uma página de bloqueio não é resultado parcial, é fabricação com carimbo `observed`.
- **Nome de keyframe sem corpo** (`tilePopIn`, `gridShimmerH`). Nomear uma animação não é especificá-la.
- **Efeito escrito como `[?]`**: um blur que foi visto e nunca medido. Leia o valor calculado ou registre em riscos; nunca afirme e se esquive ao mesmo tempo.
- **Prosa no lugar de pré-visualização.** Cor, tipo e espaçamento entregam cada um uma pré-visualização; movimento entregando só um parágrafo é o defeito antigo. Se `source/motion.json` existe e `preview/motion.html` não, o portão falha.
- **Declarar um estado que não muda nada**: um hover fantasma colhido de um elemento que apenas estava no meio de uma animação. Meça a linha de base duas vezes e desqualifique a deriva própria.
- **Relatar os arquétipos que você foi procurar** em vez do vocabulário que o site realmente repete.
- Inferir variante ou estado de componente a partir do `:root` em vez da peça renderizada.
- Token sem `confidence`, ou `design-tokens.json` / `tailwind-v4.css` editado à mão que se afasta do `tokens.css`.
- Índigo padrão do Tailwind como acento; gradiente de confiança de dois tons no hero (ambos P0).
- Entregar só o estado Populated, sem Loading/Empty/Error/Edge.
- Tokens de carrossel/slide (`slide-title`, `safe-area`, `1080×1350`) vazando para um sistema web.
- Uma pré-visualização que puxa fonte ou CDN remoto: ela precisa ser autossuficiente.
- Copiar o hex, a família ou o nome literais de uma marca de exemplo: o formato é o exemplo, o conteúdo é o site capturado da pessoa.
