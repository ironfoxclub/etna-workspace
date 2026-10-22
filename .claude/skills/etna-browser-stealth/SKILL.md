---
name: etna-browser-stealth
description: Use quando a automação com Playwright for bloqueada, cair em CAPTCHA ou for marcada como robô num site (QA, auditoria de acessibilidade, monitoramento, coleta). Só carrega o modo anti-detecção (rebrowser-playwright + Chrome real com janela) DEPOIS que uma execução normal sem janela falhou; nunca carregue de entrada numa automação nova. Gatilhos - "o site está bloqueando meu coletor", "detectado como robô", "contornar CAPTCHA", "playwright indetectável", "teste de fingerprint falhando", "navigator.webdriver true".
---

# etna-browser-stealth

Camada anti-detecção para automação com Playwright em qualquer site. **Carga condicional**: só entra depois que uma execução simples
sem janela foi barrada. Não monte essa maquinaria numa tarefa que ainda não provou precisar dela.

## Por que três camadas e não um script só

A maior parte da evasão vem do **navegador de verdade**, não de JavaScript escrito à mão. Da causa
para o efeito:

| Sinal de detecção | Playwright padrão sem janela | Resolvido por |
|---|---|---|
| Vazamento de CDP `Runtime.enable` | presente (entrega clássica do modo sem janela) | `rebrowser-playwright` + `REBROWSER_PATCHES_RUNTIME_FIX_MODE` |
| Assinatura `__pwInitScripts` (`isPlaywright`) | presente | init script que apaga a cada navegação |
| `navigator.webdriver` | `true` | o rebrowser informa `false`; **nunca apague a propriedade**, `undefined` também denuncia |
| Renderizador WebGL | SwiftShader (software) | `channel:'chrome'` + `headless:false` (GPU real) |
| User-Agent | contém "HeadlessChrome" | Chrome real via `channel`, sem sobrescrever em JS |
| Fingerprint de canvas | assinatura de software | GPU real do Chrome com janela, sem ruído em JS |
| `navigator.plugins` | lista vazia | `PluginArray` genuíno do Chrome real |
| `navigator.languages` | só `['en-US']` | opção `locale` do contexto: nativa, sem getter em JS |

**Regra de ouro:** cada remendo em JS que finge um valor cria a sua própria inconsistência
detectável (propriedade própria que não deveria existir, divergência entre thread principal e
worker, erro `Illegal invocation`). Quanto menos fingimento, mais consistência, e mais difícil de
marcar. A receita abaixo mantém só DOIS remendos ativos; o resto fica por conta do navegador genuíno.

## Montagem mínima

Pré-requisitos: Node 18+ (ESM), Google Chrome instalado (não Chromium) e modo com janela
obrigatório (sem tela, sem stealth).

```bash
npm init -y && npm install rebrowser-playwright
```

A receita, em ordem (cada linha existe por um motivo; nenhuma é ritual):

1. Exporte `REBROWSER_PATCHES_RUNTIME_FIX_MODE=addBinding` **no ambiente, antes** de carregar a biblioteca: o remendo é aplicado na importação, não em tempo de execução.
2. Importe `rebrowser-playwright` no lugar de `playwright`.
3. Abra com `headless: false` + `channel: 'chrome'`: GPU, canvas, WebGL e plugins passam a ser os do Chrome real da máquina, não emulações.
4. Acrescente a flag de linha de comando que desliga o sinalizador de automação do Blink.
5. No contexto, declare o `locale` verdadeiro: ele alinha `navigator.languages` ao cabeçalho `Accept-Language` sozinho. Não escreva os dois à mão: a divergência entre eles É a pista.
6. UM único init script: percorra as chaves de `window`, apague as que combinam com o prefixo de instrumentação do Playwright e garanta que `window.chrome` exista. **Não toque em mais nada de `navigator`**: valor real é consistente por construção; valor forjado cria justamente a inconsistência que o detector procura.
7. Só então navegue. Feche o navegador no `finally`.

O erro que anula tudo: rodar a receita com `headless: true` porque "o servidor não tem tela". Sem
tela não há stealth; use `xvfb` e mantenha o modo com janela.

## O que os dois remendos fazem (e por que só eles sobreviveram)

| Medida | Motivo |
|---|---|
| Apagar `window.__pwInitScripts` / `__playwright*` a cada navegação | remove a assinatura determinística que os detectores de `isPlaywright` procuram |
| `REBROWSER_PATCHES_RUNTIME_FIX_MODE=addBinding` (antes do import) | esconde o vazamento de `Runtime.enable` pelo CDP |

