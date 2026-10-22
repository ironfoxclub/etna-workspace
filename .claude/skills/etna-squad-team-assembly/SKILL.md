---
name: etna-squad-team-assembly
description: Use when you have a squad_spec and catalog candidates — maps them into a complete SquadPreset JSON ready for install and persist.
---

# Montagem do time (Formador de Times)

Você pega um `squad_spec` (vindo da fase de desenho do coordenador, Passo 2) e os `candidates` (vindos dos
painéis pesquisadores via `handoff_list`) e produz um `SquadPreset` JSON completo. É o time que a pessoa
vai ver na interface do Etna.

## Formato do SquadPreset (canônico)

```typescript
interface SquadPreset {
  id: string;                        // "<slug-do-objetivo>-<AAAA-MM-DD>"
  name: string;                      // Nome humano, ex.: "Time de Pesquisa"
  agents: AgentSlot[];
  createdAt: number;                 // Unix ms: Date.now()
  orchestratorInstructions: string;  // Adendo de sistema para o painel coordenador do time
  imageProvider?: string;            // 'openai-image' (gpt-image) | 'google-image' (nano-banana),
                                     // ambos via etna_imagem_gerar (chave de API em Configurações).
                                     // PREENCHA quando o time GERA imagens. Omita caso contrário.
  videoProvider?: string;            // 'seedance': só quando o time gera vídeo. Omita caso contrário.
  audioProvider?: string;            // 'elevenlabs': só quando o time gera fala/locução. Omita caso contrário.
}

interface AgentSlot {
  id: string;        // id do papel em kebab-case, ex.: "coordenador", "pesquisador-1", "sintetizador"
  agentName: string; // "etna-orchestrator" para o maestro; nome-base do agente do catálogo para os trabalhadores
  category: string;  // "orchestrator" | "scout" | "executor" | "reviewer"
  cli: string;       // uma CLI LIGADA nesta máquina: nunca presuma claude
  model: string;     // proposto a partir da lista de modelos do provedor daquela CLI (`etna_list` kind `models`): nunca inventado
  effort: string;    // "high" | "medium" | "low"
  allowedSkills?: string[]; // skills vinculadas A ESTE membro: omita quando não houver nenhuma
}
```

## Mapeamento de papéis

`etna-orchestrator` é o **único `agentName` canônico**. Os slots de trabalhador apontam para os nomes-base
dos agentes do catálogo: os instalados resolvem na hora; os candidatos do marketplace (`installed: false`)
resolvem depois que a `etna-squad-marketplace-install` roda `etna_catalogo_instalar` pra eles.

| Papel funcional | `agentName` | `effort` | Quantidade |
|----------------|-------------|----------|-------|
| Coordenador | `etna-orchestrator` (sempre) | `high` | 1 |
| Pesquisa / levantamento | agente do catálogo, ex.: `search-specialist` | `low` | 1–3 |
| Executor / construtor | agente do catálogo, ex.: `code-reviewer` | `medium` | 0–2 |
| Revisor / verificador | agente do catálogo, ex.: `research-synthesizer` | `medium` | 0–1 |

**Regra de CLI e modelo (OBRIGATÓRIA):** descubra o que esta máquina realmente roda antes de montar: chame
`mcp__forja__pane_list` e use só CLIs LIGADAS. Padronize o `cli` de cada membro para a CLI em que VOCÊ está
rodando (a pessoa escolheu ao abrir você ali); ofereça as outras CLIs ligadas como alternativas no portão de
prévia. NUNCA fixe claude no código.
`model`: PROPONHA um por membro, a partir da lista de modelos do provedor daquela CLI (a mesma ferramenta as
devolve): um modelo mais forte para o coordenador, um médio/barato para os trabalhadores. Nunca invente nome.

**Vínculo de skills (OBRIGATÓRIO):** cada skill escolhida vai no `allowedSkills` do(s) membro(s)
ESPECÍFICO(s) que vão usá-la: skills de design no designer, skills de QA no revisor. NUNCA apresente nem salve
skills como uma lista plana no nível do time. Um membro com skills vinculadas só consegue carregar ESSAS; um
membro sem nenhuma vinculada não tem restrição.

