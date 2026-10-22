---
name: etna-stamp
description: "Prova antes de qualquer afirmação de pronto, consertado, passando ou entregue: ache o comando que prova, rode de novo, leia a saída inteira e o código de saída, só então diga o resultado com a prova. Use antes de commit, envio, entrega de card, abrir PR ou dizer a alguém que algo funciona."
---

# etna-stamp: prova antes de afirmar

Dizer que o trabalho está completo sem rodar a prova é desonestidade, não eficiência. **Nenhuma
afirmação de conclusão sem prova fresca, produzida neste mesmo turno.**

## O portão: antes de qualquer status, alívio ou "pronto"

1. **Identifique** o comando que prova a afirmação.
2. **Rode** inteiro e agora (não vale a rodada de dez minutos atrás).
3. **Leia** a saída toda: código de saída, linha de contagem, cada falha.
4. **Compare:** a saída confirma? Não → relate o estado real com a prova. Sim → afirme COM a
   prova (comando, código de saída, contagens).

Pular uma etapa é chute, não conferência.

| Afirmação | Exige | Não basta |
|---|---|---|
| Testes passam | a saída do comando de teste, 0 falhas | rodada antiga, "deve passar" |
| Tipos ou lint limpos | a saída, 0 erros | rodada parcial, extrapolar |
| Build funciona | build com saída 0 | o lint passou, o log "parece bom" |
| Bug consertado | o sintoma original refeito e sumido | mexi no código, presumo que resolveu |
| Teste de regressão serve | vermelho → verde comprovado (falha sem o conserto) | o teste passou uma vez |
| Worker ou agente terminou | o diff e os arquivos conferidos | o agente disse "sucesso" |
| Requisitos cumpridos | lista linha a linha contra a especificação ou o card | testes passando |
| Entregue | commit alcançável no remoto, id citado | pasta com alterações soltas |

## Sinais de alerta

"deve", "provavelmente", "parece" · "Pronto!" antes de rodar qualquer coisa · commit, envio ou PR
sem prova · confiar no relato de outro painel · conferência parcial · "só desta vez" · cansaço e
vontade de acabar.

| Desculpa | Realidade |
|---|---|
| Estou confiante | Confiança não é prova |
| O lint passou | Lint ≠ compilador ≠ testes |
| O agente disse que deu certo | Confira por conta própria: `git diff`, rode |
| Conferência parcial basta | Parcial não prova nada |

## Modelos prontos

- Testes: rodar → ver `34/34 passaram` → "todos os testes passam (34/34, saída 0)".
- Regressão: escrever o teste → passa → desfazer o conserto → TEM que falhar → restaurar → passa.
- Requisitos: reler a especificação ou o card → lista → conferir cada linha → relatar o que falta ou o que fechou.
- Versão ou build: o artefato existe, o número da versão é o novo, o instalador abre num computador que não é o seu.

## No Etna

- No handoff, `evidence.commands` leva `{cmd, exitCode}` e `evidence.tested` diz como foi
  provado; o `summary` dá a conclusão, não o esforço.
- Entrega de card cita o commit e a conferência. Pasta com alterações soltas não é entrega.
