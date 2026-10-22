---
name: etna-cinema-plan
description: "Use when a squad worker must PLAN a multi-shot video — decompose a brief into a shot list with beat structure, write a continuity bible, and lock character / style across shots. Covers the 6-scene arc, the cut rules (one transformation / one action / one camera move / 1-2 beats per 5s), genre + ad recipes, the two-layer brief (Layer-1 prose brief vs Layer-2 execution prompt), and shot-bridging (how shot N+1 continues from shot N). Bind to the planner / director worker — NOT the orchestrator. Triggers: shot list, storyboard, video plan, multi-shot decomposition, continuity bible, character consistency across shots, ad format, genre template, beat structure."
---

> **Mídia no Etna (vale sobre qualquer outra menção neste arquivo).** Ferramentas MCP do Etna: `etna_imagem_gerar(prompt, outPath, provider?, imageUrl?, formato?)`, `etna_video_gerar(prompt, outPath, provider?, imageUrl?, endImageUrl?, formato?, segundos?)`, `etna_voz_gerar(prompt, outPath, voiceId?)` e `etna_midia_provedores()` (quem está pronto, a escolha da pessoa e o modelo de cada um; nunca mostra chave). Provedores: imagem = `antigravity` (padrão, plano do Google, sem chave) | `higgsfield` | `gemini` | `openai` | `fal`; vídeo = `higgsfield` (Seedance) | `fal` (Kling: o único que respeita `endImageUrl`, e o Etna já o escolhe sozinho quando você passa `endImageUrl`); voz = `elevenlabs`. Não passe `provider` a menos que a tarefa exija: vale a IA que a pessoa escolheu em Configurações › Imagem e vídeo. O Antigravity NÃO gera vídeo. `outPath` é relativo à pasta do painel. Sem provedor pronto a ferramenta diz o que falta: pare e avise a pessoa; nunca troque de motor em silêncio. Os nomes antigos (`google-image`, `openai-image`, `replicate-video`, `selectedModel`/`enabledModels`) = `antigravity`/`gemini`, `openai`, `fal` e o campo `modelo` de `etna_midia_provedores`.


# etna-cinema-plan — O worker diretor

Transforme um briefing em uma lista de planos + uma bíblia de continuidade + briefings de Camada 1 por plano, e
devolva tudo ao coordenador para distribuir em paralelo. É a inteligência de decomposição da equipe de cinema.

> **Onde esta skill mora.** Ligue o `etna-cinema-plan` ao painel **worker de direção / planejamento**, nunca ao
> coordenador. O coordenador é fixo e genérico: não carrega skill nenhuma e só roteia, sobe workers e colhe. O worker
> diretor é o cérebro que lê o briefing e emite o plano. A entrega dele são **três artefatos**: (1) uma lista de
> planos (o grafo do time), (2) um briefing em prosa de Camada 1 por plano, (3) a especificação da âncora
> compartilhada (bíblia de continuidade + plano da imagem de referência + prefácio de estilo travado). O coordenador
> consome isso e distribui cada plano para um worker DP do **etna-cinema-shot**, que escreve o prompt de execução
> (Camada 2) e chama a ferramenta.

> **Divisão de camadas (lei que rege tudo).** Esta skill é dona do planejamento, da decomposição e da política de
> continuidade. Ela escreve documentos de plano e briefings em prosa: nunca inventa parâmetro de ferramenta. A execução
> é fixa e mora nas skills irmãs:
> - **Vídeo** → `etna_video_gerar(prompt, outPath, provider?, imageUrl?, endImageUrl?, formato?, segundos?)`: Seedance via Higgsfield (padrão) ou Kling via fal.ai (o Etna escolhe o fal sozinho quando você passa `endImageUrl`). Texto-para-vídeo; imagem-para-vídeo quando `imageUrl` é um caminho de png. Mp4 mudo. Proporção e duração têm parâmetro (`formato`, `segundos`); o resto (fps, estilo) vai no corpo do prompt.
> - **Imagem** → `etna_imagem_gerar(prompt, outPath, provider?, imageUrl?, formato?)`: `antigravity` (nano-banana: cinematográfico / personagem / pintura) | `openai` (gpt-image: layout / texto / marca). Texto-para-imagem; imagem-para-imagem / edição / reestilização quando `imageUrl` é um caminho de png ou uma URL.
> - **Áudio** → `etna_voz_gerar(prompt, outPath, voiceId?)`: só TTS da ElevenLabs. Sem música / efeito sonoro / trilha. Trilha separada, em camada de pós, nunca gravada no mp4.
> - **Extração de quadros / montagem** → ffmpeg no Bash. **Tipografia nítida / logos / infográficos são encaminhados PARA FORA**, para as skills de Remotion (o Seedance alucina texto).

Skills irmãs do cinema: **etna-cinema-shot** (escreve as strings de prompt da Camada 2 do Seedance / imagem que o worker DP dispara) · **etna-cinema-cut** (montagem por concatenação no ffmpeg + gramática de corte) · **etna-cinema-voice** (trilha de narração em TTS da ElevenLabs). Esta skill faz referência cruzada às três; não duplica o ofício delas.

---

## O trabalho do worker diretor, em ordem

Um projeto planejado no nível do roteiro e da bíblia fica coerente; um projeto montado prompt por prompt deriva em
personagem, estilo e continuidade em três ou quatro gerações. O worker diretor faz estas passadas **por conta
própria**, antes de subir qualquer worker DP. Cada passada produz um artefato que a seguinte consome.

> Conceito → roteiro do projeto → decupagem por cena → **lista de planos** → briefings de Camada 1 por plano → **bíblia de continuidade + especificação da âncora** → (devolve ao coordenador) → workers DP escrevem os prompts de Camada 2 → gera → revisa → corrige e finaliza.
>
> O poder não está num prompt perfeito. O poder está no plano.

**Passada 1: trave o projeto, não o prompt.** Nove campos, primeiro:

