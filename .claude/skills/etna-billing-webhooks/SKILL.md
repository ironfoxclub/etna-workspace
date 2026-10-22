---
name: etna-billing-webhooks
description: >
  Recebe e verifica webhooks de cobrança (Stripe como caso principal; a mesma doutrina serve
  para qualquer provedor com assinatura HMAC). Use ao montar um endpoint que recebe eventos de
  pagamento ou assinatura, ao depurar falha de verificação de assinatura, ao decidir a ordem
  verificar → interpretar → idempotência, ou ao desenhar nova tentativa, espera crescente e fila
  morta para cobrança. NÃO use para chamar a API de cobrança como cliente (criar cobrança, criar
  cliente): isso é integração de saída, não recebimento de webhook. Também não use para webhook
  que não seja de cobrança (login, CI, chat) sem adaptar cabeçalhos e eventos ao provedor real.
---

# etna-billing-webhooks

## Quando usar

- Montar o handler que recebe eventos de cobrança (Stripe, ou qualquer provedor com assinatura HMAC no mesmo formato: horário + assinatura num cabeçalho).
- Depurar "assinatura inválida" ou "horário fora da tolerância".
- Decidir a sequência verificar → interpretar → idempotência → efeito colateral.
- Desenhar nova tentativa, código de resposta ou fila morta para evento que falha repetidamente.

## A cadeia de 3 elos: nunca inverta a ordem

1. **Verificar a assinatura** sobre o corpo CRU (bytes originais), antes de qualquer interpretação. Se o middleware de JSON já rodou na rota do webhook, o corpo que chega à verificação já foi transformado e a assinatura não bate. Não é defeito do provedor, é ordem errada de middleware. A rota do webhook precisa do leitor de corpo cru ANTES do leitor de JSON global, ou isolada por content-type.
2. **Interpretar o evento** só depois que a assinatura bater. O SDK oficial costuma verificar e interpretar numa chamada só (ex.: `stripe.webhooks.constructEvent`).
3. **Tratar com idempotência**, usando o ID único do evento. Nunca o payload inteiro como chave: o provedor garante *pelo menos uma vez*, não *exatamente uma vez*.

Pular o passo 1 (processar antes de verificar) é a falha de segurança clássica: qualquer pessoa que
descubra a URL do endpoint pode forjar um evento `subscription.created` e liberar acesso de graça.

## Verificação HMAC: como funciona

Assinatura = HMAC-SHA256 de `horário + "." + corpo_cru`, comparada com o valor do cabeçalho
(Stripe: `Stripe-Signature`, no formato `t=<epoch>,v1=<hex>`). Compare sempre em tempo constante
(`crypto.timingSafeEqual`), nunca com `===` direto em hex: a comparação ingênua vaza tempo e abre
ataque por temporização.

```javascript
// verificação manual: só se não houver SDK oficial disponível
const crypto = require('node:crypto');

function checarAssinaturaBilling(corpoCru, headerAssinatura, segredo) {
  const partes = Object.fromEntries(
    headerAssinatura.split(',').map((par) => par.split('='))
  );
  const base = `${partes.t}.${corpoCru}`;
  const esperado = crypto.createHmac('sha256', segredo).update(base).digest('hex');
  const bufA = Buffer.from(partes.v1, 'hex');
  const bufB = Buffer.from(esperado, 'hex');
  return bufA.length === bufB.length && crypto.timingSafeEqual(bufA, bufB);
}
```

Com o SDK oficial (prefira sempre que existir: cobre rotação de segredo e tolerância a repetição
sem código próprio):

```javascript
const billing = require('stripe')(process.env.BILLING_SECRET_KEY);
const evento = billing.webhooks.constructEvent(
  corpoCru,                             // Buffer/string, NUNCA o JSON já interpretado
  requisicao.headers['stripe-signature'],
  process.env.BILLING_WEBHOOK_SECRET,
);
```

**Proteção contra repetição:** rejeite horário fora de uma janela de tolerância (padrão de mercado:
cerca de 5 minutos). Sem essa checagem, uma requisição capturada por um intermediário ou gravada
em algum proxy pode ser reenviada para sempre e reprocessada como evento novo.

