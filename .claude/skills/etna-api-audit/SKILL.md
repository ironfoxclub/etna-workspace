---
name: etna-api-audit
description: "Audita superfícies de API (REST, GraphQL, RPC/tRPC/gRPC, Server Actions, webhooks) contra o OWASP API Security Top 10 (2023). Use quando o pedido falar em 'auditoria de API', 'segurança de API', BOLA, BFLA, mass assignment, limite de requisições, segurança de GraphQL/REST, exposição excessiva de dados, ou pedir revisão de endpoints por falha de autorização ou autenticação. NÃO use para varredura do projeto inteiro por categoria genérica (é outra skill, de escopo mais amplo) nem para teste ativo contra produção sem autorização explícita."
allowed-tools: Read, Grep, Glob, Bash, Write
---

# etna-api-audit

Auditoria pontual do contrato de uma API, não do projeto inteiro. Passa por CADA endpoint com os
10 padrões de falha do OWASP API Top 10 (2023). Todo achado vira `TASK/items/F-XXX.md` (skill
`qa-finding-protocol`), nunca um relatório solto em markdown perdido por aí.

**Sem força bruta:** no máximo 3 tentativas de grep ou reprodução na mesma categoria. Na 3ª falha
sem sinal, registre "lacuna de cobertura" no item e vá pra próxima categoria. Não trave a auditoria
inteira num endpoint teimoso.

## 1. Mapear a superfície antes de caçar bug

1. Levante toda rota, resolver e procedure: REST, GraphQL, tRPC, gRPC, Server Actions, webhooks, RPC interno.
2. Identifique o modelo de autenticação: JWT, cookie de sessão, chave de API, mTLS, escopos OAuth.
3. Identifique o modelo de multi-inquilino: inquilino único, vários inquilinos, isolamento por linha.
4. Marque os recursos sensíveis: dados de usuário, pagamento, arquivos, funções de administrador.

Sem esse mapa, a auditoria vira caça ao tesouro às cegas. Comece sempre por aqui.

## 2. Checklist por categoria (OWASP API Top 10 2023)

### API1: autorização quebrada no nível do objeto (BOLA)
É a nº 1 em exploração real. Toda rota que recebe um ID de objeto precisa checar a posse ANTES de ler ou alterar, não depois.
- Certo: `findFirst({ where: { id, ownerId: session.userId } })` numa consulta só. Errado: `findById(id)` seguido de um `if` que confere o dono (a consulta já passou o dado ao processo, e é fácil esquecer o `if`).
- Relação carregada pelo ORM sem filtro: `order.include(customer.paymentMethod)` devolve o cartão de outro inquilino se a relação não for protegida de forma explícita.
- UUID não é controle de acesso: só atrapalha a enumeração, não impede.
- Slug ou public_id "difícil de adivinhar" tratado como se fosse segredo.
- Grep de partida: `params.id`, `req.params.`, `formData.get(`, chamadas `.findById(`/`.find(` sem cláusula `where`, resolvers GraphQL com argumento `id` chamando `.findUnique` direto.

### API2: autenticação quebrada
- Verificador de JWT que aceita `alg: none`.
- Comparação de segredo sem `crypto.timingSafeEqual` (ou equivalente): abre ataque por tempo de resposta.
- Refresh token que nunca gira e não tem lista de revogação.
- Redefinição de senha que devolve o token no corpo da resposta em vez de só enviar por e-mail.
- Chave de API na query string da URL: fica gravada em log de acesso, CDN e proxy.
- Comparação do bearer token com variável de ambiente sem checar se ela existe: se a variável faltar, `"Bearer ${undefined}"` vira um valor literal válido.
- Grep de partida: `jwt.verify`, `jsonwebtoken`, `Bearer ${process.env`, `jwt.decode` sem verify.

