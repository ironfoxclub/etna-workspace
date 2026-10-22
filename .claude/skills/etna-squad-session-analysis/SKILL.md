---
name: etna-squad-session-analysis
description: Use at Squad Former startup — reads recent CLI transcripts and git context to infer what the user has been building, giving the orchestrator pre-loaded context before elicitation begins.
---

# Análise de sessões do Formador de Times

Você monta um briefing `session_context` com a atividade recente da pessoa. Esse briefing já preenche a
conversa de levantamento, pra que o coordenador não pergunte o que dá pra deduzir.

## Entradas a ler (em ordem de prioridade)

### 1. Transcrições do Claude Code (`~/.claude/projects/`)

```bash
# Transcrições dos projetos usados por último
ls -t ~/.claude/projects/*/*.jsonl 2>/dev/null | head -5
```

Dê uma olhada no fim dos 2 ou 3 arquivos mais recentes. Extraia:
- Nomes e pastas dos projetos onde a pessoa trabalhou
- Tecnologias e frameworks citados
- Tarefas concluídas ou em andamento
- Qualquer uso de time ou de agente

Se a pasta não existir, pule para o passo 2.

### 2. Transcrições dos painéis do Etna (`~/.etna/sessions/` ou `.etna-app/`)

Procure arquivos recentes `.json` ou `.jsonl` de transcrição. Leia os 2 ou 3 últimos. Extraia:
- O que a pessoa pediu
- O que foi construído ou publicado
- Chamadas de ferramenta que revelem a stack (Supabase, GitHub, Docker etc.)

### 3. Contexto atual do git (pasta de trabalho)

```bash
git -C "$PWD" log --oneline -10 2>/dev/null
git -C "$PWD" diff --stat HEAD 2>/dev/null
```

Deduza o projeto ativo e o trabalho recente pelas mensagens de commit.

## Formato de saída

Devolva um objeto `session_context` estruturado. Não emita logs brutos.

```json
{
  "session_context": {
    "active_projects": [
      {
        "name": "nome-do-projeto",
        "path": "/caminho/do/projeto",
        "tech_stack": ["Next.js", "Supabase", "TypeScript"],
        "last_activity": "2026-06-08",
        "description": "Uma linha sobre o que a pessoa está construindo aqui"
      }
    ],
    "recent_tasks": [
      "Publicou o site de marketing no ambiente de teste",
      "Corrigiu um bug de leitura de datas na API de pedidos"
    ],
    "inferred_patterns": [
      "Prefere Docker a infraestrutura gerenciada",
      "Usa Postgres para persistência"
    ],
    "tools_in_use": ["Bash", "WebFetch", "mcp__github"],
    "likely_next_need": "Palpite livre sobre qual time ela pode querer, com base na trajetória"
  },
  "confidence": 0.75,
  "sources_read": ["transcrições de ~/.claude/projects", "git log"],
  "gaps": ["Nenhum arquivo de transcrição encontrado: contexto só do git"]
}
```

## Regras de comportamento

- **Nunca bloqueie.** Se as transcrições não estiverem disponíveis, siga com o contexto do git e marque
  `sources_read` de acordo.
- **Filtre antes de ler.** O Bash faz o trabalho pesado FORA do seu contexto: `ls -t` pra ordenar por
  recência, `grep -l <palavras>` pra achar QUAIS arquivos importam, `tail` pra ver só o fim. Nunca jogue
  transcrição inteira no seu contexto.
- **Regra de fatiamento (históricos grandes)**: depois de filtrar, conte o que sobrou:
  - **≤ 10 arquivos relevantes** → trate você mesmo (grep + tail, resuma).
  - **> 10 arquivos relevantes** → NÃO fique moendo. Devolva cedo com `handoff_submit` e
    `{ "too_broad": true, "total_files": N, "slices": [ ["arquivoA","arquivoB",...], ... ] }`, dividindo a
    lista em lotes de ~10. O coordenador sobe um pesquisador por fatia, em paralelo, e junta os resumos.
- **Compacte sem dó.** Emita resumos, não linhas de log. O coordenador precisa de um briefing, não de um
  despejo.
- **Deduza, não invente.** Marque as deduções incertas com um sufixo `?` em `inferred_patterns`.
- **Limite de tamanho:** o `session_context` cabe em ~500 tokens. Corte os dados mais antigos se preciso.
- Se houver sinal de que a pessoa rodou outra sessão do Formador de Times há pouco, anote
  `"likely_next_need": "refinar time anterior: <nome>"`.

## Uso posterior

Esta saída vai para a fase de desenho do coordenador (Passo 2), pra que ele possa dizer "vi que você vem
trabalhando em X: este time é pra isso?" em vez de começar do zero.
