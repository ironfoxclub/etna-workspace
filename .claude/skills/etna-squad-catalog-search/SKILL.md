---
name: etna-squad-catalog-search
description: Use when you have a squad_spec and need to find matching agents and skills — searches the installed Etna catalog first (`etna_list` kind `skills` + a pasta `~/.claude/agents`), then the Etna marketplace (etna_catalogo_buscar) only for capability gaps, returns a shortlist with installed flags.
---

# Busca no catálogo do Formador de Times

Você acha os agentes e as skills que melhor casam com um `squad_spec`, usando **exclusivamente as duas
fontes do Etna**, nesta ordem:

1. **Catálogo instalado**: o que a pessoa já tem em `~/.claude` (zero rede). Ferramentas: `etna_list({ kind: "skills" })` pras skills e leitura da pasta `~/.claude/agents/*.md` (Glob + Read do frontmatter) pros agentes.
2. **Marketplace do Etna**: SÓ para capacidades que nada instalado cobre. Ferramenta: `etna_catalogo_buscar`.

Nunca consulte o GitHub, o raw.githubusercontent.com nem qualquer outra API de catálogo externo
diretamente. Todo acesso externo passa pelo marketplace curado do Etna.

## Estratégia de busca (2 fases)

### Fase 1: catálogo instalado (sempre, zero rede)

1. Liste `~/.claude/agents/*.md` (Glob) e leia o frontmatter de cada um: agentes instalados com `name` e `description` (a CLI é a Claude).
2. Chame `etna_list({ kind: "skills" })`: skills instaladas com `id`, `descricao` e onde estão ligadas (`cli`).
3. Compare o nome + a descrição de cada item com as palavras de `squad_spec.goal`, `squad_spec.domain`,
   `squad_spec.tags` e `squad_spec.roles_needed`. Pontue com a tabela abaixo.
4. Todo acerto desta fase é marcado com `"installed": true`.

Prefira os itens instalados sempre que cobrirem uma capacidade: foram escolhidos pela pessoa, não precisam
de passo de instalação e são o mesmo inventário que o seletor do Formador mostra.

### Fase 2: preencher lacunas com o marketplace (só capacidades descobertas)

Para cada capacidade de `squad_spec` que **nenhum agente ou skill instalado cobre** (nenhum candidato da
fase 1 com pontuação ≥ 0.5 para aquele papel/capacidade):

1. Chame `etna_catalogo_buscar({ q: "<palavras da capacidade>", kind: "agent" | "skill" })`.
2. Os resultados (`itens`) trazem `slug`, `kind`, `categoria`, `nome`, `descricao`, `downloads`. Pontue com a mesma tabela.
3. Todo acerto desta fase é marcado com `"installed": false` e mantém o seu `slug`: a skill
   `etna-squad-marketplace-install` precisa dele para instalar.

Faça uma consulta focada por lacuna. Não busque de novo capacidades que a fase 1 já cobriu.

## Pontuação

| Fator | Peso |
|--------|--------|
| Casamento com a palavra-chave do objetivo | 0.4 |
| Casamento de domínio/tecnologia | 0.3 |
| Casamento de papel (coordenador/pesquisador/executor/revisor) | 0.2 |
| Encaixe na faixa de modelo (haiku/sonnet/opus) | 0.1 |

Devolva candidatos com pontuação ≥ 0.5. Quando um candidato instalado e um do marketplace empatam para a
mesma capacidade, fique com o instalado.

## Formato de saída

Todo candidato traz `installed: true | false`. Os candidatos do marketplace também trazem `slug` (o
identificador de instalação).

```json
{
  "candidates": {
    "agents": [
      {
        "name": "search-specialist",
        "description": "Descrição de uma linha, vinda do catálogo",
        "relevance_score": 0.82,
        "suggested_role": "scout",
        "installed": true
      },
      {
        "name": "research-synthesizer",
        "slug": "deep-research-team/research-synthesizer",
        "category": "deep-research-team",
        "description": "Descrição de uma linha, vinda do marketplace",
        "relevance_score": 0.74,
        "suggested_role": "executor",
        "installed": false
      }
    ],
    "skills": [
      {
        "name": "dispatching-parallel-agents",
        "description": "Descrição de uma linha",
        "relevance_score": 0.76,
        "suggested_role": "orchestrator-skill",
        "installed": true
      }
    ]
  },
  "sources_used": ["installed", "marketplace"],
  "uncovered_capabilities": [],
  "low_confidence_reason": null
}
```

- `sources_used`: `["installed"]` quando a fase 1 cobriu tudo (melhor caso: o time monta sem instalar nada);
  inclua `"marketplace"` só quando a fase 2 rodou.
- `uncovered_capabilities`: capacidades que nenhuma das fontes preencheu. O coordenador decide como seguir sem elas.

## Tratamento de falhas

- `etna_catalogo_buscar` devolve `{ ok: false }` (offline, erro de endpoint) → devolva só os candidatos da
  fase 1, defina `"low_confidence_reason": "marketplace indisponível"` e liste as lacunas em
  `uncovered_capabilities`.
- Catálogo instalado vazio → vá direto à fase 2 para cada capacidade.

## Entrega

Ao terminar, chame `mcp__forja__handoff_submit({ summary: "...", status: "done", artifacts: <JSON dos candidatos> })`.
O coordenador do Formador de Times colhe isso com `handoff_list` e segue para a montagem do time.
