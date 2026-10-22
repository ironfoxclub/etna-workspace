---
name: etna-blackbox
description: "Acha a causa raiz antes de propor qualquer correção: lê o erro, reproduz, compara o que mudou, mede as fronteiras entre componentes, segue o valor errado até a origem, testa uma hipótese por vez e escreve o teste que falha antes do conserto. Use em qualquer bug, teste quebrado, comportamento instável ou falha de build/integração, antes de mexer no código."
---

# etna-blackbox: causa raiz primeiro

Chute custa horas e ainda cria bug novo. **Nenhum conserto sem investigar a causa raiz.** Enquanto
a Fase 1 não estiver pronta, não existe proposta de correção. Ao começar, avise: "Usando etna-blackbox."

Vale principalmente quando o conserto "parece óbvio", quando você já tentou algo, quando há
pressa e quando você ainda não entendeu a falha.

## Fase 1: investigar a causa raiz

1. **Leia o erro inteiro**: mensagem, pilha, número da linha, código de saída. Muitas vezes ele já diz o que fazer.
2. **Reproduza de forma confiável**, com passos exatos. Não reproduz? Junte mais dados, não adivinhe.
3. **Compare o que mudou**: `git log`, `git diff`, dependências, configuração e a diferença entre o ambiente onde funciona e o onde falha.
4. **Meça as fronteiras** em sistemas de várias peças (CI → build → assinatura; tela → processo de apoio → CLI; API → serviço → banco): registre o que entra e o que sai de cada camada, rode uma vez e descubra ONDE quebra antes de perguntar por quê.
5. **Siga o valor errado de trás pra frente**: de onde ele nasce, quem o repassou, e assim até a fonte. Conserte na fonte, nunca no sintoma.

## Fase 2: padrão

Ache, neste mesmo projeto, um código que faz algo parecido e funciona. Leia a referência inteira,
sem passar o olho. Liste toda diferença, por menor que seja, e as dependências e suposições.

## Fase 3: hipótese

Uma hipótese só, escrita: "X é a causa raiz porque Y". Teste com a MENOR mudança possível, uma
variável por vez. Não confirmou? Nova hipótese; nunca empilhe consertos. Não sabe? Diga "não
entendo X" e busque mais dados.

## Fase 4: conserto

1. **Teste que falha primeiro**: a reprodução mais simples, automatizada se houver ferramenta de teste (senão, um script avulso). Ele existe ANTES do conserto.
2. **Um conserto só**, pra causa raiz. Sem refatoração junto, sem "já que estou aqui".
3. **Confira**: o teste passa, nada mais quebrou e o sintoma original sumiu (`etna-stamp`).
4. **Não resolveu?** Conte as tentativas. Menos de 3: volte à Fase 1 com o que aprendeu. **3 ou mais consertos que falharam indicam que a arquitetura está errada**, não a hipótese: pare, descreva o padrão (cada conserto revela acoplamento em outro lugar) e converse antes da tentativa 4.

## Sinais de alerta: pare e volte à Fase 1

"Conserto rápido agora, investigo depois" · "vou só tentar mudar X" · várias mudanças e só então
rodar os testes · "pulo o teste, confiro na mão" · "deve ser X" · propor conserto antes de rastrear
o dado · "mais uma tentativa" depois de duas falhas · cada conserto revela um problema novo em outro lugar.

| Desculpa | Realidade |
|---|---|
| É simples | Bug simples também tem causa raiz; o método é rápido nesses casos |
| Emergência, sem tempo | Seguir o método é mais rápido que ficar no chute |
| Testo depois do conserto | Conserto sem teste não se sustenta; o teste prova a causa |
| Vários consertos de uma vez | Não dá pra saber o que funcionou, e nascem bugs novos |
| Já vi o problema | Ver o sintoma não é conhecer a causa |

## Quando realmente não há causa raiz

Casos de ambiente, de tempo ou de serviço externo: registre o que investigou, trate de forma
deliberada (nova tentativa, limite de tempo, mensagem de erro clara) e deixe o log ou monitor que
pegaria da próxima vez. A maioria dos "sem causa raiz" é investigação incompleta.

## No Etna

- O projeto guarda bugs num quadro ou em findings? Registre o bug (sintoma, ambiente, reprodução, hipótese) ANTES do conserto; o commit do conserto cita o id.
- Trabalhando num painel com colegas: não mexa em arquivo que é de outro worker; relate o acoplamento.
