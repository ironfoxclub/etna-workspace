---
name: etna-backend-supabase
description: Use em QUALQUER trabalho com Supabase num SaaS multi-inquilino - esquema e migrações, desenho de políticas RLS, Auth (JWT/sessão), buckets do Storage, Edge Functions, fluxo de CLI/MCP ou revisão de segurança e desempenho de tabelas existentes. Gatilhos - "política RLS", "row level security", "migração supabase", "multi-tenant", "auth.uid()", "security definer", "bucket do storage", "supabase CLI", "consulta lenta" numa tabela do Supabase, "isolamento de inquilino". NÃO serve para ajuste genérico de Postgres sem nenhuma superfície do Supabase (trabalho só de Postgres pula as seções de CLI/Auth/Storage) nem para ligar o cliente Supabase no frontend sem mudar esquema ou política.
---

# etna-backend-supabase

SaaS multi-inquilino no Supabase é 80% modelagem de RLS e 20% o resto. Este documento é o
checklist de segurança e desempenho que evita os furos clássicos; não é um tutorial de CLI.

## Regra 0: não confie na memória de treino

O Supabase muda a cada versão (assinatura de função, `config.toml`, convenção da API). Antes de
implementar algo novo, use `search_docs` (MCP) ou busque a página `.md` correspondente
(`https://supabase.com/docs/<caminho>.md`). Nunca adivinhe flag da CLI: rode `--help` primeiro,
porque a estrutura dos subcomandos muda entre versões.

**Sem força bruta:** no máximo 3 tentativas na mesma abordagem (mesma política, mesmo erro). Na
3ª falha, pare: olhe o `EXPLAIN`, releia a documentação do assunto ou rode `supabase db advisors`.
Não repita o mesmo `create policy` mudando um detalhe ao acaso 6 vezes na esperança de que funcione.

**Confira o trabalho.** Correção sem verificação não está pronta: depois de aplicar política,
migração ou permissão, rode a consulta de teste correspondente (um `select` com o papel afetado, ou
o UPDATE/INSERT que a política deveria barrar) e confirme o resultado esperado antes de encerrar.

## Isolamento de inquilino: o checklist que faz ou quebra o produto

Toda tabela em esquema exposto (`public` por padrão) é alcançável pela Data API se `anon`/
`authenticated` tiverem permissão. RLS desligada nela é uma porta destrancada, não uma decisão de
desempenho. Regra prática: **a RLS liga no `create table`, nunca depois "quando der tempo".**

### Exposição na Data API: confira antes de supor "tabela nova = acessível"

Dependendo da configuração de Data API do projeto (`Settings → Data API`), uma tabela nova criada
por SQL pode NÃO ficar exposta sozinha: `anon`/`authenticated` precisam de `GRANT` explícito. Isso
é **separado da RLS**: a RLS controla quais *linhas* aparecem depois que a tabela já é alcançável;
o GRANT controla se a tabela é alcançável. Se a pessoa disser "criei a tabela por SQL e ela não
aparece na API", olhe a configuração da Data API e os GRANTs antes de suspeitar da RLS. Ao liberar
acesso público (`anon`/`authenticated`), ligue a RLS junto, sempre: nunca um sem o outro.

### Auth e claims

- **Nunca leia `user_metadata` / `raw_user_meta_data` dentro de uma política nem de qualquer decisão de autorização.** O próprio usuário edita esse campo pelo SDK do cliente, e ele viraria um "sou admin: true" autoatribuído. A autorização mora em `app_metadata` / `raw_app_meta_data`, que só a service role escreve.
- Apagar um usuário não revoga os tokens já emitidos. Se a operação é sensível, invalide a sessão primeiro (`auth.sessions`) ou mantenha a validade curta; não suponha que "apaguei = acabou o acesso".
- Os claims de `auth.jwt()` só atualizam quando o token é renovado: não suponha que uma mudança em `app_metadata` já valha na próxima requisição do mesmo usuário sem renovação.
- `service_role` / chave secreta JAMAIS em cliente público. No Next.js, toda variável `NEXT_PUBLIC_*` vai para o pacote do navegador: nunca ponha a chave secreta nesse prefixo.

