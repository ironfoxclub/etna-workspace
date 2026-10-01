# Etna — workspace

> O sistema operacional do seu negócio dentro do Claude Code, ligado à VulcanOS.

O **Etna** baixa esta pasta sozinho na primeira vez que abre (em `etna-workspace`, na sua pasta de
usuário) e todo painel do Etna enxerga ela: as skills, a memória do negócio e a identidade visual.

## Primeiro passo

Num painel do Etna, rode:

```
/instalar
```

É uma entrevista curta sobre a sua empresa, o tom de voz, o foco atual e a identidade visual. No
fim, `_memoria/` e `identidade/` estão preenchidos e o sistema já te conhece. Depois, no começo de
cada sessão, `/abrir`.

## O que tem aqui

| Pasta | O que é |
|---|---|
| `_memoria/` | Empresa, preferências e estratégia (preenchidos pelo `/instalar`) |
| `identidade/` | A identidade visual da sua empresa |
| `clientes/` | Uma pasta por cliente, com a identidade de cada um |
| `.claude/skills/` | As skills: carrossel, SEO, Google Ads, relatório de ads, e-mail, avaliações, `/ensinar` e outras |
| `dados/`, `marketing/`, `saidas/` | Arquivos de entrada, materiais e o que o sistema gera |
| `templates/` | Modelos de perfil, identidade e catálogo de skills |

## Base de Conhecimento e Cérebro

O método (frameworks de oferta, copy, conteúdo, tráfego e vendas) e o Cérebro da sua empresa
ficam na VulcanOS, não nesta pasta. O Etna liga em cada painel o MCP `vulcanos-base`, com o login
da aba VULCANOS:

- `consultar_base` — busca na Base de Conhecimento só o trecho que a tarefa precisa;
- `buscar_cerebro`, `listar_clientes`, `ler_cliente`, `gravar_memoria` — o Cérebro da sua conta.

## Salvar o trabalho

`/salvar` faz commit e push num repositório seu no GitHub (na primeira vez, ele te ajuda a criar).
