---
name: video-ref-pdoom-clipe
description: "Referência de vídeo com IA (categoria Vídeo). Projeto completo de lyric video 4K 60 fps (TypeScript + three.js): letra sincronizada palavra a palavra, análise de batida, bíblia de estilo e motor de render. Use como modelo para clipe com letra, ou para sincronizar corte e efeito com a música."
---

# video-ref-pdoom-clipe

Skill de uso do repositório [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video) (licença: MIT). Ela diz quando usar, quais arquivos ler para cada tipo de pedido e traz o resumo do catálogo.

## Qual arquivo ler para cada pedido

| Pedido | O que fazer |
|---|---|
| Ideia, tom, paleta, regras de estilo | `docs/TREATMENT.md` (tratamento do clipe como bíblia de estilo) |
| Motor e API de cenas | `docs/ENGINE.md` |
| Sincronizar letra com áudio | `analysis/` (align.py, whisper_run.py, ctcalign.py) gera `data/lyrics.json`; `data/audio.json` traz as batidas |
| Código do vídeo | `app/` (Vite + three.js; `plates.json` lista as cenas) |

## Resumo do catálogo

- Estrutura: `analysis/` (Python: transcrição, alinhamento, análise de áudio), `app/` (renderizador), `audio/`, `lyrics/`, `data/`, `docs/`.
- Ideia do clipe: "pranchas de um tratado ilustrado" sobre o fim do mundo, cortes nas batidas, tipografia de alto contraste, regra "nada com cara de IA" (sem neon roxo/ciano, sem código Matrix).
- Princípio útil para qualquer clipe: mudanças grandes caem em cima da batida; em todo plano algo acontece.

## Como usar

1. **Pegue o repositório.** Procure a pasta de cache `~/video-ia/pdoom-video`. Se não existir, clone: `git clone --depth 1 https://github.com/mexicat/pdoom-video.git ~/video-ia/pdoom-video` (se o git não estiver instalado, avise o usuário em vez de instalar). Se já existir, use como está.
2. **Leia só o que o pedido precisa**, conforme a tabela acima. Não leia o repositório inteiro.
3. Não rode scripts de instalação ou de render do repositório sem ler antes e sem avisar o usuário (é código de terceiros).
4. Licença: MIT. Pode adaptar prompt e código ao trabalho do usuário, mantendo o crédito do autor e a licença.

**Atenção:** Não rode os scripts de `analysis/` nem o render sem ler antes: instalam dependências pesadas (uv, bun).