**Rotação de segredo:** durante a troca do segredo do webhook, o provedor pode mandar várias
assinaturas no mesmo cabeçalho (segredo antigo + novo). Teste contra todas antes de rejeitar, não
só contra a primeira.

## Idempotência: a chave é o ID do evento, não o payload

```javascript
async function processarEventoBilling(evento) {
  const jaProcessado = await db.query(
    'SELECT 1 FROM billing_events_processados WHERE event_id = $1',
    [evento.id],
  );
  if (jaProcessado.rowCount > 0) return { status: 'duplicado' };

  await aplicarEfeitoColateral(evento);          // liberar acesso, revogar, etc.
  await db.query(
    'INSERT INTO billing_events_processados (event_id, tipo) VALUES ($1, $2)',
    [evento.id, evento.type],
  );
  return { status: 'processado' };
}
```

Corrida entre 2 instâncias que recebem o mesmo evento ao mesmo tempo:
`INSERT ... ON CONFLICT (event_id) DO NOTHING RETURNING event_id`. Quem não receber a linha de volta
perdeu a corrida e não executa o efeito colateral de novo.

## Resposta rápida, processamento assíncrono

Devolva 2xx em milissegundos e processe depois (fila ou segundo plano). Handler síncrono lento é a
causa raiz mais comum de duplicata: o provedor entende o tempo esgotado como falha e reenvia, mesmo
que o processamento tenha terminado depois do limite.

| Situação | Status | Efeito esperado no provedor |
|---|---|---|
| Processado (ou duplicata reconhecida) | `200` | não reenvia |
| Assinatura inválida | `401` | não reenvia (falha permanente) |
| Payload malformado | `400` | não reenvia |
| Dependência indisponível (banco fora) | `503` | reenvia com espera crescente |
| Erro desconhecido no handler | `500` | reenvia |

Erro que persiste depois de N tentativas: grave numa fila morta com o motivo e o payload original,
avise a equipe e nunca descarte em silêncio.

## Eventos principais do ciclo de assinatura

| Evento | Gatilho | Efeito típico |
|---|---|---|
| `checkout.session.completed` | checkout concluído | ativar o acesso inicial |
| `customer.subscription.created` | assinatura nova | liberar o plano |
| `customer.subscription.updated` | troca de plano ou quantidade | ajustar os direitos de uso |
| `customer.subscription.deleted` | cancelamento ou expiração | revogar o acesso |
| `invoice.paid` | fatura paga | registrar o pagamento |
| `invoice.payment_failed` | fatura não paga | cobrança de recuperação, período de carência |

Lista completa de eventos: documentação do provedor. Não tente decorar tudo no handler; mapeie só
os tipos que o produto realmente consome.

## Variáveis de ambiente

```bash
BILLING_SECRET_KEY=sk_...        # chave da API do provedor
BILLING_WEBHOOK_SECRET=whsec_... # segredo específico do endpoint do webhook
```

Nunca deixe esses valores fixos no código nem os registre em log; mascare em qualquer saída de
depuração (veja a regra geral do repositório contra vazamento).

## Sem força bruta

A assinatura não bate depois de conferir corpo cru + segredo certo + janela de tolerância (3
tentativas direcionadas)? Pare e relate a lacuna. Quase sempre é um middleware consumindo o corpo
antes da rota do webhook, não erro na fórmula do HMAC. Não fique testando variações de codificação
às cegas.

## QA de webhook: achou bug, não conserte ao vivo

Se durante o teste do endpoint aparecer duplicata processada, assinatura aceita indevidamente ou
reenvio infinito, abra um finding em `TASK/items/F-XXX.md` (skill `qa-finding-protocol`) em vez de
relatório solto ou correção silenciosa no meio de outra tarefa.

## Origem

Skill original do Etna, escrita na nossa voz a partir de técnica de domínio público. Nenhum texto
ou código de terceiros foi reproduzido. A verificação HMAC e a sequência verificar → interpretar →
idempotência são conhecimento técnico comum a webhooks assinados (Stripe e provedores parecidos);
os fatos foram consultados em documentação MIT de skills de webhook de terceiros, sem copiar
expressão.
