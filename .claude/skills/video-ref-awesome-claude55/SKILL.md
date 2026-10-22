---
name: video-ref-awesome-claude55
description: "Referência de vídeo com IA (categoria Vídeo). Catálogo de ~420 vídeos feitos com Claude 5.5, com análise de estilos por domínio, briefing de produção e playbook de prompts. Use para estudar como um tipo de vídeo foi produzido, escolher o fluxo e montar o briefing."
---

# video-ref-awesome-claude55

Skill de uso do repositório [athemeroy/awesome-claude-5-5-videos](https://github.com/athemeroy/awesome-claude-5-5-videos) (licença: CC BY 4.0 (só o texto do repositório; vídeos e prompts de terceiros não)). Ela diz quando usar, quais arquivos ler para cada tipo de pedido e traz o resumo do catálogo.

## Qual arquivo ler para cada pedido

| Pedido | O que fazer |
|---|---|
| Planejar a produção de um vídeo | leia `docs/production-brief.md` e `docs/production-resources.md` |
| Escolher estilo por tipo de conteúdo | `docs/domain-style-atlas.md` e `docs/visual-effects-fit.md` |
| Cores e tratamento | `docs/color-modes.md` |
| Achar casos parecidos | `data/cases.csv` (colunas `source_url`, `primary_path`, `label`, `review_note`, `duration_s`) e `data/domain-style.csv`; filtre por `primary_path` |
| Estrutura do prompt | `docs/prompt-playbook.zh-CN.md` (em chinês: traduza ao ler) |

## Resumo do catálogo

- `data/cases.csv`: casos com origem, trilha principal (`primary_path`, ex.: `3d_or_realtime_graphics`), observação de revisão e duração.
- `docs/` (inglês, com versões `.zh-CN`): `library.md`, `research-guide.md`, `workflow-analysis.md`, `statistics.md`, `chart-generation.md`, `evidence-examples.md`.
- `docs/*.zh-CN.md` sem par em inglês: `prompt-playbook`, `prompt-matrix`, `methodology`.

## Como usar

1. **Pegue o repositório.** Procure a pasta de cache `~/video-ia/awesome-claude-5-5-videos`. Se não existir, clone: `git clone --depth 1 https://github.com/athemeroy/awesome-claude-5-5-videos.git ~/video-ia/awesome-claude-5-5-videos` (se o git não estiver instalado, avise o usuário em vez de instalar). Se já existir, use como está.
2. **Leia só o que o pedido precisa**, conforme a tabela acima. Não leia o repositório inteiro.
3. Não rode scripts de instalação ou de render do repositório sem ler antes e sem avisar o usuário (é código de terceiros).
4. Licença: CC BY 4.0 (só o texto do repositório; vídeos e prompts de terceiros não). Pode adaptar prompt e código ao trabalho do usuário, mantendo o crédito do autor e a licença.

**Atenção:** Licença CC BY 4.0 vale para o texto do repositório. Os vídeos e prompts citados são de terceiros: use como estudo e cite a fonte, não copie.
