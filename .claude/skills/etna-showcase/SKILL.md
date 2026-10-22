---
name: etna-showcase
description: "Regras de UI/UX para construir, revisar ou consertar interfaces de produto: acessibilidade e toque primeiro, depois desempenho, layout, tipografia e cor, movimento, coerência de estilo e gráficos, com checklist antes da entrega. O design system do projeto sempre vale mais que estes padrões. Use ao desenhar, construir, revisar ou consertar qualquer tela, componente, página ou painel."
---

# etna-showcase: interface profissional por regra, não por gosto

Regras em ordem de prioridade que separam uma interface profissional de um modelo pronto. **Regra
dura: quando o projeto tem design system (tokens, componentes, documento de marca), ele vale mais
que qualquer coisa daqui.** Leia-o primeiro (`docs/design-system/`, a folha de estilo global, duas
ou três telas vizinhas) e preencha só as lacunas com estes padrões. Interface de produto (painéis,
admin, SaaS, configurações, dados densos) → seção **Interface de produto** abaixo (antiga
`etna-app-ui`, absorvida aqui); páginas de marketing e de captura → `etna-site-premium`; entrega
portátil de design system capturada de um site no ar → `etna-design-dna`.

## Fluxo

1. **Leia o pedido**: tipo de produto (SaaS, painel, página de captura, celular...), setor, palavras de estilo, stack (padrão: a do projeto; senão HTML + Tailwind).
2. **Leia o projeto**: tokens, componentes existentes, escalas de espaçamento e de tipo, tratamento de claro/escuro. Reaproveite antes de inventar.
3. **Decida o sistema para o que falta**: estilo, paleta (um acento sobre base neutra), par de fontes (as personalidades de título e corpo combinam), escala de espaçamento, elevação, orçamento de movimento. Escreva antes de codar.
4. **Construa** pelas regras abaixo, **revise** com o checklist e **conserte** o que falhar.

## Regras por prioridade

1. **Acessibilidade (crítica)**: contraste do texto ≥ 4,5:1 (3:1 para texto grande); anéis de foco visíveis; texto alternativo em imagem que tem significado; `aria-label` em botão só de ícone; ordem do Tab = ordem visual; todo campo tem rótulo; a cor nunca é o único sinal.
2. **Toque e interação (crítica)**: alvos ≥ 44×44 px; ação principal por clique ou toque, nunca só no hover; botão desabilitado com indicador de carregamento durante trabalho assíncrono; erro ao lado do campo, em palavras; `cursor: pointer` em tudo que é clicável; retorno no hover que não desloca o layout.
3. **Desempenho (alta)**: WebP/AVIF, `srcset`, carregamento preguiçoso abaixo da dobra; respeitar `prefers-reduced-motion`; reservar espaço para conteúdo assíncrono (sem saltos de layout); esqueletos em vez de indicadores giratórios nas áreas de conteúdo.
4. **Layout e responsivo (alta)**: meta viewport; corpo ≥ 16 px no celular; sem rolagem horizontal; uma largura de contêiner; conteúdo nunca escondido atrás de barra fixa; escala de z-index (10 / 20 / 30 / 50), sem números mágicos; conferir 375, 768, 1024 e 1440.
5. **Tipografia e cor (média)**: altura de linha de 1,5 a 1,75 no corpo; de 65 a 75 caracteres por linha; no máximo duas famílias; texto atenuado ainda legível (slate-600, não gray-400); bordas visíveis nos dois modos; superfícies de vidro com opacidade ≥ 80 % no modo claro.
6. **Movimento (média)**: de 150 a 300 ms em microinterações; animar `transform` e `opacity`, não largura nem altura; todo estado de carregamento e de vazio desenhado.
7. **Estilo (média)**: um estilo só em todas as páginas; o estilo combina com o produto (fintech não é app infantil); ícones SVG de um único conjunto (Lucide, Heroicons) com viewBox e tamanho fixos, **nunca emoji como ícone**; logos de marca corretos, do SVG oficial.
8. **Gráficos e dados (baixa)**: o tipo do gráfico combina com o dado (tendência → linha, comparação → barra, parte do todo → poucas fatias); paletas acessíveis; alternativa em tabela para leitores de tela.

