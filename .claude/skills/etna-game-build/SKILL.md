---
name: etna-game-build
description: "Constrói um jogo jogável de navegador com Three.js/Vite do zero até a primeira fatia jogável: estrutura do projeto, laço do jogo, entidades, entrada, câmera, colisão/física, desenho de fase e encontro, e 'juice' (hitstop, tremor de tela, achatamento e esticada, chute de câmera). Use para protótipo de jogo novo, para acrescentar mecânica a um laço existente, para ajustar a sensação do jogo ou para revisar se uma construção é 'de fato um jogo' ou só uma demo estática. NÃO use para visuais 3D sem interação (hero com rolagem, render de produto): isso é etna-site-scrub/etna-cinema-shot. Também não serve para jogo 2D em canvas sem Three.js."
---

# etna-game-build

## Doutrina central

Um jogo só é jogo quando prova o laço com entrada real: verbo → objetivo → pressão →
recompensa/progressão → falha/nova tentativa. Renderizar uma cena bonita não é gameplay. Antes de
escrever qualquer mecânica, escreva o contrato do laço:

```
O jogador faz [verbo] para atingir [objetivo] enquanto [pressão] cria risco;
o sucesso dá [recompensa/progressão], a falha causa [custo/nova tentativa].
```

Rejeite sem dó: "explorar uma cena legal" não é briefing de design. Falta decisão de verdade na
primeira janela de jogo. Falta pressão até o primeiro minuto jogável.

## Doutrina embutida (sem arquivos de referência separados)

Esta skill não tem `references/`: arquitetura, desenho de fase, escolha de física e juice estão
todos nas seções abaixo. Antes de dar a fase de gameplay por concluída, confirme que consultou:
"Desenho de fase e encontro" (jogo novo ou mudança grande de mecânica), "Colisão e física"
(física, colisão, veículo, bola, pinball, sensores) e "Juice" (ajuste de sensação e impacto).
Registre no relatório final quais seções aplicou (sim/não, com o motivo se pulou). Não declare o
gameplay pronto pulando uma seção obrigatória para o seu caso.

## Estrutura inicial

Se pedirem um jogo novo do zero, use `scripts/scaffold_game.py <destino>` (se existir na pasta da
skill) ou monte à mão: Vite + TypeScript + Three.js, com `src/{core,game,entities,systems,assets,ui,tests}`.
Nunca entregue um jogo sem laço de atualização, sem entrada real, sem tela de recomeço: reprova
no portão abaixo.

## Ciclo de implementação (por mecânica)

1. Estado e dados.
2. Simulação e atualização.
3. Representação visual.
4. Retorno ao jogador: interface, áudio, efeitos, câmera, animação.
5. Diagnóstico.
6. Verificar com entrada real + 1 caso de borda que deveria falhar.

Exemplos de forma (ajuste os nomes ao jogo real): coletável = surgir → gatilho de colisão → estado
de pontuação ou medidor → efeito e áudio de coleta → pulso no HUD → reaparecer ou limpar.
Obstáculo = aviso → movimento → colisor simplificado → estado de dano ou falha → retorno do acerto
→ recomeço. Habilidade com recarga = recarga → projétil/acerto → retorno do impacto → interface de
munição ou carga → legibilidade do alvo.

## Arquitetura mínima

Não invente camada antes de a mecânica pedir. Extraia a duplicação de entidade, entrada ou
colisão só quando 2 ou mais funções já compartilham a lógica.

```
entrada → física fixa (se houver) → sistemas de gameplay → animação/efeitos → câmera → ponte com a interface → render
```

## Colisão e física: escada de escolha

1. **Colisão própria** (padrão): gatilhos de arcade, faixas, corredores infinitos, itens, projéteis simples.
2. **Rapier** (`@dimforge/rapier3d-compat`): bolas, pinball, minigolfe, plataformas móveis, sensores, corpos rígidos, colisões em alta velocidade. É a escolha robusta padrão para física séria no navegador.
3. **cannon-es**: plano B leve em JS quando não se quer WASM e a cena é simples.

Regras inegociáveis: colisor simples, nunca a malha visual detalhada; delta limitado ou passo
fixo na física; sincronizar a transformação física ↔ visual em um único sistema; detecção
contínua de colisão (CCD) só em corpos rápidos (custa caro); descartar corpos e colisores no
recomeço, porque corpo fantasma sobrevivendo ao recomeço é um bug clássico de QA.

## Desenho de fase e encontro: contrato mínimo

Antes de construir pista, arena, mapa, onda ou quebra-cabeça: formato do espaço, contrato da
câmera (o que pode e o que não pode mostrar), ponto de partida + primeira decisão + primeira
ameaça + primeira recompensa, zona de aprendizado, rota principal + rota de risco opcional,
escalada a cada 20-60 s, pontos de respiro e legibilidade da falha (aviso antes do golpe).

Primeiro o protótipo cinza: formas simples provam escala, rota, ritmo e colisão antes de gastar
com arte.

Testes de rejeição de diversão: se qualquer um for verdadeiro, itere antes de polir:
- Nenhuma decisão real nos primeiros 30 s.
- Dá pra ignorar a mecânica principal e mesmo assim progredir.
- A falha vem antes de o jogador entender o porquê.
- A dificuldade é só "mais coisas", nunca combinações melhores.
- O espaço é decorativo e não molda decisão.

## Juice: sensação é comunicação de estado, não enfeite

