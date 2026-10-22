---
name: video-ref-claude-animacao
description: "Referência de vídeo com IA (categoria Vídeo). Kit de partida em p5.js + p5.brush para animar um personagem (Clawd, 31 expressões) em vídeo de 15 s com storyboard e render para mp4. Use para pedidos de animação de personagem desenhado à mão."
---

# video-ref-claude-animacao

Skill de uso do repositório [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) (licença: MIT). Ela diz quando usar, quais arquivos ler para cada tipo de pedido e traz o resumo do catálogo.

## Qual arquivo ler para cada pedido

| Pedido | O que fazer |
|---|---|
| Qualquer animação de personagem | leia `ANIMATION_GUIDE.md` inteiro antes (antecipação, overshoot, uma linha de história, emoções via `emotions()`, giros via `turn()`) |
| Rodar/renderizar | `render.mjs` e `README.md` (precisa de Node, Chrome e ffmpeg; sem GPU o render é lento) |
| Ver expressões disponíveis | `docs/emotions.jpg` (as 31 expressões) e `docs/views.jpg` |

## Resumo do catálogo

- `src/clawd.js` (personagem), `core.js` (motor), `timeline.js` (linha do tempo), `sheets.js`, `config.js`.
- `studio.html` abre o estúdio de preview; `gpu_probe.mjs` testa a GPU.
- Fluxo do repositório: storyboard primeiro, depois plano por cena, folha de contatos para conferir, e `out/video.mp4`.
- Pedido-modelo: "Leia ANIMATION_GUIDE.md e faça um vídeo de 15 s do Clawd tentando pegar uma borboleta".

## Como usar

1. **Pegue o repositório.** Procure a pasta de cache `~/video-ia/ClaudeAnimationBase`. Se não existir, clone: `git clone --depth 1 https://github.com/JohnHeibel/ClaudeAnimationBase.git ~/video-ia/ClaudeAnimationBase` (se o git não estiver instalado, avise o usuário em vez de instalar). Se já existir, use como está.
2. **Leia só o que o pedido precisa**, conforme a tabela acima. Não leia o repositório inteiro.
3. Não rode scripts de instalação ou de render do repositório sem ler antes e sem avisar o usuário (é código de terceiros).
4. Licença: MIT. Pode adaptar prompt e código ao trabalho do usuário, mantendo o crédito do autor e a licença.

**Atenção:** O personagem Clawd é da Anthropic: para outro personagem, troque `src/clawd.js` por um novo e mantenha as regras do guia.
