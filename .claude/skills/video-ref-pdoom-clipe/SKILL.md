---
name: video-ref-pdoom-clipe
description: "Referência de vídeo com IA (categoria Vídeo). Projeto completo de clipe com letra sincronizada palavra a palavra (estilo karaokê), 4K 60fps, em TypeScript + three.js. Use como modelo para um lyric video: alinhamento de letra, análise de batida e renderizador."
---

# video-ref-pdoom-clipe

Skill-índice: o repositório é um projeto de exemplo, não uma skill pronta. Ela só diz quando usar e onde ler.

- **Repositório:** https://github.com/mexicat/pdoom-video
- **Licença:** MIT
- **Categoria:** Vídeo

## Quando usar

Projeto completo de clipe com letra sincronizada palavra a palavra (estilo karaokê), 4K 60fps, em TypeScript + three.js. Use como modelo para um lyric video: alinhamento de letra, análise de batida e renderizador.

## Como usar

1. Veja se já existe um clone em `~/video-ia/pdoom-video`. Se não, clone raso: `git clone --depth 1 https://github.com/mexicat/pdoom-video.git ~/video-ia/pdoom-video`.
2. Leia só o que precisa: `docs/TREATMENT.md` (conceito), `docs/ENGINE.md` (API do renderizador), `analysis/` (alinhamento e batidas em Python), `app/` (renderizador, bun + Vite), `data/lyrics.json` e `data/audio.json` (formato dos tempos). O áudio da música é de terceiros: não reutilize.
3. Não rode scripts de instalação ou de render do repositório sem ler antes e sem avisar o usuário (é código de terceiros).
4. Respeite a licença acima ao reaproveitar prompt ou código em material entregue; cite a fonte.