Ordem de aplicação (cada camada depende da anterior): latência de entrada (<100 ms no verbo
principal; resolva isso ANTES de qualquer polimento) → curvas de resposta (aceleração e suavização
no próprio movimento) → retorno de contato (flash, achatamento, hitstop, tremor no instante do
impacto) → câmera (tremor, chute e FOV que amplificam sem esconder o campo de jogo) → sincronia
entre áudio e imagem (som no mesmo quadro do visual, com variação de tom e volume).

Regra de legibilidade: se o efeito esconde a próxima decisão do jogador, é bug, não polimento.

**Toda aleatoriedade de gameplay ou efeito passa por gerador com semente** (nunca `Math.random`):
isso quebra os ganchos de teste determinístico e as referências de captura de tela. Efeitos
baseados em tempo (ruído do tremor, deriva do ambiente) usam o tempo de jogo acumulado, nunca
`performance.now()`/`Date.now()`.

Receitas prontas (ajuste os nomes de variável ao seu código; a técnica é a mesma):

- **Tremor por trauma:** tremor = `trauma²` (evento pequeno quase não mexe a câmera; grande bate forte), queda linear por segundo, teto em 1.0. Trauma recomendado: coleta 0.15, acerto 0.4, explosão 0.7.
- **Hitstop:** reduz só o `delta` de gameplay, nunca o laço de desenho; o quadro continua sendo desenhado, senão o congelamento fica invisível. De 60 a 90 ms na escala 0.05 em acertos pesados; nunca em eventos menores (vira travada, não peso).
- **Achatar e esticar:** ao deformar um eixo por `s`, contra-escale os outros dois por `1/√s` para preservar o volume. Ultrapassagem com curva tipo `easeOutBack` dá o "assentar" elástico.
- **Soco de FOV:** pico aditivo de FOV com queda exponencial (constante de tempo de ~200 ms); chame sempre `updateProjectionMatrix()` depois, porque esquecer isso deixa o FOV visualmente parado.
- **Flash de impacto:** pulse a `emissiveIntensity` do material atingido e volte ao valor base com tween; o `emissive` do material precisa ser diferente de preto, senão o pulso não aparece.
- **Vibração de controle:** detecte `vibrationActuator`; o `playEffect` pode ser rejeitado em hardware sem suporte, então engula a promise.
- **Áudio:** varie o tom a cada reprodução (±5-6%) para evitar o efeito "metralhadora" do mesmo som repetido; baixe o volume do ambiente durante o hitstop para o impacto se destacar.

Tabela de evento → pilha de retorno (escale a intensidade com a do evento): coleta = estalo +
pulso no HUD + som com tom variado + trauma leve; acerto no jogador = hitstop + trauma médio +
flash + vibração + pulso no HUD; explosão = hitstop maior + trauma alto + flash de tela inteira +
soco de FOV + vibração forte.

Maus hábitos: tremor constante sem queda (enjoa e esconde o campo); trauma sem curva quadrática
ou sem teto; hitstop em todo evento pequeno; retorno que bloqueia a entrada principal; efeito
guiado pelo relógio real ou pelo delta de gameplay já reduzido (dessincroniza durante o próprio
hitstop).

## Verificação (pirâmide de QA)

Nunca declare função de gameplay pronta sem, nesta ordem: `pnpm run build`/checagem de tipos →
foto do estado em texto (diagnóstico, `window.__GAME_DIAGNOSTICS__` ou equivalente) → captura de
tela só no veredito final. Rode sem janela sempre que der; captura de tela é o último recurso, não
o primeiro.

Checklist mínimo: build limpo, sem erro de console ou de página, canvas não vazio, 1 caminho de
entrada real testado, progressão do objetivo testada e falha/nova tentativa testada quando couber.

Bug achado pelo caminho → **1 arquivo `TASK/items/F-XXX.md`** (skill `qa-finding-protocol`),
nunca relatório solto nem lista no texto. Sem força bruta: no máximo 3 tentativas na mesma
abordagem de correção ou ajuste; na 3ª falha, mude de abordagem ou relate a lacuna de forma
explícita. Nunca itere a 10ª variação do mesmo ajuste.

## Falhas comuns (reprove se vir)

Demo estática no lugar de laço jogável. Fase decorativa que não molda decisão. Mecânica que
compila mas não responde à entrada real. Câmera que atrasa ou esconde a próxima decisão. Mudança
de estado que não mexe em interface, áudio ou efeitos. Abstração de arquitetura chegando antes de
a mecânica precisar dela. Corpo de física sobrevivendo ao recomeço.

## Mídia de apoio (sprites, texturas, interface)

Recurso visual que o jogo PRECISA gerar (sprite, textura, ícone do HUD) usa `etna_imagem_gerar`,
nunca banco de imagens nem link externo. Delegue à `etna-image-assets` quando o pedido for um
recurso simples e isolado (não cena cinematográfica, não sequência de rolagem).

## Relatório final

Relate: lista das referências carregadas, briefing de design, contrato do laço, plano de fase e
encontro, resultado do checklist de gameplay, comportamento observado, controles, arquivos
alterados, escolhas de arquitetura, constantes ajustadas, evidência de verificação e findings
abertos (com o ID do item).

## Origem

Skill original do Etna, escrita na nossa voz a partir de técnica de domínio público (padrões de
game design, física de jogos, sensação de jogo). Nenhum texto ou código de terceiros foi
reproduzido. Foi inspirada por uma skill MIT de terceiro (Majid Manzarpour) consultada como
referência de domínio, sem cópia de expressão.
