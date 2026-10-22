---
name: video-ref-claude-animacao
description: "Referência de vídeo com IA (categoria Vídeo). Kit de partida para animar um personagem (31 expressões) em p5.js + p5.brush, com guia de regras para o modelo storyboardar, animar e renderizar. Use quando o pedido for animação de personagem desenhado à mão."
---

# video-ref-claude-animacao

Skill-índice: o repositório é um projeto de exemplo, não uma skill pronta. Ela só diz quando usar e onde ler.

- **Repositório:** https://github.com/JohnHeibel/ClaudeAnimationBase
- **Licença:** MIT
- **Categoria:** Vídeo

## Quando usar

Kit de partida para animar um personagem (31 expressões) em p5.js + p5.brush, com guia de regras para o modelo storyboardar, animar e renderizar. Use quando o pedido for animação de personagem desenhado à mão.

## Como usar

1. Veja se já existe um clone em `~/video-ia/ClaudeAnimationBase`. Se não, clone raso: `git clone --depth 1 https://github.com/JohnHeibel/ClaudeAnimationBase.git ~/video-ia/ClaudeAnimationBase`.
2. Leia só o que precisa: Leia `ANIMATION_GUIDE.md` primeiro; depois `src/` e `render.mjs`. Para renderizar precisa de Node.js, Chrome e ffmpeg (`npm install` e `node render.mjs --clip --out=out/video.mp4`: só rode depois de ler o `package.json`).
3. Não rode scripts de instalação ou de render do repositório sem ler antes e sem avisar o usuário (é código de terceiros).
4. Respeite a licença acima ao reaproveitar prompt ou código em material entregue; cite a fonte.