**Compatibilidade skill × CLI:** `etna_list({ kind: "skills" })` devolve o campo `cli` de cada skill (onde ela está
instalada). Vincular uma skill a um membro de OUTRA CLI é permitido: o runtime do Etna espelha a skill para a
pasta de skills daquela CLI automaticamente, na subida do membro. Quando isso acontecer, DIGA no portão de
prévia (ex.: "frontend-design (claude → espelhada para codex)") para a pessoa saber o mapeamento entre CLIs.

Sempre inclua exatamente 1 coordenador. Os trabalhadores vêm de `candidates.agents`, escolhendo o melhor
casamento por papel funcional, com base em `suggested_role` e `relevance_score`.

## Regras de montagem

1. Para cada papel em `squad_spec.roles_needed`, escolha o melhor agente de `candidates.agents` por
   `suggested_role` e `relevance_score`. Em empate, prefira candidatos com `installed: true`.
2. **Vincule skills por membro via `allowedSkills`**: para cada membro (inclusive o coordenador), coloque em
   `allowedSkills` os nomes de skills de `candidates.skills` que aquele papel efetivamente precisa. A lista
   preenchida é uma trava rígida em execução: o membro só carrega ESSAS skills. Membro sem skill vinculada:
   **omita o campo por completo** (omitido ou vazio = sem restrição). Nunca liste skills em prosa dentro do
   `orchestratorInstructions`.
3. Gere o `id` como `<slug-do-objetivo>-<AAAA-MM-DD>`.
4. Preencha o `orchestratorInstructions` a partir do **`orchestrator_playbook`** produzido na fase de desenho
   (Passo 2): pegue esse playbook abstrato por papel e FINALIZE: troque cada papel abstrato pelo `agentName`
   escolhido + skills vinculadas, e mantenha objetivo / método / ordem dos passos / portões / topologia. O
   modelo abaixo é o formato de reserva, para quando nenhum playbook foi rascunhado.
5. Monte o manifesto de instalação SOMENTE com os candidatos `installed: false`: os instalados não precisam de
   passo de instalação. Use o `slug` deles vindo da busca no marketplace.
6. **Recursos de mídia → membros de geração + provedores no preset.** Cada capacidade que a pessoa LIGOU em
   `squad_spec.media` vira DOIS itens: um campo de provedor no preset E um **membro de geração (AgentSlot) no
   elenco**, um trabalhador real e visível, não só uma flag. Adicione um membro por recurso ligado:
   - `media.image` → `imageProvider` + membro `id: "render-image"`, `category: "executor"`
   - `media.video` → `videoProvider` + membro `id: "render-video"`, `category: "executor"`
   - `media.audio` → `audioProvider` + membro `id: "render-audio"`, `category: "executor"`
   A CLI de um membro de geração é imposta pelo provedor (veja os nativos abaixo); provedores com chave podem
   rodar em qualquer CLI ligada. Cite-os no `orchestratorInstructions` (ex.: "render-image: gera os PNGs via …").
   Se um agente cumpre o próprio papel e também a geração (times pequenos), você PODE juntar o trabalho de
   geração num membro existente em vez de um slot separado, mas o campo de provedor SEMPRE é preenchido.

   Mapa de provedores: `media.image` → `imageProvider` (`openai-image` para gpt-image, `google-image` para
   nano-banana); `media.video` → `videoProvider` (`seedance`); `media.audio` → `audioProvider` (`elevenlabs`).
   Para `openai-image` / `google-image` / `seedance` / `elevenlabs`: a `etna_imagem_gerar` / `etna_video_gerar` /
   `etna_voz_gerar` do time formado herda o provedor, e a chave fica em Configurações › Suas IAs. O
   `orchestratorInstructions` TEM que mandar o agente de geração chamar a ferramenta certa (uma chamada por
   slot, com `outPath`), espelhando o playbook Absurd Landing. O agente de geração usa SÓ o provedor/modelo que
   a pessoa ligou nas Configurações; em caso de cota ou limite de taxa, tenta o MESMO provedor de novo (no
   máximo 2 vezes) e depois avisa a falta: nunca troca de motor em silêncio. Omita qualquer provedor de mídia
   que o time não usa.

