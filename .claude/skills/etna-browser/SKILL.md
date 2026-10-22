---
name: etna-browser
description: Automação de navegador para testar e validar apps web: detecta o servidor de desenvolvimento, usa esperas nomeadas (nunca tempo fixo), seletores resistentes, preenchimento de formulário, extração de dados e prints. Prefira as ferramentas MCP do Playwright (browser_navigate, browser_snapshot, browser_click, browser_fill_form...) quando estiverem carregadas; use script avulso na pasta temporária só quando precisar de lógica que o MCP não cobre (laço, extração complexa, cabeçalhos, vários tamanhos de tela em lote). Use quando o pedido for "testa essa página", "valida esse fluxo", "preenche esse formulário", "vê se quebrou", "tira um print", "confere no celular". NÃO use para caçar falha de segurança nem para montar hero de site (etna-site-scrub).
---

# etna-browser

Automação de navegador: MCP nativo primeiro, script Node avulso como plano B. É um método de
esperas, seletores e organização de arquivos, não uma camada em volta da API.

## Ordem de decisão

1. **As ferramentas MCP do Playwright estão carregadas?** Use direto (`browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_fill_form`, `browser_wait_for`). Sem preparação, sem arquivo, com a sessão já aberta.
2. **Precisa de lógica que o MCP não oferece** (laço sobre N links conferindo o status, vários tamanhos de tela em sequência, cabeçalho próprio por requisição, extração estruturada de tabela)? Script avulso com Playwright na pasta temporária.
3. Nunca escreva script só pra fazer o que uma chamada do MCP já faz: gasta token à toa e aumenta a chance de erro.

## Passo 0: sempre, antes de apontar para localhost

Descubra qual servidor está rodando antes de chutar porta. Nunca fixe `localhost:3000` sem conferir.

```bash
lsof -nP -iTCP -sTCP:LISTEN | grep -E ':(3000|3001|5173|5174|8080|4200)\b'
```

No Windows (PowerShell): `Get-NetTCPConnection -State Listen | Where-Object LocalPort -In 3000,3001,5173,5174,8080,4200`.

- Achou 1 porta: use e diga qual.
- Achou 2 ou mais: pergunte qual (não escolha por palpite).
- Nenhuma: peça a URL ou ofereça subir o servidor de desenvolvimento.

## Regra de ouro 1: espera nomeada, nunca tempo fixo

`waitForTimeout(N)` é aposta, não verificação: ou espera demais (lento) ou de menos (instável).
Toda espera aponta para uma condição que dá pra observar:

```javascript
await page.waitForURL('**/painel');                       // a navegação terminou
await page.waitForSelector('[data-testid="lista-carregada"]'); // o elemento existe
await page.waitForLoadState('networkidle');                // a rede sossegou
```

Exceção: animação puramente visual, sem nenhum sinal de estado. Aí `waitForTimeout` é o único
jeito, e vai junto um comentário explicando o motivo.

## Regra de ouro 2: seletor resistente, nesta ordem de preferência

1. `data-testid` / `aria-label`: sobrevive a mudança visual.
2. `role` + texto acessível (`getByRole('button', { name: 'Confirmar' })`).
3. Atributo semântico (`input[name="email"]`).
4. Classe CSS: só se nenhuma opção acima servir; classes de estilo mudam a cada redesenho.

Nunca use `nth-child` nem seletor só de posição: quebra na menor mudança de ordem do DOM.

## Regra de ouro 3: script na pasta temporária, nunca no repositório

Script de teste não é parte do produto. Sempre `/tmp/etna-browser-<apelido>.js`, nunca dentro da
pasta do projeto. O sistema limpa sozinho e o repositório fica limpo. (No Windows, use a pasta
temporária da sessão.)