## Vícios que parecem amadorismo

Ícones de emoji · escala no hover que desloca o layout · vidro `bg-white/10` no modo claro · texto
de corpo em gray-400 · bordas invisíveis · larguras de contêiner misturadas · barra de navegação
colada em `top-0` sem respiro · transições instantâneas ou acima de 500 ms · anel de foco do
navegador removido sem substituto.

## Interface de produto: painéis, admin, SaaS, dados densos (antiga `etna-app-ui`)

O inimigo é o padrão estatístico: todo modelo já viu milhares de painéis e escorrega para o centro
da distribuição, uma fonte simpática numa grade genérica, uma paleta quente sobre estrutura fria.
**Teste de falha:** se outro agente, recebendo um pedido parecido, chegaria à mesma tela, você caiu
no padrão. O design nasce DESTE produto, DESTA pessoa, DESTA tarefa. (Páginas de captura e
marketing não são esta seção → `etna-site-premium`.)

1. **Intenção antes do código**: um briefing curto, não um ensaio. *Quem* é essa pessoa de verdade (onde está, o que fez cinco minutos antes, o que faz cinco minutos depois); *qual verbo* ela precisa completar (aprovar um pagamento, achar o deploy quebrado, corrigir uma prova); *que sensação* a tela carrega, em palavras que significam algo ("denso como um pregão", "calmo como um leitor", "frio como um terminal"; "limpo e moderno" não diz nada). Se o pedido não responde às três, faça UMA pergunta objetiva; se dá para supor com responsabilidade, suponha e declare. A intenção é sistêmica: "denso" significa espaçamento, tipografia e arquitetura de informação densos, não só a paleta. Escolha justificada com "é comum" ou "funciona" é um padrão disfarçado.
2. **Explore o domínio do produto** antes de qualquer decisão visual, e produza quatro coisas: ≥ 5 conceitos do domínio (vocabulário e metáforas daquele mundo, território, não funções); ≥ 5 cores que existem na versão física daquele espaço; uma **assinatura**, elemento visual, estrutural ou de interação que só poderia existir NESTE produto (sem candidata → continue explorando); três escolhas óbvias para este tipo de tela que você rejeita, cada uma com a substituta. Teste: tire o nome do produto da sua proposta; um leitor ainda adivinha o que é?
3. **Hierarquia e composição**: um foco por tela, dito em voz alta antes de construir e feito vencer por tamanho, contraste ou espaço em volta, com o resto rebaixado de propósito; escala tipográfica por razão (≈1,2 para interface densa ou calma, 1,25 para a maioria dos produtos, 1,333 para algo expressivo) a partir de uma base de 14 a 16 px, de modo que os degraus sejam visivelmente distintos; peso e cor carregam mais hierarquia que tamanho (um único corpo de 14 px sustenta três camadas: valor 600/primário · rótulo 500/secundário · meta 400/atenuado; use tamanho, peso e cor juntos, nunca só tamanho); densidade é uma escolha expressa em px (12 a 16 px de preenchimento lê como bancada de trabalho, 24 px como folheto) e o valor escolhido se repete em todo lugar; ritmo espacial desigual: zona densa de controles cede a conteúdo aberto, o que é relacionado fica junto, com ar de verdade entre grupos (mesmo card e mesmo vão em todo lugar é o som de ninguém ter decidido); proporção diz algo (barra lateral de 280 px serve ao conteúdo, de 360 px os torna pares; se você não sabe dizer o que uma proporção diz, ela não diz nada); ≈60/30/10 neutro/secundário/acento, estrutura por espaço e peso ANTES de linhas e bordas, espaçamento entre letras mais justo em títulos grandes, altura de linha ≈1,5 no corpo.
4. **Camadas e superfícies**: escala de elevação numerada com alguns % de luminância por degrau (dropdown > card > página: cada degrau quase imperceptível sozinho, empilhados revelam a hierarquia); barra lateral com o mesmo fundo do canvas e uma borda sutil, nunca cor diferente (isso separa o "mundo da barra" do "mundo do conteúdo"); dropdown ou popover um nível acima do pai; campo de entrada levemente MAIS ESCURO que o entorno (ele recebe conteúdo, é rebaixado); bordas em `rgba` de baixa opacidade (o modo escuro vive em torno de `rgba(255,255,255,0.06–0.12)`), hex sólido parece duro ao lado delas. **Teste de apertar os olhos:** desfoque a vista; a hierarquia deve continuar lá e nada deve saltar. Todo padrão tem infinitas expressões: uma métrica pode ser um número herói, uma estatística em linha, um minigráfico, um medidor, uma variação comparativa; a mesma barra lateral + grade + card ícone-número-rótulo em todo projeto é o sinal mais óbvio de IA. A cor vem de algum lugar: visite a versão física daquele espaço (materiais, luz, objetos) antes de escolher a paleta, para que ela pareça ter VINDO de lá em vez de aplicada por cima.
5. **Use o que existe**: o jeito mais rápido de degradar um código é reinventá-lo (`<div onClick>` ao lado do `Button` de verdade do projeto, um dropdown sem teclado ao lado de uma primitiva instalada que já resolve isso). Controles, nesta ordem: HTML nativo onde funciona (`<button>`, `<a>`, `<dialog>`, `<details>`) → primitiva testada em batalha para o que tem estado e é difícil de acertar (select, combobox, diálogo, tooltip, abas, seletor de data; Radix, React Aria, Ark e Headless UI já resolvem teclado, foco, ARIA e posicionamento) → feito à mão só como último recurso real, devendo o contrato completo (navegação por teclado, prisão e devolução de foco, ARIA, clique fora, trava de rolagem). Estilo, nesta ordem: o design system (`<Button variant="…">`) → um componente ou variante para o que se repete duas vezes → tokens semânticos (`bg-card text-muted-foreground`, nunca hex cru nem gray-N, que quebram tema e modo escuro) → utilitário em linha só para um ajuste de layout realmente único.
6. **Essenciais do sistema**: tokens de cor rastreados até um punhado de primitivas (primeiro plano, fundo, borda, marca, semânticas destrutiva/aviso/sucesso), zero hex solto; quatro níveis de texto (primário / secundário / terciário / atenuado; dois é chato); unidade de espaçamento de 4 ou 8 px, só múltiplos, escalada por contexto (micro / componente / seção / área); UMA estratégia de profundidade, mantida (só borda: técnico e denso · sombra sutil: acolhedor · sombra em camadas: premium · variação de superfície: sem sombra), nunca misturadas; raio em escala (pequeno em campo e botão, médio em card, grande em modal); tokens próprios para controles (campo, select e checkbox não reaproveitam o token genérico de superfície); o modo escuro se apoia em bordas (a sombra é fraca no escuro), dessatura as cores semânticas, mantém a mesma hierarquia com valores invertidos, um matiz variando só em luminância.
7. **Acabamento e movimento**: raio concêntrico (`externo = interno + preenchimento`; o mesmo raio no pai e no filho é o erro "quase certo" mais comum); preenchimento simétrico, a menos que o conteúdo peça outra coisa; `font-variant-numeric: tabular-nums` em todo número dinâmico (contador, preço, coluna de tabela); alinhamento óptico corrigido a olho (≈2 px a menos de preenchimento do lado do ícone que do lado do texto); todo elemento interativo tem padrão/hover/ativo/foco/desabilitado e toda visão de dados tem carregando/vazio/erro (estado faltando é o sinal mais rápido de tela inacabada); sombra em vez de borda para elevação em card ou botão que "levanta"; `:active` com `transform: scale(0.97)` (nunca abaixo de 0,95) como confirmação tátil; movimento é sentido, não assistido (ação repetida mais de 100 vezes por dia, como atalho ou paleta de comandos, NÃO anima; superfície ocasional, como modal, gaveta ou aviso, anima); < 300 ms, ease-out personalizado nunca ease-in, só `transform`/`opacity` (GPU), nunca `transition: all`, nunca partindo de `scale(0)` (comece em `scale(0.95) + opacity: 0`), popovers crescem a partir do gatilho, modais ficam centralizados, entradas de lista em cascata de 30 a 80 ms, `prefers-reduced-motion` respeitado.
8. **Ponto de controle antes de cada componente**, mesmo pequeno: escreva uma linha para cada um. Intenção (pessoa, verbo, sensação) · hierarquia (o elemento em foco e como ele vence) · paleta (cores da exploração do domínio, e por quê) · profundidade (borda / sombra sutil / camadas, e por quê) · superfícies (escala de elevação, e por que essa temperatura) · tipografia (família + alavancas de tamanho/peso/cor, e por quê) · espaçamento (unidade base + densidade escolhida). Linha sem um *porquê* é padrão: pare e decida de novo.