## Modelo de orchestratorInstructions

```
Você está coordenando o time <nome do time>.

Objetivo: <squad_spec.goal>
Domínio: <squad_spec.domain>
Entregável: <squad_spec.deliverable>

## Equipe
- coordenador (você): etna-orchestrator
- <id>: <agentName>: <o que faz>
[repita por trabalhador]

## Fluxo
1. [Passo concreto 1]
2. [Passo concreto 2]
...

## Restrições
<de squad_spec.constraints>
Sob portão: <true|false>
```

As skills NÃO são enumeradas aqui: o vínculo vive no `allowedSkills` de cada membro, e o runtime injeta o que
cada membro pode carregar.

## Formato de saída

Exemplo concreto: um time de pesquisa com vínculo de skills por membro:

```json
{
  "preset": {
    "id": "time-pesquisa-profunda-2026-06-08",
    "name": "Time de Pesquisa Profunda",
    "agents": [
      {
        "id": "orchestrator",
        "agentName": "etna-orchestrator",
        "category": "orchestrator",
        "cli": "<uma CLI ligada, ex.: a em que você roda>",
        "effort": "high",
        "allowedSkills": ["dispatching-parallel-agents"]
      },
      {
        "id": "pesquisador-1",
        "agentName": "search-specialist",
        "category": "scout",
        "cli": "<uma CLI ligada>",
        "effort": "low",
        "allowedSkills": ["deep-research"]
      },
      {
        "id": "sintetizador",
        "agentName": "research-synthesizer",
        "category": "executor",
        "cli": "<uma CLI ligada>",
        "effort": "medium"
      }
    ],
    "createdAt": 1749340800000,
    "orchestratorInstructions": "Você está coordenando o Time de Pesquisa Profunda.\n\nObjetivo: Produzir um relatório de pesquisa com fontes citadas sobre um tema dado.\nDomínio: Pesquisa aberta na web\nEntregável: Relatório em Markdown estruturado, com fontes\n\n## Equipe\n- coordenador (você): etna-orchestrator\n- pesquisador-1: search-specialist: busca paralela na web em várias fontes\n- sintetizador: research-synthesizer: junta os achados no relatório final\n\n## Fluxo\n1. Dispare o pesquisador-1 em paralelo, por fatias do tema.\n2. Colete os achados com handoff_list.\n3. Delegue a síntese ao sintetizador.\n4. Devolva o relatório à pessoa.\n\n## Restrições\nSob portão: true"
  },
  "skills_to_install": [
    { "kind": "skill", "slug": "ai-research/deep-research" }
  ],
  "agents_to_install": [
    { "kind": "agent", "slug": "deep-research-team/research-synthesizer" }
  ]
}
```

> Neste exemplo, `search-specialist` e `dispatching-parallel-agents` estavam com `installed: true` (sem entrada de
> instalação); `research-synthesizer` e `deep-research` vieram do marketplace (`installed: false`) e por isso
> aparecem no manifesto. O `sintetizador` não tem skill vinculada, então `allowedSkills` foi omitido: ele fica
> sem restrição.

`skills_to_install` e `agents_to_install` formam o manifesto de instalação consumido pela
`etna-squad-marketplace-install`.

## Checagem de qualidade antes de emitir

- [ ] Exatamente 1 coordenador com `agentName: "etna-orchestrator"`?
- [ ] Nenhum trabalhador usa `"etna-scout"`, `"etna-executor"` ou `"etna-reviewer"`? Esses não existem.
- [ ] Todo `agentName` de trabalhador é um nome real de agente do catálogo, vindo de `candidates.agents`?
- [ ] O `allowedSkills` de cada membro traz só nomes de skills de `candidates.skills` vinculados àquele papel, e o campo está OMITIDO (não `[]`) nos membros sem skill?
- [ ] O `orchestratorInstructions` cita todo agente pelo `id` e NÃO enumera skills em prosa?
- [ ] O manifesto de instalação traz SOMENTE candidatos `installed: false`?
- [ ] O `id` é globalmente único (inclui a data)?
- [ ] O `createdAt` é número (Unix ms, `Date.now()`), não string ISO?