Todo o resto fica com o navegador real (`channel:'chrome'` + com janela): UA genuíno, WebGL/GPU,
canvas, `PluginArray`, hardware e permissões coerentes, `languages` via `locale`.

**Removido por ser contraproducente** (cada um criava uma pista própria): `navigator.plugins`
falso, ruído em `getImageData`, `hardwareConcurrency`/`deviceMemory` fixos, deslocamento de
`outerWidth/Height`, sobrescrita de permissões (dá `Illegal invocation`), apagar
`navigator.webdriver` (vira `undefined`, o que denuncia), getter customizado de
`navigator.languages` (diverge do worker).

Flag de abertura: `--disable-blink-features=AutomationControlled`. `--no-sandbox` só se pedirem:
é sinal de automação E risco de segurança, nunca o padrão.

Uma SPA pesada (rede social) pode registrar `[rebrowser-patches] cannot get world`. Não é fatal,
a página carrega. Se incomodar, troque para `REBROWSER_PATCHES_RUNTIME_FIX_MODE=alwaysIsolated`.

## Comportamento humano (quando o fingerprint sozinho não basta)

Sites com barreira comportamental (Cloudflare Turnstile, DataDome) não cedem só com fingerprint
limpo. Acrescente: atraso aleatório entre ações, digitação caractere por caractere no lugar de
`fill()` e movimento do mouse antes do clique. Isso reduz a assinatura de "rápido demais para ser
humano"; não é contorno de CAPTCHA.

## Cobertura honesta: o que passa e o que não passa

Fingerprint + framework de automação: passa limpo (webdriver `false`, WebGL/UA reais, sem
vazamento de Runtime, sem assinatura `isPlaywright`).

Barreiras de comportamento ou de IP (Cloudflare Turnstile, DataDome, Kasada) e telas de login:
**sem garantia de contorno**. Pedem IP residencial e interação real, ou troca de motor
(`patchright` como substituto direto, ou `nodriver`, que evita toda a classe de protocolo
CDP/automação).

Em volume, redes sociais (Instagram/Facebook/LinkedIn/TikTok) aplicam envelhecimento do cookie de
sessão, HTTP 999 e limite de requisições. Isso é problema de IP e de conta, não de fingerprint, e
esta skill não resolve.

**Limitação conhecida que sobra:** `window.__playwright_builtins__` é um global não configurável
do Playwright e nenhuma versão atual do rebrowser consegue apagá-lo ou redefini-lo. Nenhum
detector testado hoje usa isso, mas pode virar pista no futuro. Relate com honestidade; não finja
100%.

## Sem força bruta

No máximo 3 variações de remendo para um mesmo detector. Passou de 3 sem resultado? Então é
barreira de comportamento ou de IP, não de fingerprint: mude de abordagem (proxy residencial,
`patchright`, `nodriver`) ou relate a lacuna como limitação; nunca insista numa 4ª variação do
mesmo JS.

Se o bloqueio persistir e a causa não ficar clara em 3 tentativas,
registre como finding pela skill `qa-finding-protocol` (um arquivo `TASK/items/F-XXX.md`) em vez
de deixar o diagnóstico solto na conversa.

## Python

`undetected-chromedriver` é a opção recomendada: remenda no nível do driver, não só em JS (o
`playwright-stealth` em Python só remenda JS, e o WebGL continua mostrando SwiftShader). Se o
pipeline é Python mas o stealth precisa ser Node, chame o script `.mjs` com `subprocess.run`.

## Diagnóstico rápido

| Sintoma | Causa provável |
|---|---|
| WebGL mostra SwiftShader | está rodando sem janela de fato, ou sem GPU: force `headless:false` + `channel:'chrome'` numa máquina com GPU real |
| Ainda detectado depois dos 2 remendos | é comportamento ou IP, não fingerprint: veja "Comportamento humano" e "Cobertura honesta" |
| `ERR_MODULE_NOT_FOUND` | rode `npm install rebrowser-playwright` na mesma pasta do script |
| O processo trava | `browser.close()` fora do `finally` |

## Origem

Skill original do Etna, escrita na nossa voz a partir de técnica de domínio público. Nenhum texto
ou código de terceiros foi reproduzido. A referência (rebrowser-playwright, `playwright-bot-bypass`,
licença MIT) serviu só como pesquisa de fatos técnicos; a atribuição MIT fica registrada por
cortesia, sem reproduzir expressão.