**Evite:** borda dura como primeira coisa que o olho pega · salto dramático de elevação · hierarquia chapada sem foco definido · o mesmo card e o mesmo vão em todo lugar · espaçamento fora da grade · estratégias de profundidade misturadas · estado faltando · raio grande em elemento pequeno, borda decorativa grossa · gradiente decorativo ou cor sem significado, vários acentos · fonte do sistema ou Inter genérica quando uma direção foi declarada · gambiarras estruturais (margem negativa desfazendo o preenchimento do pai, escapes com `calc()`, `position: absolute` para fugir do fluxo).

**Regras de trabalho:** inspecione o app, os tokens e os padrões existentes antes de propor algo novo; explore o domínio (as quatro saídas) antes de decidir layout, cor, tipo ou densidade; construa e rode a checagem de tipos/build quando houver; verifique visualmente a interface não trivial, com foto do texto/DOM ANTES da captura de tela (pirâmide de QA: sempre sem janela, pixels só no veredito final), conferindo sobreposição, espaçamento quebrado, estado vazio e texto ilegível; no máximo três tentativas na mesma abordagem para um problema visual ou técnico, e na terceira falha mude a abordagem ou relate a lacuna, nunca tente a variação dez; uma referência visual, quando precisar, é gerada com `etna_imagem_gerar` (mídia própria, nunca banco de imagens nem link externo); bug de interface achado numa auditoria (que não é a tarefa atual) vai para `TASK/items/F-XXX.md` pela `qa-finding-protocol`, nunca relato solto na conversa; ao citar bom acabamento, cite uma referência de categoria (Linear, Stripe, Vercel, Apple), nunca um exemplo genérico. Quando a direção for ambígua ou cara de mudar depois, **sugira e pergunte**: domínio (5+ conceitos) · paleta (5+ cores desse domínio) · assinatura · rejeição (óbvio → alternativa) · direção que liga tudo; depois "essa direção serve?".