```javascript
// /tmp/etna-browser-checkout.js
const { chromium } = require('playwright');

const ALVO = process.env.ETNA_TARGET_URL || 'http://localhost:5173';

(async () => {
  const browser = await chromium.launch({ headless: true }); // pirâmide de QA: sem janela por padrão
  const page = await browser.newPage();

  await page.goto(`${ALVO}/checkout`);
  await page.getByRole('button', { name: 'Finalizar compra' }).click();
  await page.waitForURL('**/confirmacao');

  console.log('checkout OK, chegou na confirmação');
  await browser.close();
})();
```

Rodar: `node /tmp/etna-browser-checkout.js`.

## Regra de ouro 4: pirâmide de QA, do mais barato ao mais caro

1. **Sem janela** por padrão (`headless: true`). Só abre janela visível (`headless: false`) se a pessoa pedir depuração visual.
2. **Primeiro o texto/DOM** (`page.textContent()`, `page.locator(...).count()` ou `browser_snapshot` no MCP): mais barato e mais previsível que pixel.
3. **Print só no veredito**, quando alguém precisa ver (aprovação humana, comparação visual, prova de bug). Print a cada passo intermediário é ruído.

## Preencher formulário

```javascript
await page.getByLabel('Nome').fill('Maria Souza');
await page.getByLabel('E-mail').fill('maria@exemplo.com');
await page.getByRole('button', { name: 'Enviar' }).click();
await page.waitForSelector('[data-testid="confirmacao-envio"]');
```

No MCP, `browser_fill_form` faz isso numa chamada só. Prefira quando o formulário é simples
(campo → valor).

## Extrair dados

```javascript
const linhas = await page.locator('table tbody tr').all();
const dados = await Promise.all(
  linhas.map(async (linha) => ({
    nome: await linha.locator('td:nth-child(1)').textContent(),
    status: await linha.locator('td:nth-child(2)').textContent(),
  })),
);
console.log(JSON.stringify(dados, null, 2));
```

## Conferir responsivo (vários tamanhos de tela)

```javascript
const viewports = [
  { nome: 'desktop', width: 1920, height: 1080 },
  { nome: 'tablet', width: 768, height: 1024 },
  { nome: 'mobile', width: 375, height: 667 },
];

for (const v of viewports) {
  await page.setViewportSize({ width: v.width, height: v.height });
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: `/tmp/etna-browser-${v.nome}.png`, fullPage: true });
}
```

## Sem força bruta

O seletor não acha o elemento? No máximo **3 tentativas** com a mesma abordagem (por exemplo,
variar o seletor). Na 3ª falha, pare e relate a lacuna; nada de testar 10 variações de classe
CSS no escuro. Causa comum: elemento dentro de shadow DOM ou iframe. Confira isso antes de
insistir no seletor.

## Bug achado no teste vira finding, não relato solto

Se a automação descobrir um bug real do produto (link quebrado, formulário que não envia, layout
quebrado no celular), não despeje na resposta em texto. Registre em `TASK/items/F-XXX.md` (um
arquivo por bug) seguindo a `qa-finding-protocol`. A automação é o instrumento da descoberta; o
item é o registro que sobrevive à sessão.

## Cabeçalhos próprios

Quando precisar identificar o tráfego automatizado ou passar uma autenticação global:

```javascript
const context = await browser.newContext({
  extraHTTPHeaders: { 'X-Etna-Browser': '1' },
});
const page = await context.newPage();
```

## Quando algo não funciona

- **Playwright não instalado:** `npm install playwright && npx playwright install chromium` (uma vez, no projeto ou global).
- **Elemento não encontrado:** veja se não é shadow DOM ou iframe antes de trocar o seletor; acrescente uma espera nomeada explícita.
- **Navegador não abre com janela:** confira `headless: false` e se há tela disponível (SSH e CI não têm).

## Origem

Skill original do Etna, escrita na nossa voz a partir de técnica de domínio público. Nenhum texto
ou código de terceiros foi reproduzido; a referência técnica consultada (MIT, lackeyjb/playwright-skill)
serviu só pelos fatos, com expressão inteiramente nova.
