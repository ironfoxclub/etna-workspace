---
name: video-ref-opus-prompts-zh
description: "Referência de vídeo com IA (categoria Vídeo). 18 prompts de vídeo em chinês para Claude Opus (lançamento de startup, motion showreel, explicativo, anúncio, zoom, loop de UI, jogo em Three.js...). Use para se inspirar na estrutura de prompts longos de vídeo; traduza ao ler."
---

# video-ref-opus-prompts-zh

Skill de uso do repositório [joeseesun/opus-video-prompts](https://github.com/joeseesun/opus-video-prompts) (licença: sem licença). Ela diz quando usar, quais arquivos ler para cada tipo de pedido e traz o resumo do catálogo.

## Qual arquivo ler para cada pedido

| Pedido | O que fazer |
|---|---|
| Lançamento/anúncio de produto | `prompts/01-inference-startup-launch.md`, `14-saas-launch-real-assets.md`, `16-high-end-product-video.md`, `12-remotion-app-promo-1.md`, `13-remotion-app-promo-2.md` |
| Explicativo | `05-transformer-explainer-js`, `07-business-explainer-30s`, `08-negroni-recipe-explainer`, `09-atmospheric-circulation-tts` |
| Showreel / estilo artístico | `02-motion-showreel-15s`, `03-china-5000-years-lineart`, `10-talking-head-to-lineart`, `15-ui-morph-loop` |
| Cinema / zoom / jogo | `04-opus-1984-ad`, `06-room-to-quarks-zoom`, `11-austerlitz-film`, `17-pixel-wizard`, `18-prehistoric-island-threejs` |

## Resumo do catálogo

Os 18 arquivos de `prompts/` são prompts completos em chinês; `cases.json` indexa os casos (autor, link). `README.md` explica a coleção.

## Como usar

1. **Pegue o repositório.** Procure a pasta de cache `~/video-ia/opus-video-prompts`. Se não existir, clone: `git clone --depth 1 https://github.com/joeseesun/opus-video-prompts.git ~/video-ia/opus-video-prompts` (se o git não estiver instalado, avise o usuário em vez de instalar). Se já existir, use como está.
2. **Leia só o que o pedido precisa**, conforme a tabela acima. Não leia o repositório inteiro.
3. Não rode scripts de instalação ou de render do repositório sem ler antes e sem avisar o usuário (é código de terceiros).
4. **Licença: sem licença.** Não copie código, prompt nem texto deste repositório para material entregue nem para dentro de projetos do usuário: leia, entenda a técnica e escreva o seu.

**Atenção:** SEM LICENÇA: use só para aprender o formato e escreva o seu prompt com palavras próprias.