**Verificações finais (interface de produto):** teste da troca: troque a fonte pela padrão e o layout por um modelo genérico, algo mudaria? onde não mudaria, você caiu no padrão · teste de apertar os olhos: a hierarquia continua legível desfocada? · teste da assinatura: aponte cinco lugares específicos onde ela aparece ("a sensação geral" não vale) · teste dos tokens: leia as variáveis CSS em voz alta, elas pertencem a ESTE produto ou a qualquer projeto?

## Checklist antes da entrega

- [ ] Contraste, foco, rótulos, texto alternativo e caminho pelo teclado verificados
- [ ] Alvos de toque e cursores em todo elemento interativo
- [ ] Modo claro e escuro conferidos
- [ ] Responsivo em 375 / 768 / 1024 / 1440, sem rolagem horizontal
- [ ] Movimento reduzido respeitado; sem salto de conteúdo no carregamento
- [ ] Ícones de um único conjunto, sem emoji; logos corretos
- [ ] Tokens e componentes do projeto usados; nada fixo no código que o design system já define
- [ ] Interface de produto: um foco nomeado por tela, todos os estados interativos e de dados presentes, uma estratégia de profundidade, as quatro verificações finais (troca / olhos apertados / assinatura / tokens) aprovadas

## Origem

Skill original do Etna. A seção Interface de produto reescreve, na nossa voz, a doutrina de
acabamento de interface de produto da antiga `etna-app-ui` (absorvida aqui), a partir de fatos
técnicos de domínio público; nenhum texto ou código de terceiros foi reproduzido. Referência dessa
doutrina: interface-design (github.com/damolaaki/interface-design), MIT, com atribuição mantida.