### RLS: as 4 armadilhas que passam no "funciona" e falham em produção

1. **View ignora a RLS por padrão.** No Postgres 15+: sempre `create view ... with (security_invoker = true)`. Em versão anterior, revogue o acesso de `anon`/`authenticated` na view ou mova-a para um esquema não exposto; senão a view é um túnel que pula toda política da tabela de origem.
2. **UPDATE sem política de SELECT afeta 0 linhas em silêncio.** A RLS precisa selecionar a linha antes de atualizar; sem `for select`, o `UPDATE` roda sem erro e não muda nada. É o bug fantasma clássico do "meu update não fez nada".
3. **`TO authenticated` sozinho é autenticação sem autorização: é BOLA/IDOR de bandeja.** Confere só o papel, não o dono da linha. Combine sempre com um critério de posse:
   ```sql
   create policy tenant_read on invoices
     for select to authenticated
     using ( (select auth.uid()) = owner_id );
   ```
   E nunca use `auth.role() = 'authenticated'` (obsoleto, e quebra com login anônimo, porque o usuário anônimo carrega o papel `authenticated` do Postgres mesmo sem login de verdade).
4. **UPDATE precisa de `USING` E `WITH CHECK`.** Só `USING` deixa o usuário passar a linha para outro inquilino ou dono; o `WITH CHECK` é o que trava o valor final, não só o valor lido:
   ```sql
   create policy tenant_write on invoices
     for update to authenticated
     using ( (select auth.uid()) = owner_id )
     with check ( (select auth.uid()) = owner_id );
   ```

### `SECURITY DEFINER`: armadilha de privilégio, não atalho para bug

Função `SECURITY DEFINER` roda com o privilégio de quem a criou (normalmente um papel que já tem
`bypassrls`). **Nunca** ponha `SECURITY DEFINER` numa função só pra fazer um erro de permissão
sumir: isso retira o controle de acesso sem consertar a causa. O padrão é `SECURITY INVOKER`.

Quando for realmente necessário (por exemplo, uma consulta interna que precisa furar a RLS de
propósito): esquema não exposto (`private`, nunca `public`), `auth.uid()` conferido DENTRO do
corpo da função e `revoke execute ... from public, anon, authenticated`. O Postgres dá `EXECUTE`
a `PUBLIC` por padrão em toda função nova, então uma `SECURITY DEFINER` esquecida em `public` é
um endpoint público sem documentação. Rode `supabase db advisors` depois de qualquer mudança
nesse território.

### Storage

Upsert de arquivo (substituir um que já existe) exige INSERT + SELECT + UPDATE na política do
bucket. Dar só INSERT faz o upload novo funcionar e a substituição falhar em silêncio, sintoma
confuso porque "criar" funciona e só "sobrescrever" quebra.

### Cadeia de suprimentos

Fixe a versão e versione o arquivo de lock de todo pacote do Supabase (`supabase-js`,
`@supabase/ssr`, etc.). Sem isso, uma atualização transitiva silenciosa muda o comportamento da
autenticação em produção sem nenhuma diferença visível no seu código.

## Desempenho: o que realmente muda o resultado (por ordem de impacto)

1. **Índice em toda coluna de `WHERE`/`JOIN`.** O Postgres NÃO indexa chave estrangeira sozinho: todo `references outra_tabela(id)` precisa de um `create index` manual, senão JOIN e `ON DELETE CASCADE` viram leitura da tabela inteira. Consulta para achar chave estrangeira sem índice:
   ```sql
   select conrelid::regclass as tabela, a.attname as coluna
   from pg_constraint c
   join pg_attribute a on a.attrelid = c.conrelid and a.attnum = any(c.conkey)
   where c.contype = 'f'
     and not exists (
       select 1 from pg_index i
       where i.indrelid = c.conrelid and a.attnum = any(i.indkey)
     );
   ```
