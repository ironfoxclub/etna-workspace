---
name: video-ref-mg-styles-15
description: "Referência de vídeo com IA (categoria Vídeo). 15 estilos de motion graphics de 10 s, cada um com prompt completo e código-fonte. Use quando pedirem um vídeo de motion design num estilo visual (flat, line art, isométrico, 3D, colagem, líquido, bauhaus, synthwave, pixel, HUD...) e para reaproveitar o prompt."
---

# video-ref-mg-styles-15

Skill de uso do repositório [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) (licença: MIT). Ela diz quando usar, quais arquivos ler para cada tipo de pedido e traz o resumo do catálogo.

## Qual arquivo ler para cada pedido

| Pedido | O que fazer |
|---|---|
| Escolher/mostrar estilos | liste a tabela abaixo; leia só o `prompts/<estilo>.md` escolhido |
| Fazer um vídeo de 10 s num estilo | leia `prompts/<estilo>.md` (prompt completo) e `demos/<estilo>/index.html` (código que o gerou); adapte tema e cores ao pedido |
| Revisar o resultado | aplique `rubric.md` (critérios) antes de entregar |
| Estrutura de um prompt novo | copie o molde de `template.md` |

## Resumo do catálogo

| Arquivo em `prompts/` | Estilo |
|---|---|
| 01-flat-vector | vetor chapado |
| 02-line-art | traço/linha |
| 03-isometric | isométrico |
| 04-3d-render | render 3D |
| 05-cel-boil | cel animation "boil" |
| 06-collage | colagem |
| 07-liquid | líquido |
| 08-morph | morph |
| 09-bauhaus | bauhaus |
| 10-synthwave | synthwave |
| 12-aurora-glass | vidro aurora |
| 18-hanazi | hanazi |
| 19-paperclip | clipes de papel |
| 20-pixel | pixel art |
| 22-hud | HUD/interface |

Cada `demos/<estilo>/` tem `index.html` (a animação), `cues.json` e `audio.py` (som). Não use `videos/` (mais de 1 GB de vídeo pronto).

## Como usar

1. **Pegue o repositório.** Procure a pasta de cache `~/video-ia/mg-styles-15`. Se não existir, clone: `git clone --depth 1 --filter=blob:none https://github.com/Vincentwei1021/mg-styles-15.git ~/video-ia/mg-styles-15` (se o git não estiver instalado, avise o usuário em vez de instalar). Se já existir, use como está.
2. **Leia só o que o pedido precisa**, conforme a tabela acima. Não leia o repositório inteiro.
3. Não rode scripts de instalação ou de render do repositório sem ler antes e sem avisar o usuário (é código de terceiros).
4. Licença: MIT. Pode adaptar prompt e código ao trabalho do usuário, mantendo o crédito do autor e a licença.

**Atenção:** O clone é grande (1,2 GB com vídeos). Na versão sob demanda o clone usa `--filter=blob:none`: leia só `prompts/`, `demos/`, `rubric.md` e `template.md`.