### API3: autorização quebrada no nível da propriedade (mass assignment + exposição excessiva)
- O endpoint devolve a linha inteira do banco em vez de um objeto de resposta enxuto: `res.json(usuario)` vaza `password_hash`, `stripe_customer_id`, flags internas.
- Campo só de administrador (`role`, `is_verified`, `tenant_id`) aceito numa atualização feita por usuário comum: mass assignment clássico.
- Mutation de GraphQL sem checagem de campo por papel: o resolver só confere "está logado", não "pode mudar este campo".
- Grep de partida: `res.json(` sem escolha explícita dos campos, `Object.assign(registro, req.body)`, `findByIdAndUpdate(id, req.body)` (Mongoose), `.update().set(req.body)` (Drizzle), `update(req.body)` (Sequelize).

### API4: consumo irrestrito de recursos
- Sem limite de requisições em endpoint de autenticação (login, cadastro, redefinição de senha, envio de SMS/e-mail).
- Sem cota por inquilino em operação cara (chamada a LLM, busca, processamento de arquivo, disparo de webhooks).
- Tamanho de página sem teto: `?limit=10000000` devolve 10 milhões de linhas.
- Profundidade de consulta GraphQL sem limite: relação circular roda para sempre.
- Complexidade de consulta GraphQL não analisada: uma única consulta dispara N+1 contra tabela gigante.
- Webhook que refaz trabalho caro sem idempotência.

### API5: autorização quebrada no nível da função (BFLA)
- A checagem existe na rota mas não no handler: o middleware genérico não pega rota montada à mão.
- Endpoint "meio administrativo" alcançável trocando `POST /api/v1/perfil/me` por `POST /api/v1/perfil/<outro_id>`.
- Troca de verbo: `DELETE /admin/usuarios/123` está bloqueado, mas `POST /admin/usuarios/123/deletar` passa.
- Autorização condicional baseada em `req.user.role === "admin"` quando o papel vem de um cabeçalho controlado pelo cliente.
- Rota irmã sem proteção: `PUT /:id` protegido, mas `POST /:id/enviar` escreve na mesma linha sem checagem.
- Em TODO handler, pergunte: ele valida a autenticação de forma explícita, ou confia em algo anterior que pode não cobrir este caminho?

### API6: acesso irrestrito a fluxos de negócio sensíveis
- O endpoint permite automação que quebra a intenção do negócio: comprar estoque limitado 1000 vezes por segundo, reservar todos os assentos, forçar código de indicação.
- Sem CAPTCHA, prova de trabalho ou identificação do dispositivo em fluxo com restrição de negócio (cadastro, resgate de cupom, voto, curtida).
- Proteção contra automação só na interface e não na API: contorno trivial indo direto no endpoint.

### API7: falsificação de requisição pelo servidor (SSRF)
- URL controlada pelo usuário passada para um fetch no servidor: URL de webhook, busca de imagem, callback de SSO, geração de PDF, pré-visualização de link.
- Lista de permitidos que checa só o nome do host: não cobre IPv6 mapeado para IPv4, ponto final, metadados de nuvem, IP codificado.
- `redirect: "follow"` (padrão) num fetch com URL do usuário deixa um 302 pular para o serviço de metadados.
- Entrega de webhook do seu domínio para a URL do atacante: seu servidor virou proxy dele.

### API8: configuração de segurança incorreta
- CORS com `Access-Control-Allow-Origin: *` junto de `Allow-Credentials: true` (o navegador recusa, mas o servidor nem devia servir isso).
- Reflexão do cabeçalho `Origin` sem lista de permitidos: qualquer origem passa.
- Erro detalhado vazando pilha, query string e IDs internos.
- Introspecção do GraphQL ou especificação OpenAPI expostas em produção com o esquema completo.
- Cabeçalho de segurança faltando (o conjunto completo é escopo de uma auditoria mais ampla, fora desta skill).
- Cookie de sessão sem a flag `HttpOnly`.