2. **Embrulhe a função na política: `(select auth.uid())`, nunca `auth.uid()` solto.** Sem o `select`, a função roda uma vez POR LINHA (1 milhão de linhas = 1 milhão de chamadas); com o `select`, o planejador guarda o resultado e reaproveita, e o ganho é de uma ordem de grandeza em tabela grande. Indexe também a coluna que a política compara (`user_id`, `tenant_id`).
3. **Pool de conexões é obrigatório, não otimização.** Cada conexão do Postgres custa de 1 a 3 MB de RAM; sem pooler (pgbouncer/Supavisor), 500 usuários simultâneos = 500 conexões = banco de joelhos. O modo transação (devolve a conexão ao fim de cada transação) atende a maioria dos apps; o modo sessão só quando precisar de prepared statement ou tabela temporária entre consultas.
4. **N+1 mata no laço da aplicação, não no SQL isolado.** Uma consulta por item dentro de um `for` fica invisível no profiling de cada consulta e só aparece no agregado. Troque por `where coluna = any($1::bigint[])` passando o array de IDs de uma vez, ou por um JOIN: 1 ida ao banco em vez de N+1.

O detalhe fino (esquema, lock, monitoramento) fica fora do escopo enxuto deste documento: busque
sob demanda com `search_docs` quando o caso pedir (particionamento, `pg_stat_statements`, advisory lock).

## CLI: descubra, não decore

```bash
supabase --help
supabase <grupo> --help
supabase <grupo> <comando> --help
```

Pegadinhas atuais:
- `supabase db query` exige CLI ≥ 2.79.0; sem isso, use `execute_sql` (MCP) ou `psql` puro.
- `supabase db advisors` exige CLI ≥ 2.81.3; o plano B é `get_advisors` (MCP).
- Migração nova SEMPRE nasce de `supabase migration new <nome>`: nunca invente nome de arquivo de migração nem confie na memória de um formato antigo.

## Fluxo de migração (iterar rápido, commitar limpo)

1. **Iteração:** mude o esquema com `execute_sql` (MCP) ou `supabase db query` (CLI), que roda direto, sem gravar uma entrada de migração a cada chamada. O `apply_migration` grava histórico em TODA chamada; usá-lo para iterar te prende ao primeiro SQL que você mandou, porque `db diff`/`db pull` depois comparam com esse histórico sujo.
2. **Antes de fechar:** rode `supabase db advisors` (ou o MCP `get_advisors`) e resolva o que apontar. Se a mudança tocou view, função ou política de storage, releia o checklist de isolamento de inquilino acima.
3. **Commit:** `supabase db pull <nome-descritivo> --local --yes` gera a migração limpa a partir do estado real.
4. **Confirme:** `supabase migration list --local`.

## Servidor MCP

Instalação e URL do servidor: `https://supabase.com/docs/guides/getting-started/mcp` (busque a
página atual; não fixe o endereço de memória). Diagnóstico em ordem: `curl` no endereço (401 =
servidor no ar, tempo esgotado = fora do ar) → confira se o `.mcp.json` aponta para o servidor
certo → se ainda não há ferramentas, a pessoa precisa concluir o fluxo OAuth no navegador e
recarregar a sessão.

## Achou falha de isolamento de inquilino ou de desempenho em produção?

Não escreva relatório solto. Registre um arquivo por bug em `TASK/items/F-XXX.md`, seguindo a
skill `qa-finding-protocol`: reprodução, severidade, tabela ou política afetada. É o contrato que
o pipeline de lançamento consome; achado sem card não vira correção rastreável.

## Origem

Skill original do Etna. Doutrina de Supabase/Postgres reescrita na nossa voz a partir de material
com licença MIT (`supabase/agent-skills`, Supabase Inc.). Nenhum texto ou código de terceiros foi
reproduzido literalmente.
