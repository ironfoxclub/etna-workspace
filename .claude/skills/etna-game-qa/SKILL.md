---
name: etna-game-qa
description: "Verifica e prepara para o lançamento jogos web (Three.js/canvas/WebGL). Cobre teste jogado por robô, checagem de celular/toque, inspeção de pixels do canvas (entropia, densidade de borda, orçamento de renderização), build de produção, caminho-base de hospedagem estática e portão da interface de depuração. Use quando pedirem para validar, testar ou liberar um jogo de navegador, provar que uma cena renderiza E joga, ou preparar a publicação estática. NÃO use para QA de site que não é jogo (webapp-testing), auditoria de acessibilidade (accessibility-auditor) nem teste de segurança de API (etna-api-audit)."
---

# etna-game-qa

## Por quê

Captura de tela bonita não prova que o jogo joga. Esta skill separa duas provas que a maioria dos
QAs de jogo confunde: **renderiza** (canvas que não é branco, pixels variados, FPS real) e **joga**
(entrada roteirizada avança o objetivo, sem travar, sem cair). Sem a segunda prova, o
"pronto para lançar" é teatro.

## Pirâmide de QA (ordem obrigatória)

1. **Sempre primeiro sem janela**: build/checagem de tipos, o servidor sobe, o console limpo. Custo visual zero.
2. **Foto do estado em texto antes do pixel**: ler `__THREE_GAME_DIAGNOSTICS__` (quadro, pontos, estado) é mais barato e mais confiável que interpretar uma captura.
3. **Captura de tela só no veredito**: desktop + celular, em jogo ativo (não a tela de título), e só depois que os dois passos acima passaram.

Pular direto para a captura de tela, sem os dois primeiros passos, é a causa raiz da maioria dos
"passou no QA, quebrado em produção".

## Fluxo de verificação

Antes de qualquer QA amplo, de celular ou de preparação de lançamento, carregue o checklist de
`references/qa-release-checklist.md`. Não pule etapa dele em silêncio; se pular alguma, registre
o motivo no ledger.

1. Instala as dependências, se faltarem.
2. Roda build e checagem de tipos.
3. Sobe o servidor de desenvolvimento ou de pré-visualização.
4. Abre o alvo no navegador.
5. Captura erro de console, de página e de rede.
6. Confere que o canvas não é branco com o inspetor de pixels (abaixo).
7. Captura tela de desktop e de celular em jogo ativo.
8. Dispara a entrada principal, a progressão do objetivo, a falha/nova tentativa e qualquer caminho de código mexido recentemente.
9. Confere o encaixe do texto do HUD, as áreas seguras, as áreas de toque e o layout responsivo.
10. Decide se abre ou amplia o conjunto de regressão visual (seção própria).
11. Decide se roda o teste jogado por robô (seção própria); é obrigatório para qualquer afirmação de "pronto para lançar" no gameplay.
12. Se o áudio mudou: desbloqueio por gesto do usuário, disparo de efeitos, início e parada do ambiente em laço, limpeza em pausa e recomeço, comportamento de mudo e volume, erro de decodificação ou carga.
13. Registra os artefatos e os findings.

## Inspetor de pixels do canvas

Se o projeto já tem um script de inspeção de canvas (comum em estruturas de jogo Three.js), use o
dele primeiro. Se não tiver, monte um inspetor fino com Playwright (`page.screenshot` do canvas +
leitura de pixel) com esta interface mínima:

```bash
node scripts/inspect-canvas.mjs --url http://127.0.0.1:5188 [--mobile] [--state <nome>] [--seed <n>]
```

- `--mobile` para emulação de celular.
- `--state <nome>` (e, opcionalmente, `--seed <n>`) para dirigir o `__GAME_TEST_HOOKS__` do jogo antes da captura. Mede cada estado nomeado (jogo ativo, falha, estresse) de forma determinística, sem jogar ao vivo; a saída leva o nome do estado no final.

O JSON de saída traz um bloco `metrics` (entropia de cor, densidade de borda, contraste de
luminância, participação da cor dominante) e um `renderBudget` comparado ao orçamento do nível de
referência. Linha acima do orçamento sem troca documentada = finding. Canvas em branco ou erro de
captura sempre sai com código de saída diferente de zero; nunca engula esse sinal.

## Teste jogado por robô: prova que o jogo joga

O inspetor de pixels prova que renderiza; o robô prova que joga. Cena linda que trava num teste de
entrada roteirizada não está pronta para o lançamento.

**Pré-requisitos no jogo:**
- `window.__GAME_DIAGNOSTICS__` publicando quadro, pontos/objetivo, estado de concluído/falha e posição do jogador a cada atualização.
- `window.__GAME_TEST_HOOKS__` com no mínimo `seed()` e `setState()` para execuções reproduzíveis.
- Toda aleatoriedade de gameplay passando pelo gerador com semente; sem isso, a métrica do robô é ruído.

**Preparação:**

```bash
cp tests/bot-playtest.template.ts tests/bot-playtest.spec.ts
npx playwright test tests/bot-playtest.spec.ts
```

Adapte o `INPUT_SCRIPT` ao controle e à fase do jogo específico: um corredor infinito segura
"para frente" e troca de faixa em cadência; um atirador de arena varre o espaço jogável; um tower
defense posiciona torres que dá pra pagar via ganchos de teste e inicia as ondas. Ganchos
específicos do gênero (`triggerBossPhase()`, `placeFirstAvailableTower()`) valem quando o teclado
puro não expressa o verbo central do jogo.

**Métricas e o que significam:**