### API9: inventário de APIs mal gerido
- Versão antiga da API (`/v1/`) ainda no ar e sem correção ao lado da `/v2/`: o atacante prefere a que tem menos checagens.
- Endpoint "interno" ou de homologação acessível pela internet (URL de preview de deploy, ambiente `*-staging` exposto).
- Endpoint sem documentação: todo endpoint deveria aparecer no contrato publicado, e o órfão é sinal para auditar.
- Rota de depuração gerada automaticamente: `/__debug`, `/__db`, rota padrão de framework.
- Grep de partida: `app.get`, `router.get`, pastas `pages/api/`/`app/api/`; compare com o contrato publicado.

### API10: consumo inseguro de APIs
- O serviço chama uma API de terceiro e confia na resposta sem validar: redirecionamento aberto via `provider.user.profile_url`, XSS via `provider.user.bio` exibido sem escape.
- Chamada entre servidores sem verificação de integridade (JWT assinado, mTLS, HMAC): quem alcança a URL do upstream finge ser o upstream.
- Erro do upstream guardado em cache como sucesso: um 200 com corpo JSON de erro virando dado em cache.

## 3. Específico por protocolo

**GraphQL:** introspecção ligada em produção (`__schema`/`__type`); autorização por campo ausente (o resolver valida a consulta mas não o campo); profundidade e complexidade sem limite; abuso de lote (1000 consultas num POST só); mensagem de erro revelando o caminho interno de um campo.

**REST:** verbo HTTP não imposto (`GET` aceito em endpoint que muda estado, com risco de CSRF e envenenamento de cache); Content-Type presumido mas não validado; path traversal no ID do recurso (`/arquivos/../../etc/passwd`).

**Webhook:** verificação de assinatura ausente ou contornável; repetição de requisição sem tolerância de horário/nonce; caminho previsível (`/webhooks/stripe`) sem lista de IPs permitidos nem assinatura.

## 4. Confira a correção rodando, não no build

`tsc --noEmit` verde e build passando NÃO é correção verificada. Reproduza o cenário real:
- BOLA: autentique como usuário A, peça o recurso do usuário B e confira que volta 404, não 200.
- Mass assignment: envie a requisição com o campo extra preenchido e confira que o campo é ignorado ou rejeitado.
- Limite de requisições: bata no endpoint a 10 vezes a taxa configurada e confira que volta 429, não 200.
- CORS: envie uma requisição com `Origin: https://evil.example` e confira o bloqueio.

## 5. Registrar o achado: sempre como item, nunca relatório solto

Cada vulnerabilidade confirmada nasce como `TASK/items/F-XXX.md` (skill `qa-finding-protocol`),
com severidade, endpoint ou handler, CWE, prova de conceito mínima (nunca carga de ataque),
correção e um critério de verificação observável. Não escreva achado em markdown fora de
`TASK/items/`.

Inventário final: para cada endpoint mapeado no passo 1, classifique como **auditado sem
problemas** / **auditado com N achados** / **N/A com motivo** (ex.: health-check sem superfície de
autenticação).

## 6. Limites

- Audite só as APIs que a pessoa apontou ou liberou.
- Entregue correção, não exploit: a prova de conceito é a menor requisição que mostra o bug, nunca uma carga pronta para ataque.
- Achado de baixa confiança vai marcado como "potencial", não como confirmado.
- Nunca rode prova de BOLA contra produção real sem autorização expressa por escrito: leia o código e proponha a verificação num ambiente de teste.
- Recuse varredura em massa, credential stuffing e qualquer exploração ativa de fluxo de abuso.

## Referências

OWASP API Security Top 10 (2023) · OWASP Cheat Sheet de segurança REST · OWASP Cheat Sheet de segurança GraphQL · CWE-639 (contorno de autorização por chave controlada pelo usuário) · CWE-915 (modificação mal controlada de atributos determinados dinamicamente)

## Origem

Skill original do Etna, escrita na nossa voz a partir de técnica de domínio público (OWASP API
Security Top 10). Nenhum texto ou código de terceiros foi reproduzido. A fonte de inspiração
(`api-audit`, repositório `cybersecurity-skills` de Bri Russell) é MIT; a atribuição fica
registrada por transparência, sem reaproveitar expressão.
