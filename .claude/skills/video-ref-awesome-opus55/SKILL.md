---
name: video-ref-awesome-opus55
description: "Referência de vídeo com IA (categoria Vídeo). 703 prompts reais de vídeos feitos com Claude Opus 5.5 em código (HTML, Canvas, SVG, Three.js, shaders), por categoria e técnica. Use para achar um prompt pronto parecido com o pedido (motion graphics, explicativo, 3D, interativo) e adaptar."
---

# video-ref-awesome-opus55

Skill de uso do repositório [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) (licença: MIT). Ela diz quando usar, quais arquivos ler para cada tipo de pedido e traz o resumo do catálogo.

## Qual arquivo ler para cada pedido

| Pedido | O que fazer |
|---|---|
| Achar prompts parecidos com o pedido | busque em `data/videos.json` (campos `category`, `tech_tags`, `prompt`) com Python; leia só os 2 ou 3 melhores |
| Ver o prompt inteiro de um vídeo | `prompts/<slug>.md` (o `slug` vem do `videos.json`) |
| Saber que técnica usar | veja os `tech_tags` abaixo e use a combinação do vídeo mais parecido |

## Resumo do catálogo

- **703 vídeos.** Categorias: `motion` (369), `3d` (117), `explainer` (116), `interactive` (101).
- **Técnicas (`tech_tags`):** canvas (267), svg (183), threejs (131), shader (92), gsap (86), css (57), audio (39), playable (22), particles (17), pixel (15), webgl (9), physics (9).
- Cada item do `videos.json`: `slug`, `author`, `post_url`, `category`, `tech_tags`, `prompt`, `prompt_partial`, `poster_url`.
- Busca rápida (rode dentro da pasta do repositório): `python -c "import json;d=json.load(open('data/videos.json',encoding='utf8'));print([x['slug'] for x in d if 'svg' in x['tech_tags'] and x['category']=='explainer'][:20])"`.

## Como usar

1. **Pegue o repositório.** Procure a pasta de cache `~/video-ia/awesome-opus5-5-videos`. Se não existir, clone: `git clone --depth 1 https://github.com/yihui-dev/awesome-opus5-5-videos.git ~/video-ia/awesome-opus5-5-videos` (se o git não estiver instalado, avise o usuário em vez de instalar). Se já existir, use como está.
2. **Leia só o que o pedido precisa**, conforme a tabela acima. Não leia o repositório inteiro.
3. Não rode scripts de instalação ou de render do repositório sem ler antes e sem avisar o usuário (é código de terceiros).
4. Licença: MIT. Pode adaptar prompt e código ao trabalho do usuário, mantendo o crédito do autor e a licença.

**Atenção:** Os prompts são de criadores diversos; o repositório é MIT, mas cite o autor (`author`) ao reaproveitar um prompt.
