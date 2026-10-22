---
name: etna-qa-correcao
description: Rotina do worker resolvedor de QA no Etna — pegar o próximo achado aberto (F-XXX.md) por severidade, respeitar quem já está em cada arquivo, corrigir a causa raiz, validar no app rodando, um commit por achado com o ID e atualizar o arquivo do achado. Use sempre que o seu papel for corrigir achados registrados com etna-qa-achados.
---

# etna-qa-correcao

Você trabalha em ciclo sobre a pasta de achados (padrão `TASK/items/F-XXX.md`; vale a pasta do
brief se ele indicar outra). Formato e estados: skill `etna-qa-achados`.

## 1. Escolher o próximo

1. Leia os arquivos da pasta.
2. Candidatos: `status: aberto` (e `reaberto`).
3. Ordem: severidade `alta` → `média` → `baixa`; empate, o menor número.
4. **Um arquivo de código, um dono.** Se o achado mexe num arquivo que outro resolvedor já está
   corrigindo, pule pro próximo. Achados que caem no mesmo arquivo ficam com o mesmo resolvedor.
   Nunca edite arquivo que está com outro worker.

## 2. Corrigir

1. Leia antes de mexer: o arquivo apontado, quem chama ele e a evidência (print ou trecho), até
   achar a **causa**. O sintoma do achado raramente é onde está o defeito.
2. Mude o mínimo que resolve. Nada de arrumar código vizinho "de carona".
3. **Valide antes de declarar**: checagem de tipos/build da área afetada + refaça os passos do
   achado no app rodando (servidor de desenvolvimento, Electron reaberto, etc.). Olhe o log do
   app por erro novo. Sem validação, o achado volta como `reaberto`.

## 3. Commit (um por achado)

- `git add` **só** dos arquivos que você mexeu neste achado. Nunca `git add -A` nem `git add .`:
  arquivo de outro worker no commit é contaminação.
- Mensagem com o ID: `fix(<área>): F-XXX — <o que mudou>`.
- Dois achados no mesmo arquivo continuam sendo dois commits, na ordem em que corrigiu.
- Se a pasta não for repositório git, pule o commit e anote isso na "Correção".

## 4. Atualizar o achado

No `F-XXX.md`: `status: aberto` → `status: corrigido`, e preencha "Correção (resolvedor)" com:
causa raiz (1–2 frases), arquivos + hash do commit, e **como validou** (o que rodou e o que viu).
Quem promove pra `verificado` é o teste no navegador, não você.

## Quando não dá

- **Dúvida de produto** (comportamento esperado ambíguo, escolha de UX ou de escopo): marque
  `precisa-decisão`, escreva a pergunta objetiva no arquivo e siga pro próximo. Não decida produto.
- **Três tentativas** com a mesma abordagem e nada? Anote no achado o que tentou e troque de
  abordagem ou devolva no handoff. Não fique variando a mesma ideia.
- Nunca mate processo que você não abriu. Encerrar servidor de dev = pelo PID que você subiu,
  nunca por nome (`taskkill /IM`, `pkill`).

## Fim

Acabaram os elegíveis ou estourou o limite do brief → handoff com: IDs corrigidos + commits,
`precisa-decisão` pendentes, e arquivos/achados que sobraram.
