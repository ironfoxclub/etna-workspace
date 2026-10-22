---
name: video-ref-pdoom-john
description: "Referência de vídeo com IA (categoria Vídeo). Outro clipe musical animado (personagem Clawd, palco de teatro que sai dos trilhos), com storyboard e guia de animação. Use só como estudo de storyboard e ritmo de clipe; o repositório não tem licença."
---

# video-ref-pdoom-john

Skill de uso do repositório [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) (licença: sem licença (todos os direitos reservados)). Ela diz quando usar, quais arquivos ler para cada tipo de pedido e traz o resumo do catálogo.

## Qual arquivo ler para cada pedido

| Pedido | O que fazer |
|---|---|
| Aprender a estruturar o clipe | `STORYBOARD.md` (ideia, elenco, regra 'em todo plano algo acontece', piadas só com imagem) |
| Regras de animação | `ANIMATION_GUIDE.md` |
| Ver como o código organiza cena | `src/` (timeline.js, cast.js, props.js, lyrics.js), só leitura |

## Resumo do catálogo

- Conceito: cortina de teatro pintada abre e fecha; entre as duas, a IA cresce de rabisco a planeta; texto mínimo, efeitos sonoros curtos (FOOM, BOOM, CHOMP).
- `render.mjs` + `studio.html` renderizam; `assets/pdoom.mp3` é a música; `legacy/` guarda versão antiga.

## Como usar

1. **Pegue o repositório.** Procure a pasta de cache `~/video-ia/PDoomVideo`. Se não existir, clone: `git clone --depth 1 https://github.com/JohnHeibel/PDoomVideo.git ~/video-ia/PDoomVideo` (se o git não estiver instalado, avise o usuário em vez de instalar). Se já existir, use como está.
2. **Leia só o que o pedido precisa**, conforme a tabela acima. Não leia o repositório inteiro.
3. Não rode scripts de instalação ou de render do repositório sem ler antes e sem avisar o usuário (é código de terceiros).
4. **Licença: sem licença (todos os direitos reservados).** Não copie código, prompt nem texto deste repositório para material entregue nem para dentro de projetos do usuário: leia, entenda a técnica e escreva o seu.

**Atenção:** SEM LICENÇA: leia para aprender a técnica e escreva o seu próprio roteiro e código. Para clipe com licença, use `video-ref-pdoom-clipe` ou `video-ref-claude-animacao` (MIT).