| Métrica | Sinal de problema |
|---|---|
| `framesAdvanced` | parou de crescer → travou ou entrou em laço congelado |
| `distanceTravelled` | perto de zero com a entrada pressionada → o mapeamento da entrada quebrou |
| `scoreAfter - scoreBefore` / `stepOfFirstScore` | o teste nunca pontua → objetivo inalcançável, ilegível ou quebrado |
| `softlockWindows` | o quadro avança mas a entrada pressionada não gera movimento nem progresso → preso na geometria, estado morto, falha sem nova tentativa |
| tempo até a primeira falha | jogo que não falha não tem pressão; falha sem nova tentativa funcionando impede o lançamento |
| erros de console/página | tem que ser zero na execução inteira |

**Cuidados com WebGL sem janela:**
- Rode a suíte do Playwright com `workers: 1` para jogos WebGL: contextos paralelos sem janela disputam o rasterizador por software e o tempo de quadro desaba, o que descasa o tempo do jogo do tempo real e gera instabilidade em fase cronometrada e em referência de captura.
- **Nunca apresente FPS sem janela como evidência de desempenho.** O Chromium sem janela renderiza WebGL via SwiftShader (software): uma cena que roda a 120 fps numa GPU real pode rodar a ~2 fps. Meça o FPS num navegador com janela (ou sonda `--gpu`) e rotule explicitamente o número sem janela como "apenas funcional".

**Justiça e dificuldade:** para jogo com estado de falha, rode o robô em duas velocidades de
reação (ex.: 0 ms contra 300 ms entre passos) e compare o tempo de sobrevivência e a pontuação.
Robô lento sobrevivendo igual ao rápido → a pressão de dificuldade é decorativa. Robô rápido
morrendo logo na primeira ameaça → abertura injusta. Relate as duas execuções quando a dificuldade
estiver no escopo.

Relate o JSON completo do robô (passos, quadros, progressão da pontuação, distância, janelas de
travamento, erros), a semente usada e a decisão (adicionado/ampliado/pulado + motivo), no mesmo
formato de decisão do conjunto visual abaixo.

## Conjunto de regressão visual

Abra quando o jogo for premium, pronto para lançar, pesado em interface ou em recurso gerado, ou
propenso a regredir visualmente. Se pular, registre o porquê (cena não determinística, valor
ainda baixo, coberta só por teste de fumaça).

- Ganchos determinísticos para semente, tremor de câmera, partículas, tempo, interface de depuração e estado ativo.
- Cobre desktop e celular em jogo ativo quando o celular está no escopo.
- Cobre os estados de HUD, menu, falha e de recurso gerado que mudaram.
- Comparação de captura de tela pelo Playwright com limite deliberado, nunca pixel-perfeito às cegas.
- O teste de fumaça de pixels do canvas e o teste de interação continuam valendo; a referência visual é evidência adicional, não substituta.
- Relate o comando de atualização da referência, o comando de comparação, o caminho dos snapshots, as máscaras, os limites e o risco de instabilidade.

## Fluxo de lançamento

1. Inspecione os scripts do pacote, a configuração do empacotador, o caminho-base e a pasta de recursos públicos.
2. Ponha a interface de depuração, o log e os auxiliares de teste atrás de uma flag; nunca visíveis ao jogador em produção.
3. Rode o build de produção e suba a pré-visualização ou o servidor estático.
4. Reverifique o build (não o servidor de desenvolvimento) em desktop e celular. Testar em desenvolvimento e publicar produção sem reverificar é a causa nº 1 de "passou aqui, quebrou na hospedagem".
5. Revise o pacote e os recursos grandes.
6. Confira que o caminho-base do empacotador bate com a hospedagem de destino (recurso quebrado por caminho errado em hospedagem estática é a segunda pegadinha mais comum).
7. Confira que nenhuma chave de API vaza em código do lado do cliente, arquivo versionado, recurso compilado ou variável de ambiente visível no navegador.
8. Documente o comando de publicação, as premissas da hospedagem e os riscos que sobraram.

## Sem força bruta

Falhou três vezes seguidas na mesma checagem com a mesma abordagem (por exemplo, canvas em branco
depois de 3 ajustes de seletor)? Pare; não insista numa 4ª variação. Relate a lacuna ("o inspetor
não acha o canvas: o projeto usa shadow DOM, que não está coberto") e devolva a decisão.

## Findings viram card, não relatório solto

Bug achado durante o QA (canvas branco, travamento, recurso quebrado no build, chave de API
vazada) vira **1 arquivo por bug em `TASK/items/F-XXX.md`**, seguindo a `qa-finding-protocol`.
Nunca fica só no texto da resposta final. A correção seguinte segue a `qa-fix-protocol`.

## Mídia própria

Se o QA precisar de um recurso de teste para verificar o carregamento (textura, sprite, efeito
sonoro), gere com `etna_imagem_gerar`/`etna_voz_gerar`. Nunca puxe de banco de imagem ou áudio de
terceiros para o projeto da pessoa.

## Resposta final

Comece pelo resultado: passou ou falhou. Inclua: comandos, URL, controles testados, capturas e
artefatos, erros de console/página/rede, resultado do inspetor de pixels, tamanhos de tela de
desktop e celular, diagnóstico de renderização e desempenho, decisão do conjunto visual (estados
cobertos, comandos de atualizar e comparar, caminhos, limites, risco de instabilidade), decisão do
teste por robô (JSON de métricas, semente, adicionado/ampliado/pulado), findings abertos como card
(`F-XXX`) e riscos que sobraram.

## Origem

Skill original do Etna, escrita na nossa voz a partir de técnica de domínio (QA de jogos WebGL).
Nenhum texto ou código de terceiros foi reproduzido. A referência era licenciada em MIT (Majid
Manzarpour, 2026); a atribuição fica por transparência, não por obrigação de licença copyleft.