> Tipo do projeto · Sujeito principal · Estilo visual · Objetivo da cena · Público · Clima · Duração · Cenário · **O que precisa continuar igual**

O último campo sustenta a carga: ele decide o contrato de continuidade. Se você não sabe o que precisa continuar igual,
todos os outros campos podem estar travados e o resultado ainda assim vai parecer desconexo.

**Passada 2: Roteiro-mestre.** A planta única do projeto (NÃO é um roteiro de cinema: explica a ideia completa com
clareza). Tem que incluir: a história / conceito · a ordem das cenas · os personagens ou produtos principais · o estilo
visual · as regras de câmera · o cenário · o tom emocional · as regras de continuidade · o que nunca deve acontecer.
Sem ele, cada plano vira uma ilha aleatória.

**Passada 3: separe o roteiro do prompt.** "O roteiro é o que acontece; o prompt é como a IA mostra." Mantenha os dois em
documentos separados; não deixe instruções com cara de prompt vazarem para o roteiro. Cada batida da história se
decompõe em quatro categorias de instrução de produção: **Notas de câmera · Direção de luz · Movimento do sujeito · Detalhe do ambiente.**

**Passada 4: dê a cada cena um só trabalho** (o arco de 6 cenas, abaixo).

**Passada 5: corte as cenas em planos do tamanho de um worker** (as regras de corte, abaixo). A lista de planos É o time.

**Passada 6: monte a bíblia de continuidade + a especificação da âncora** (a bíblia, abaixo). É o contrato compartilhado e persistido que todo worker a jusante lê.

**Passada 7: escreva um briefing de Camada 1 por plano** (a seção de autoria em duas camadas, abaixo).

**Passada 8: escreva a rubrica de sucesso falsificável ANTES de devolver** (abaixo), para que o aceite seja binário, e não feito depois.

---

## O arco de decomposição em 6 cenas (narrativa → lista de planos)

Um mapeamento reutilizável de narrativa para lista de planos. O arco dá a sequência de *propósitos*; as regras de corte
abaixo decidem onde cada cena se divide em gerações do tamanho de um worker.

> **Cena 1: plano de estabelecimento**: aberto, situa o lugar.
> **Cena 2: apresentação do personagem**: médio, mostra o protagonista.
> **Cena 3: batida de ação**: fechado, movimento.
> **Cena 4: reação**: primeiro plano, emoção.
> **Cena 5: consequência / virada**: médio ou aberto.
> **Cena 6: resolução / fechamento**: varia.

Seis propósitos de cena cobrem a maior parte do trabalho: **Apresentar o personagem · Mostrar o lugar · Criar tensão · Revelar o produto · Criar emoção · Entregar a ação.** Uma boa cena responde a seis perguntas: *Quem está no plano? · Onde está a câmera? · O que o sujeito está fazendo? · O que o espectador deve notar primeiro? · O que precisa continuar visível? · O que não deve acontecer?* Tentar fazer uma cena fazer coisa demais causa mistura: movimento bagunçado, ângulos errados, gente a mais, mãos quebradas, objetos que somem.

Uma cena pode ocupar vários planos. O arco diz a ordem dos propósitos; as regras de corte dizem onde dividir.

---

## As regras de corte: onde o roteiro quebra em planos

Cada plano é trabalho de um painel. Quatro regras decidem onde o roteiro corta.

