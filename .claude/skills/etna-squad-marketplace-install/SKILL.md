---
name: etna-squad-marketplace-install
description: Use when you have a completed SquadPreset and an install manifest — installs each marketplace component (source aitmpl) via etna_catalogo_instalar, then persists the squad via etna_time_salvar.
---

# Instalação do marketplace do Formador de Times

Você executa o manifesto de instalação produzido pela `etna-squad-team-assembly`: uma chamada de
`etna_catalogo_instalar` por componente e, no fim, uma chamada de `etna_time_salvar` para salvar o preset
completo.

## Formato do manifesto de instalação

Recebido da `etna-squad-team-assembly`:

```json
{
  "preset": { /* SquadPreset completo, com allowedSkills por membro (veja etna-squad-team-assembly) */ },
  "skills_to_install": [
    { "kind": "skill", "slug": "ai-research/deep-research" }
  ],
  "agents_to_install": [
    { "kind": "agent", "slug": "deep-research-team/research-synthesizer" }
  ]
}
```

O manifesto traz **só candidatos do marketplace** (`installed: false` na lista da
`etna-squad-catalog-search`). Candidatos já instalados (`installed: true`) nunca aparecem aqui: não
precisam de instalação. Se uma entrada do manifesto apontar para algo que já está no disco, a ferramenta
pula e devolve `skipped: true`.

## Procedimento de instalação

### Passo 1: instalar cada componente

Chame `etna_catalogo_instalar` para cada item de `skills_to_install` e `agents_to_install`:

```
etna_catalogo_instalar({
  kind: "skill",            // ou "agent"
  slug: "<categoria/nome>",  // slug do marketplace, ex.: "ai-research/deep-research"
  source: "aitmpl"
})
```

**Tratando as respostas:**
- `{ ok: true, installed: { name, path } }` → registre o sucesso e continue
- `{ ok: true, skipped: true }` → já estava instalado, pule sem alarde
- `{ ok: false, error: "..." }` → registre o erro e continue com as demais instalações (não aborte o lote inteiro)

**Ordem:** instale as skills antes dos agentes. As skills não dependem umas das outras; podem entrar em qualquer ordem.

### Passo 2: salvar o time

Depois que todas as instalações terminarem (mesmo com falhas parciais), chame:

```
etna_time_salvar(preset)
```

Em que `preset` é o objeto `SquadPreset` completo vindo da `etna-squad-team-assembly`, **incluindo o
`allowedSkills` de cada membro**. Não remova nem reescreva o campo: uma lista preenchida é a trava
rígida de execução daquele membro; campo omitido significa sem restrição. O preset salvo é a única fonte da
verdade para o vínculo de skills.

**Resposta:**
- `{ ok: true }` → o time já está no ar na interface do Etna
- `{ ok: false, error: "..." }` → informe o erro ao coordenador; NÃO tente de novo automaticamente

### Passo 3: emitir o relatório de instalação

Devolva um resumo estruturado ao coordenador:

```json
{
  "install_report": {
    "installed": [
      { "kind": "skill", "slug": "ai-research/deep-research", "path": "~/.claude/skills/deep-research/SKILL.md" }
    ],
    "skipped": [],
    "failed": [],
    "squad_saved": true,
    "squad_id": "deep-research-squad-2026-06-08",
    "squad_name": "Deep Research Squad",
    "allowed_skills_bound": {
      "orchestrator": ["dispatching-parallel-agents"],
      "researcher-1": ["deep-research"]
    }
  }
}
```

`allowed_skills_bound` espelha o `allowedSkills` de cada membro como ficou salvo. Membros sem o campo ficam de fora.

## Regras de segurança

- **Nunca sobrescreva.** O `skip-if-exists` é imposto pela ferramenta MCP (`skipped: true`). Não passe flag pra forçar sobrescrita.
- **Só slugs do manifesto.** Não aceite slug arbitrário que não esteja no manifesto de instalação. O manifesto foi validado pela `etna-squad-team-assembly` e traz só candidatos do marketplace com `installed: false`.
- **Não escreva direto em `~/.claude/`.** Toda escrita passa por `etna_catalogo_instalar`. Nunca use `cp`, `echo` ou `Write` no Bash para colocar arquivos na pasta `.claude` da pessoa.
- **Preserve o `allowedSkills`.** Passe o preset para `etna_time_salvar` exatamente como foi montado. Nunca acrescente skills que um membro não tinha, nem apague a lista de um membro.
- **Sucesso parcial é aceitável.** Uma skill que falhou não deve bloquear o salvamento do time. Relate as falhas e siga. Mas, se a skill vinculada a um membro falhou ao instalar, sinalize isso no relatório para o coordenador avisar a pessoa.

## Uso posterior

Depois que o `etna_time_salvar` devolver `{ ok: true }`, o time aparece na interface do Etna na hora. Volte
ao coordenador com o relatório de instalação, pra ele mostrar um resumo limpo à pessoa.