**Regra de corte 1: uma transformação por plano.** Planeje exatamente **uma mudança de estado por geração**: um lugar para
outro lugar, uma batida emocional para a próxima, uma ação para a consequência. Planos com várias batidas ("ela entra,
vê o corpo, saca a arma, avança") obrigam o modelo a interpolar entre duas ou três intenções diferentes, e o resultado
deriva em pelo menos uma delas. **Corte o plano na primeira batida. Gere a segunda batida como plano próprio.**

**Regra de corte 2: uma ação principal por clipe.** Uma ação principal por clipe do Seedance, com uma ou duas ações
secundárias no máximo. (É a regra de contagem de ações por plano, distinta do propósito narrativo de cada cena.) Veja
etna-cinema-shot § Uma ação por clipe.

**Regra de corte 3: um movimento de câmera por plano.** Um movimento de câmera dominante por geração. Empilhar movimentos
("travelling para dentro, depois panorâmica rápida, depois grua para cima") é uma múltipla transformação disfarçada e
deriva do mesmo jeito. Se uma cena precisa de dois movimentos, são dois planos.

**Regra de corte 4: portão de densidade de batidas (1 a 2 batidas a cada 5 segundos → dividir).** Oriente-se por **1 a 2
batidas a cada 5 segundos** de clipe. Uma "batida" é qualquer mudança de estado que o olho registra (uma ação, uma
reação, uma revelação, um movimento de câmera, uma mudança de luz). Se um plano planejado passar de ~2 batidas por 5 s,
o modelo tem coisa demais para interpolar: **divida** em mais planos, mais curtos. Roteiros mais densos significam mais
painéis, não clipes mais longos.

### Tabela de densidade de batidas

| Janela | Batidas | Exemplo |
|---|---|---|
| 3 a 5 s | 1 a 2 | Pular + pousar |
| 5 a 8 s | 2 a 3 | Pular + pousar + sacar a arma |
| 8 a 12 s | 3 a 5 | Pular + pousar + sacar + atirar + se abrigar |
| 12 a 15 s | 4 a 6 | Sequência de ação completa → **use vários planos** |

> **Exemplo de uma ação só.** ERRADO (um plano): "Ela pula o muro, rola ao cair, saca a arma e dispara três tiros
> correndo." CERTO (3 planos): Plano 1 "Ela salta o muro, o casaco abrindo. Ao cair com força, rola para a frente."
> · Plano 2 "Ao se levantar do rolamento, saca a arma num único movimento fluido." · Plano 3 "Correndo em sprint total,
> dispara três tiros. O clarão da boca da arma ilumina o beco."

**Disciplina de geração única.** Planeje o plano bem o bastante para que a **primeira geração seja o trabalho**. Gerar e
escolher entre vinte é falha de orçamento, não de fluxo. Trate cada geração como o entregável, mesmo sabendo que um
*aproveitável* pode custar dezenas de tentativas (isso é o funil, não o plano).

> **Heróis web de scroll são outra equipe.** Um *herói de scrub* (scroll = tempo de reprodução), um loop contínuo de
> fundo ou um clipe de capa de site NÃO é vídeo narrativo: é um plano-sequência contínuo, sem nenhuma imobilidade, e as
> regras de corte / o arco de 6 cenas / o contrato de 2 segundos de imobilidade daqui estão errados para ele. Esse
> ofício mora na equipe de **Site Cinematográfico** (`etna-site-scrub` / `etna-site-encode`), não aqui. Se o briefing
> disser scrub / scroll / scrollytelling / rolável / loop de fundo / herói web, encaminhe para lá.

---

## Taxonomia de dependências → o grafo do time

A lista de planos vira um grafo (DAG). Separe cada plano pelo que ele **realmente depende**: essa separação dá velocidade
sem perder controle estrutural, e É o grafo que o diretor devolve.

| Balde | O que é | Lugar no grafo |
|---|---|---|
| **Depende de um quadro final** | precisa da saída da geração anterior (âncoras de continuação, edições de um quadro renderizado) | **aresta SEQUENCIAL**: o plano N espera o último quadro extraído do plano N-1 como `imageUrl` |
| **Pode ser escrito em paralelo** | planos independentes; sem dependência de renderização | **leque PARALELO**: workers DP rodam ao mesmo tempo |
| **Construção da espinha** | ordem das cenas, identificação de pontes, mapeamento do arco de continuidade | **o próprio worker diretor** (esta skill, antes do leque) |
| **Espera refinamento posterior** | inserções a nível de plano, micro-prompts, ajustes de batida | **onda de refinamento**: depois que a estrutura estiver travada |

**Seletor de topologia (primeira decisão do diretor por cluster):**

| Você está planejando | Topologia |
|---|---|
| Um plano cinematográfico só | **Sem time.** Uma imagem (Quadro-herói) → um vídeo. Montar um time para um clipe de 5 s é erro de excesso de engenharia. |
| Filme curto / série, estilo consistente | **Leque paralelo**: todos os planos compartilham UMA imagem de referência + prefácio de estilo travado; workers DP rodam ao mesmo tempo. |
| Série social, mesmo personagem | **Leque paralelo**: personagem travado uma vez, modelo por post, o mesmo modificador de estilo em todo post. |
| Teste A/B rápido (até 5 direções) | **Leque paralelo**, sem montagem: clipes únicos, exportação direta. |
| Estilo muda de cena para cena OU cada plano precisa do último quadro do plano anterior | **Cadeia de continuidade sequencial**: o plano N recebe o último quadro extraído do plano N-1 como `imageUrl` + o prompt do plano N-1 como contexto. |
| Misto | **DAG híbrido**: clusters paralelos de planos do mesmo estilo, unidos por arestas sequenciais onde a continuidade carrega o peso. |

Desenhe o DAG explicitamente antes de devolver: os nós são planos / painéis; as arestas são as passagens de quadro final
(as pontes, abaixo).

### Heurística de densidade de planos (quantos painéis)

Roteiro mais denso = **mais painéis, não clipes mais longos.** Cada plano tem teto de uma transformação / uma ação
principal / um movimento de câmera / ~2 batidas por 5 s. Quando um plano planejado passa de qualquer um desses, divida-o e
acrescente um painel. O diretor dimensiona o time contando as batidas do Roteiro-mestre e dividindo pelo orçamento de
densidade de batidas, não chutando um número de planos.

---

## AUTORIA EM DUAS CAMADAS DO PROMPT (o briefing que o diretor escreve vs o prompt que o DP escreve)

É a passagem que carrega peso e o ponto mais comum de falha. Há **dois documentos distintos**, escritos por **dois painéis
distintos**:

**Camada 1: o BRIEFING EM PROSA por plano (o worker diretor escreve).** Linguagem simples, estruturado, completo. Diz ao
worker DP tudo que ele precisa para escrever o prompt de execução **sem reconstruir o projeto**. Um briefing de Camada 1
nomeia:

- **Sujeito**: quem / o quê está no quadro (por identificador de referência quando for um personagem recorrente; por marcas visuais caso contrário: nunca por nome próprio ou rótulo de idade).
- **Batida**: a única transformação / ação que este plano entrega, e o lugar dela no arco de 6 cenas.
- **Look**: o prefácio de estilo travado (paleta / correção de cor / luz / sensação óptica), copiado da bíblia, idêntico em todo plano.
- **Referências de continuidade**: qual caminho de PNG de referência é o `imageUrl` deste plano; para um plano com ponte, o caminho do último quadro E uma descrição curta em texto desse quadro (veja Pontes).
- **Restrições**: a lista de regras negativas do projeto, o movimento de câmera único, a classe de artefato por gênero para autoverificar, o mandato do fechamento de 2 segundos de imobilidade.

**Camada 2: o PROMPT DE EXECUÇÃO (o worker DP do etna-cinema-shot escreve).** A string enxuta do Seedance / da imagem que a
ferramenta de fato recebe: fórmula CSLA / de seis campos, divisão Identidade × Movimento, movimento de câmera nomeado em
linguagem simples, antiplástico limpo. **Esta skill não escreve a Camada 2.** Ela entrega a Camada 1 ao DP e deixa o
etna-cinema-shot compilá-la.

> **Modo de falha: briefing de Camada 1 fino gera saída reencenada, com continuidade quebrada.** Quando o diretor entrega
> um briefing que diz só "plano 3, ela corre", o worker DP inventa o figurino, reencena o local, redescreve o rosto e
> escolhe uma câmera aleatória; e em N painéis paralelos cada invenção diverge. A bíblia de continuidade existe
> justamente para que o briefing seja **grosso**: o DP preenche só o *movimento*, nunca *identidade, estilo, local ou
> look*, porque o briefing já os prendeu por referência. **Regra prática: se o worker DP precisar adivinhar qualquer fato
> de aparência, local ou estilo, o briefing de Camada 1 estava fino demais: engrosse antes de distribuir.**

### Esquema do briefing de Camada 1 por plano (o que o diretor emite por plano)

```
[PLANO]      índice · propósito (arco de 6 cenas) · topologia (paralelo | aresta sequencial do plano K)
[ÂNCORA]     imageUrl = <caminho da imagem de referência compartilhada>   (idêntico entre planos do mesmo ativo)
             — ou, para um plano com ponte: frameK.png (último quadro extraído do plano K) + sua descrição em texto
[IDENTIDADE] <Bloco de Identidade literal: copiado da bíblia, NUNCA reescrito>
[LOOK]       <prefácio de estilo travado: paleta/correção/luz/óptica, idêntico em todo plano>
[BATIDA]     a ÚNICA transformação / ação que este plano entrega; um movimento de câmera (nomeado em linguagem simples)
[NOTA DE MOVIMENTO] ← o que SE MOVE ou MUDA (o DP expande isso no Bloco de Movimento da Camada 2). Uma ação
             principal, até 2 secundárias. Feche com o contrato de 2 segundos de imobilidade.
[NEGATIVO]   <lista de regras negativas do projeto: cresce conforme as falhas viram regras>
[PORTÃO]     classe de artefato por gênero para autoverificar primeiro (Ação→Corpo/Movimento; Terror→Conteúdo/Segurança;
             Personagem→Rosto/Identidade); rode o lint de pré-voo do etna-cinema-shot antes de gerar.
```

O coordenador recebe um desses por plano, mais a especificação compartilhada da âncora, e distribui cada um para um worker DP (etna-cinema-shot).

---

## PONTES: como o plano N+1 continua o plano N

A continuidade sequencial é o método de maior alavanca para qualquer modelo de imagem-para-vídeo: **dê o último quadro da
cena anterior + uma descrição dele ao briefing da cena seguinte.** O estilo pode mudar radicalmente de cena para cena,
enquanto personagem, objetos e continuidade da história se mantêm.

Um worker DP com ponte recebe **três** entradas no seu briefing de Camada 1:

1. **A nota de movimento** (o DP a expande no próprio Bloco de Movimento, sobre o Look travado).
2. **O último quadro do plano N como `imageUrl`**: passado como imagem inicial do plano N+1.
3. **Uma DESCRIÇÃO CURTA EM TEXTO desse último quadro**, colada no briefing.

> **Por que a descrição em texto não é negociável.** O escritor do prompt (worker DP) é um **painel diferente** do gerador
> e do painel que renderizou o plano N. O DP não enxerga os pixels de `frameN.png` enquanto escreve, então o visual desse
> quadro precisa ser **descrito, não presumido**. A ponte = `imageUrl` (os pixels) **E** uma descrição em prosa de 1 a 2
> frases do quadro (o visual para o qual o DP escreve): pose, enquadramento, estado da luz, o que está assentado e pronto
> para se mover. Sem a descrição, o DP redescreve de imaginação e quebra a emenda que deveria ficar invisível.

**A etapa de extração (ffmpeg no Bash: o diretor planeja, o etna-cinema-cut / o DP executa):**

```bash
ffmpeg -sseof -0.1 -i shotN.mp4 -frames:v 1 -q:v 2 frameN.png
```

`-sseof -0.1` posiciona 0,1 s antes do fim; `-frames:v 1` pega um quadro; `-q:v 2` mantém quase sem perda. Depois,
`frameN.png` vira o `imageUrl` do plano N+1. **Último quadro do plano A = primeiro quadro do plano B = continuidade sem
emenda.** Os últimos quadros carregam a física própria do modelo (desfoque de movimento, peso, impulso) e composições que
você nunca pediria diretamente no prompt.

**Combina com o contrato de 2 segundos de imobilidade.** Todo plano fecha com imobilidade para que os cortes caiam limpos e
o último quadro extraído alimente o plano seguinte sem um solavanco no meio da ação:

> Peça no prompt um **momento explícito de ~2 segundos parado ou quase parado no INÍCIO e no FIM de cada plano**: um olhar
> mantido, uma pose assentada, uma pausa segurada antes de o movimento começar, uma respiração segurada depois que ele
> para. Quem edita coloca os cortes suaves em **imobilidade, não em movimento**. O meio pode ser tão cinético quanto o
> roteiro exigir; as bordas é que ganham os cortes.

Esta é uma linha obrigatória na `[NOTA DE MOVIMENTO]` de todo briefing de Camada 1.

**Cinco regras de continuação** (o diretor as codifica nos briefings com ponte): (1) Âncora no último quadro. (2) Bloco de
Identidade colado palavra por palavra. (3) Clipe anterior como memória secundária: uma frase de referência. (4) Continuação
imediata: próximo quadro, sem pulo, sem fade, sem corte. (5) Sem repetir a ação: estenda, não faça loop. Frases
anti-repetição para semear: `start immediately after the final frame` / `do not restage the earlier beat` /
`continue forward into the new action` / `preserve the same fatigue state and emotional carryover`.

> **Interpolação entre quadros-chave só no Kling (fal).** `etna_video_gerar` tem `endImageUrl`, mas o Seedance (Higgsfield)
> o ignora. Sem `endImageUrl` (ou sem chave do fal), a cadeia de extração de quadros acima é o substituto:
> encadeie planos curtos, cada um começando do último quadro extraído do plano anterior. Não prometa interpolação
> de início e fim fora do Kling.

---

## A bíblia de continuidade (a especificação da âncora que o diretor devolve)

Workers DP que rodam independentes vão reinterpretar cada um o personagem, o cômodo, o produto, a não ser que a identidade
seja **referenciada, não redescrita.** Redescrever um ativo dentro de cada prompt é a causa-raiz de toda deriva do tipo
"cada plano reinterpreta o X". O diretor faz valer um contrato de quatro partes na bíblia:

1. **UMA imagem de referência compartilhada → o MESMO `imageUrl` para todo worker.** Cada ativo recorrente é gerado UMA vez com `etna_imagem_gerar`, e depois o *mesmo* caminho de arquivo é distribuído como `imageUrl` a todo plano que precisa dele. Monte uma folha de referência quando uma propriedade aparecer em **3 ou mais planos**; detalhes de plano único são escritos em linha.

2. **Bloco de Identidade literal em todo briefing.** Copie a descrição do personagem **idêntica** em todo briefing. Mesmo pequenas diferenças de redação fazem o personagem derivar entre painéis. A identidade (rosto, corpo, cabelo, figurino, marcas) mora na imagem de referência + no Bloco de Identidade; **nunca** coloque descritores de rosto / roupa na nota de movimento quando uma referência de identidade está ativa.

3. **Preâmbulo de Look travado em todo briefing.** O modificador de estilo (paleta, correção, técnica de luz, sensação óptica) é **idêntico sempre; só a cena muda.** Escrito uma vez, colado no início de todo briefing, travado.

4. **Os workers escrevem SÓ o movimento.** Identidade, Look e local são da bíblia e travados. Cada DP escreve apenas o que *se move* no seu plano.

> Para planos com mais de um personagem, o diretor também aprova UM esquema de posicionamento espacial visto de cima, e
> cada briefing o cita em termos **absolutos**: "Gandelfina fica atrás da mesa, de frente para leste, na janela; Roko fica a
> 2 m dela, de frente para norte, na direção da porta" vale mais que "Gandelfina perto da mesa, Roko por ali". Veja
> etna-cinema-shot § Posicionamento espacial.

### A divisão Identidade × Movimento (a lei antideriva)

Quando uma imagem de referência está ativa, todo prompt TEM que se dividir em dois blocos. O diretor escreve o Bloco de
Identidade uma vez na bíblia; o DP escreve o Bloco de Movimento por plano.

| Bloco de Identidade (da bíblia, literal) | Bloco de Movimento (do DP, por plano) |
|---|---|
| Formato do rosto, tom de pele, cor dos olhos | Nome do movimento de câmera |
| Penteado, cor, comprimento do cabelo | Verbos de ação (corre, vira, senta) |
| Tipo de corpo, altura, porte | Movimento do ambiente (vento, chuva, luzes) |
| Roupa, acessórios, joias | Sinais de velocidade e tempo |
| Cicatrizes, tatuagens, marcas distintivas | Mudanças atmosféricas (trocas de luz, névoa) |
| Paleta de cores do personagem | Estilo e correção de cor da cena |

**Por que funciona:** o modelo deforma o rosto no meio do clipe quando relê descritores de rosto *enquanto* processa o
movimento. Manter os descritores fora do texto de movimento trava a identidade. **Regra-chave:** o PNG já carrega o rosto:
descreva só o que é *diferente* do personagem base (roupa trocada, cenário, expressão, ação).

### Folha de personagem (geometria de build para o PNG de referência)

Uma referência de vários ângulos melhora bastante a consistência em ângulos extremos e perfis. Gere a folha inteira em **um
prompt → uma imagem 16:9 → grade 3×2, seis painéis rotulados**, com a identidade descrita uma vez (passada única mantém a
identidade mais travada; montagem em várias etapas deriva de painel para painel). Use `etna_imagem_gerar(provider:'antigravity')`.

- **P1: corpo de frente** (de frente, neutro, da cabeça aos pés) · **P2: três quartos** (~30°, peso no quadril de trás) · **P3: corpo de costas** · **P4: retrato da cintura para cima** · **P5: detalhe das mãos em primeiro plano** (pilha de anéis, acabamento da unha, adereço na mão) · **P6: detalhe do rosto em primeiro plano** (da clavícula para cima; fica como fonte de rosto para recortar e colar em planos abertos com rosto de plástico).

Feche com: `Identical character identity locked across all six panels. Uniform studio backdrop and lighting across all six panels.`

> **Fato de capacidade: refine reescrevendo o prompt, nunca editando.** Pra
> refinar, prefira reescrever o prompt; `imageUrl` em `etna_imagem_gerar` serve de referência/âncora, não de editor com máscara. Para corrigir um detalhe, aperte essa UMA cláusula
> no Bloco de Identidade (regra de uma variável só) e **regere**: mesmo bloco travado + a correção. Não existe chamada de
> edição / inpaint. Para continuidade entre várias **imagens fixas**, cole o **Bloco de Identidade idêntico + o preâmbulo
> de Look travado** em todo prompt de texto-para-imagem: a reutilização literal é o *único* mecanismo de identidade entre
> imagens (não existe entrada de imagem de referência).

### Bloco de âncora do personagem (no momento do plano, por personagem em cena)

O diretor nomeia, por personagem e por plano, dez atributos que o DP tem que respeitar: **1 Identidade · 2 Posição na tela
(qualitativa + %) · 3 Camada de profundidade (primeiro plano / meio / fundo) · 4 Ocupação do quadro (%) · 5 Orientação do
corpo (para a câmera / de costas / perfil esquerdo / perfil direito / três quartos) · 6 Pose · 7 Direção do olhar (posição no
quadro ou `olhando para o Personagem B`) · 8 Pontos de contato · 9 Trava de estado (calmo / exausto / ferido / encharcado / em
movimento) · 10 Expressão facial.**

**Acompanhamento de estado de várias formas (supervisão do roteiro).** Quando um personagem muda de estado ao longo do
projeto (ferimentos persistentes, troca de figurino, transformação em várias etapas), gere **um PNG de referência separado
por estado**. Um personagem de cinco etapas (inicial → ferido na luta → parcialmente transformado → quase completo →
totalmente transformado) recebe **cinco PNGs de referência distintos**. O plano referencia o PNG correspondente pelo caminho;
o briefing nomeia a etapa no Bloco de Identidade. Uma passada de `etna_imagem_gerar` por estado; o ganho é não aparecer bug
de continuidade na hora de revisar os quadros.

### Bíblia do projeto: bloco de personagem para copiar e colar

Mantenha uma bíblia em texto simples que o diretor e todo worker DP compartilham, um bloco por personagem:

```
PERSONAGEM: Anna
  PNG de referência: char_anna.png        (variantes de estado: char_anna_injured.png)
  rosto/corpo: fim dos 20 anos, rosto oval, olhos verdes, sardas leves, corpo alto e esguio
  cabelo: castanho-avermelhado na altura dos ombros, ondas soltas
  figurino (padrão): jaqueta de couro preta ajustada, jeans índigo escuro, tênis branco
  marca registrada: pingente prateado, relógio no pulso esquerdo
  notas de estado: a partir do PLANO 4 usa char_anna_injured.png (corte na bochecha, manga rasgada)
```

A bíblia é a única fonte da verdade para a identidade. Um worker DP cola o bloco correspondente no seu Bloco de Identidade e
o caminho do PNG correspondente em `imageUrl`: assim a identidade se mantém entre painéis, e não só entre planos.

---

## Banco de gêneros (9 estruturas centrais de batida → decomposições por plano)

Cada gênero = um **padrão central** (a espinha narrativa reutilizável, que também é o mapa de decomposição em planos) +
um vocabulário de câmera escrito em prosa. O diretor escolhe o padrão, divide a estrutura de batidas em N planos e escreve um
briefing de Camada 1 por plano. O DP compila cada um num prompt de Seedance. (Nomes de câmera são **descrições em prosa do
movimento**, nunca IDs de predefinição / controle: o Seedance lê a descrição da câmera.)

| # | Gênero | Padrão central (estrutura de batidas) | Câmera (prosa) | Formato do time |
|---|---|---|---|---|
| 1 | **Ação / perseguição** | `Estabelecer → Perseguição → Obstáculo → Clímax` | Corrida de ação, drone FPV, zoom brusco para dentro, bullet time | 4 planos → 4 painéis |
| 2 | **Drama emocional** | `Estabelecer o espaço → Revelar o estado do personagem → Batida emocional` | Travelling para dentro, arco, acompanhamento de cabeça, troca de foco | normalmente 1 take contínuo |
| 3 | **Anúncio de produto** | `Revelação da textura → Vitrine de características → Conexão emocional → Quadro final` | Lazy Susan (plataforma giratória), travelling para dentro, braço robótico | quadro-herói primeiro → revelação em imagem-para-vídeo |
| 4 | **Ficção científica / futurista** | `Estabelecer o mundo → Revelar a tecnologia / ameaça → Batida de ação` | Grua para cima, drone FPV, travelling para trás super, ângulo holandês | 3 planos |
| 5 | **Terror / sobrenatural** | `Calma falsa → Detalhe errado → Escalada → Revelação` | Travelling para dentro, ângulo holandês, câmera na mão, zoom brusco | 3 a 4 planos |
| 6 | **Romance / íntimo** | `Encontro de olhares → Tensão → Momento de conexão` | Arco, travelling para dentro, troca de foco, empurrão lento até quase um beijo | 1 a 3 planos |
| 7 | **Documentário / natureza** | `Estabelecer o ambiente → Sujeito em contexto → Momento observacional` | Grua para baixo, timelapse, travelling lateral, vista de cima | 3 planos; **sem efeitos artificiais: puramente observacional** |
| 8 | **Dança / clipe musical** | `Estabelecer o espaço → A performance cresce → Clímax no ritmo` | Órbita de 360°, travelling para dentro/fora no ritmo, vista de cima, zoom brusco | 3+ planos; mp4 mudo: música entra no etna-cinema-cut |
| 9 | **Transformação / antes e depois** | `Estado anterior → Gatilho → Transformação → Estado posterior` | Travelling para dentro no gatilho, um take contínuo sempre que possível | 1 take contínuo; **nomeie o ponto médio explicitamente** |

**Roteamento de restrição negativa por gênero (mantenha literal).** Escolha o gênero e antecipe a classe típica de artefato
desse gênero no slot `[PORTÃO]`, antes de o DP gerar:

> **Receitas de ação → Corpo/Movimento. Terror → Filtro de conteúdo/Segurança. Foco em personagem → Rosto/Identidade.**

**Transformação exige um ponto médio explícito.** Uma mudança de estado num único take TEM que nomear o intervalo (costuras
se repuxando, fissuras finas de luz azul traçando o esterno). Sem isso, o modelo faz um corte brusco ou renderiza um borrão
ambíguo. Um take contínuo dentro de um clipe.

---

## Banco de predefinições de anúncio (9 receitas de marketing → prefixos de prompt)

Para trabalho de marketing, o diretor escolhe uma predefinição, e o briefing = `câmera/registro da predefinição + (gancho
opcional) + (cenário) + produto/conceito + Contrato de câmera + Look + bloco negativo`. O DP compila para um prompt de
Seedance. (Toda a camada de API de roteamento de terceiros (`marketing_studio_video`, `hook_id`, `setting_id`, avatares/mídias,
créditos) foi descartada; estes são só modelos de prompt nomeados.)

| # | Predefinição | Câmera / registro | Observações |
|---|---|---|---|
| 1 | **UGC** | Enquadramento de selfie de celular, na mão, altura dos olhos, take único contínuo; casual, conversacional | Variante ASMR = ambiente íntimo + narração em TTS + SEM gancho |
| 2 | **Tutorial** | Câmera estável (tripé / vista de cima / na mão travada); cortes permitidos entre etapas; voz imperativa ("aplique", "segure", "pressione") | passo a passo / receita |
| 3 | **Desembalando** | Vista de cima ou de três quartos; mãos no quadro; close táteis nos momentos de revelação | precisa de uma imagem do ativo da embalagem (gera com `etna_imagem_gerar`, passa como `imageUrl`) |
| 4 | **Movimento intenso** | Herói cinético de produto (respingo / despejo / giro / queda); panorâmicas rápidas, órbitas, rampas de velocidade; tiro de embalagem automático; **funciona sem pessoa** | roda com **prompts de 5 palavras** quando uma referência de ativo carrega o peso; o logo pode ser o herói |
| 5 | **Avaliação de produto** | Plano médio do apresentador + inserções de detalhe do produto (B-roll) | medido, observacional, terceira pessoa |
| 6 | **Comercial de TV** | Travelling / grua composto; arco estruturado (estabelecer → produto → estilo de vida → herói/logo) | capaz de prompt de 5 palavras; **o plano de embalagem padrão tem que ser negado explicitamente** quando não for desejado |
| 7 | **Carta curinga** | Plano único surreal; permissão para quebrar a gramática de anúncio: geometria impossível, escala surreal | — |
| 8 | **Provador virtual UGC** | Enquadramento de selfie ou espelho; ambiente casual; movimento natural (virar / andar / gesto); de celular | experimentar antes de comprar, registro casual |
| 9 | **Provador virtual profissional** | Qualidade de estúdio; fundo limpo (parede de ciclorama / fundo contínuo); luz controlada; poses compostas; órbita / empurrão / estático editorial | editorial / lookbook |

**Biblioteca de ganchos** (estruturas de cena visual coladas no briefing, não legendas): **Acrobático**: Produto atingido ·
Objeto aleatório no microfone · Nevasca · Produto desviado. **Sutil**: Apimentado · Entrevista · Produto caindo · Esbarrão na
câmera · Fracasso épico.

**Biblioteca de cenários:** **Realistas**: Quarto · Banheiro · Cozinha · Escritório · Dentro do carro · Rua · Academia · Natureza.
**Irrealistas**: Asa de avião · Telhado · Borda de vulcão · Avaliador minúsculo · Teto de carro · Surfando no trem.

**Técnica de prompt de anúncio que o diretor semeia nos briefings:**

- **Contrato de câmera**: abra com uma regra firme de câmera, reforçada em cada batida: `CAMERA: COMPLETELY STATIC throughout. Fixed position, fixed angle, zero movement. Only subjects and objects move within the frame.` (ou a variante de deriva lateral: `Camera stays strictly side-on the entire time, drifting smoothly alongside him at constant speed and height, never ahead, never behind, never rotating. One continuous uncut shot.`)
- **Trava de identidade** (o sistema de avatares foi descartado; o ofício sobrevive pela PNG de referência): `the female model — use her exact face, hair, and body throughout the entire video without any changes.`
- **Cabeçalho de campanha com vários clipes** propagado a todo clipe / painel, depois um `## CLIP N` nomeado por plano: isso É a decomposição em planos: o diretor escreve o contrato compartilhado de LOCAL + CÂMERA, distribui cada `## CLIP N` a um DP, e o etna-cinema-cut monta na ordem via concatenação no ffmpeg. Continuidade = trava de identidade + uma PNG de referência compartilhada passada como `imageUrl` + o estado "já vestindo X" de cada clipe.
- **Âncora de cor única**: nomeie UMA cor saturada como "a única cor saturada" e fixe um hex (`#d1fe17`) para que ela fique exata entre gerações.

**Clusters de restrição negativa por formato (mantenha literal):**

| Cluster | Use quando |
|---|---|
| `NO bag, NO backpack, NO purse` (por clipe) | o modelo continua acrescentando acessórios incidentais a uma pessoa |
| `No VFX. No box unpacking.` | Comercial de TV / visual de rua limpo |
| `NO visual effects, NO lightning, NO energy beams, NO particles, NO light trails on the character.` | o modelo exagera em efeitos de energia |
| `ABSOLUTELY NO PACKSHOT. NEVER SHOW ISOLATED PRODUCTS.` | o final padrão de embalagem do Comercial de TV não é desejado |
| `no shadows, no gradients, no clipping, no cropping` | isolamento limpo de foto de produto |
| `NO text, NO callouts, NO labels` / `NO letters, NO text, NO words` | o Seedance alucina texto: mantenha fora |

**Contornos dos limites do motor (dispositivos criativos transferíveis que o diretor planeja em torno deles):** vários locais
num take → **cortes de portal** ("cortes retos de borda dura no ar aberto, ele corre direto através"); troca de figurino →
**itens flutuantes** ("no instante em que ele atravessa um item flutuante, ele está instantaneamente no corpo dele, perfeitamente
ajustado"); **transição de varredura líquida** (uma onda de mercúrio dissolve o ambiente e materializa outro).

---

## Ordem pelo quadro-herói primeiro (barato antes de caro)

O diretor ordena o grafo para que as gerações baratas de imagem barrem antes das caras de vídeo:

```
Passo 1: 5 a 10 variações de imagem (custo muito baixo)     → encontre a mais próxima da visão
Passo 2: refine essa imagem (custo baixo, reescrevendo o prompt) → acerte exatamente
Passo 3: anime UMA VEZ a partir do Quadro-herói perfeito      → a primeira animação já tem base forte
```

No time isso significa: o diretor planeja um **cluster de referência / Quadro-herói que espalha gerações paralelas e baratas
de imagem e PORTEIA nas imagens fixas estarem certas ANTES de qualquer painel de vídeo rodar.** Nunca planeje ir direto a
texto-para-vídeo para um plano que você se importa.

> **Texto nítido é encaminhado PARA FORA.** Qualquer plano cuja intenção seja texto legível na tela, um conjunto de logo, um
> infográfico ou um cartão de título com legenda **não** pertence a um prompt do Seedance: o Seedance alucina texto. Encaminhe
> para as skills de Remotion (`remotion-best-practices` / `video-post` / `reels-editor`) e componha. O diretor marca isso no
> plano como fora do Seedance.

---

## Âncoras de orçamento de iteração (dimensione o cronograma com honestidade)

Um vídeo de time é um trabalho assíncrono de centenas de gerações. O diretor orça com estas âncoras conservadoras de
planejamento (não garantias):

> **Aceitação de imagem ~1,0%. Aceitação de vídeo ~1,5%.** "1 em 64 vídeos, 1 em 100 entrou."

- **Por ativo aceito:** oriente-se por ~64 gerações de vídeo / ~100 de imagem. É por isso que o paralelismo é essencial: contagens pesadas de geração por aproveitável tornam qualquer cronograma impossível sem distribuir em leque.
- **Âncora de personagem:** travar uma identidade de personagem reutilizável ≈ **~800 iterações** (~600 iniciais entre pose / figurino / expressão + ~200 de refinamento). Antecipe **só** quando o personagem se repetir em muitos planos: um personagem em 1 ou 2 planos não justifica ~800.
- **Âncora de plano:** um plano de estabelecimento de 10 segundos pesado em iterações rodou **72 gerações**. Use 72 gerações por 10 s como **teto**, não como média. Contra-intuitivamente, planos conceitualmente simples (uma panorâmica + empurrão) podem ser os *mais* pesados em iteração. Limite um plano a ~72 gerações de vídeo antes de redesenhar o prompt em vez de forçar na marra.
- **Referência de escala:** um longa-metragem 100% com IA de 90 min levou 108.859 gerações em 14 dias com uma equipe de 15 pessoas. Iteração intensa é o **modo esperado** do cinema com IA, não sinal de falha.

**Disciplina de cronograma em duas ondas.** **Onda 1: montagem bruta completa**: distribua **todos** os planos e tenha um corte bruto
completo: todas as cenas presentes, mesmo que brutas. **Onda 2: refinamento dos momentos-chave**: distribua de novo **só** os
planos de peso emocional, concentrando ali o orçamento restante; aceite takes mais brutos no resto. Sem essa divisão, o custo de
iteração estoura o orçamento antes mesmo de o projeto estar montado.

---

## Rubrica de sucesso falsificável (o diretor escreve ANTES de devolver)

Escreva os critérios primeiro, depois verifique em binário (provado / lacunas catalogadas) no corte montado. Isso impede a
racionalização depois do fato.

1. O espectador **para de perceber a geração por IA** durante toda a duração.
2. **Coerência narrativa**: abertura, meio e desfecho estruturados; as preparações têm pagamentos.
3. **Os personagens são lidos como pessoas habitadas**, não figuras produzidas por modelo com marcas de cinema de IA.
4. **As batidas emocionais pretendidas produzem a resposta pretendida no público.**
5. **O público sente um impacto emocional não previsto**, além da intenção do roteiro.

---

## Gramática de corte que o diretor entrega ao etna-cinema-cut

O diretor anota a lista de planos com a sequência, para que o etna-cinema-cut monte corretamente:

**Regra do corte de contraste duplo**: ordene clipes vizinhos para que **contrastem em dois eixos ao mesmo tempo** (aberto → fechado *e* parado → em movimento, ou frio → quente *e* lento → rápido). Um corte que muda duas coisas lê como edição intencional; um corte que muda uma lê como tremida de continuidade. Escala: `plano geral extremo → plano geral → médio → plano médio fechado → primeiro plano → primeiríssimo plano`. Caráter da câmera: `Na mão | Estática | Acompanhamento estabilizado | Grua | Aérea`: nunca repita através de um corte. O arco de 6 cenas já alterna tamanho de plano e energia: preserve essa alternância ao sequenciar. Em sequências de ação, alterne planos de rosto com referência travada e planos de ação só com texto; o cérebro de quem assiste preenche a continuidade entre os cortes.

A montagem final (concatenação no ffmpeg na ordem do corte de contraste duplo) e a camada de TTS separada são do **etna-cinema-cut** e do **etna-cinema-voice**: esta skill planeja, não executa.

---

## Lacunas de capacidade: diga com honestidade, não invente

- **O provedor de vídeo é FIXO no Seedance.** Sem escolha de modelo; descarte todo ID de modelo, CLI ou maquinário de créditos que não seja do Seedance.
- **Sem geração de música / efeito sonoro / trilha**: `etna_voz_gerar` é só TTS da ElevenLabs; o mp4 é mudo. Música e desenho de som vêm de fora da equipe (o etna-cinema-voice cuida só da trilha de narração em TTS).
- **Sem sincronia labial de verdade.** Apresentador falando para a câmera está fora do escopo; o composto de geração por personagem + imagem-no-canto é um **contorno MANUAL sinalizado**, não um caminho suportado. Avise antes de prometer um apresentador falando.
- **Sem entrada de referência de movimento, sem ampliação / troca de elenco**: nenhum parâmetro de transferência de movimento, nenhuma re-renderização para mais fidelidade, nenhuma troca de personagem em vídeo já animado (reanime um quadro-chave editado).
- **Interpolação de quadro-chave só no Kling (fal)**: no Seedance vale só o `imageUrl` de início; use a cadeia de pontes por extração de quadros.
- **Edição de imagem / imagem-para-imagem É suportada**: os dois provedores fazem imagem-para-imagem quando `imageUrl` é definido (edição inlineData do nano-banana / `/images/edits` do gpt-image). Não há parâmetro discreto de máscara / inpaint: descreva a mudança no prompt. Preserve um personagem / produto entre imagens passando a PNG de âncora compartilhada como `imageUrl`, NÃO redescrevendo-o em prosa.
- **Tipografia nítida / logos / infográficos são encaminhados PARA FORA** para o Remotion.

---

## Referências cruzadas

- **etna-cinema-shot**: compila cada briefing de Camada 1 num prompt de Camada 2 de Seedance / imagem: fórmula CSLA / de seis campos, divisão Identidade × Movimento, Uma-Ação-Por-Clipe, Posicionamento Espacial, I2V "descreva só o que se move", o portão de lint de pré-voo.
- **etna-cinema-cut**: montagem por concatenação no Bash com ffmpeg na ordem do corte de contraste duplo; a etapa de extração de quadros da ponte; encaminhamento para o Remotion para texto nítido.
- **etna-cinema-voice**: a trilha separada de narração em TTS da ElevenLabs, mixada na montagem (sem música / efeito sonoro).
