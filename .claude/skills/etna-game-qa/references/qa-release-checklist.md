# Checklist de QA e lançamento: jogo web

Consulte antes de declarar um jogo de navegador completo, premium, pronto para lançar ou corrigido.

## Matriz mínima de QA

- Dependências instaladas ou conhecidas.
- Build e checagem de tipos passando.
- Servidor de desenvolvimento ou de pré-visualização no ar, na URL certa.
- Console, página e rede sem erro capturado.
- Canvas que não é branco e tem variação real de pixels (não basta "não ser preto").
- Captura de desktop em jogo ativo.
- Captura de celular em jogo ativo quando o celular está no escopo.
- A entrada principal muda o estado real do jogo.
- O caminho do objetivo e da progressão funciona.
- Falha/nova tentativa ou pausa/retomada funciona, quando se aplica.
- O caminho de código recente ou de risco foi disparado.
- Jogo com física: motor, passo fixo, contagem de corpos e colisores, caminho de colisão/gatilho, checagem de atravessamento em alta velocidade, limpeza dos corpos no recomeço.
- Texto do HUD sem sobreposição; área segura e área de toque conferidas quando a interface mudou.
- Diagnóstico do renderizador capturado quando a complexidade gráfica mudou.
- Caminho, tamanho e comportamento de carga do recurso importado ou gerado conferidos quando mudaram.
- Áudio: desbloqueio por gesto, decodificação e carga, limpeza do laço, mudo e volume, efeito principal.
- Decisão sobre o conjunto de regressão visual registrada quando o trabalho é premium, de lançamento, pesado em interface ou em recurso gerado, ou propenso a regressão.

## QA de interação (o que o jogador realmente faz)

- Começar e retomar.
- Mover, mirar, pilotar, pular, atacar ou acelerar, conforme o gênero.
- Coletar ou pontuar.
- Evitar ou acertar um perigo.
- Disparar mudança de estado: combo, onda, ponto de retorno, dano, escudo, falha, vitória.
- Pausar e retomar.
- Recomeçar depois de uma falha: o corpo de física zera limpo, sem corpo fantasma simulando.
- Redimensionar e girar a tela quando o responsivo ou o celular está no escopo.

Gameplay não se valida só por captura de tela.

## QA visual

Para pedido premium, AAA, vitrine ou "menos genérico":

- Captura em jogo ativo antes e depois, quando possível.
- Falhas automáticas a vigiar: cena dominada por forma primitiva, mundo raso de plano e caixa, HUD genérico de cartão de estatística, mesma silhueta de obstáculo ou recompensa repetida, neblina, brilho ou escuridão escondendo geometria que falta, ausência de diagnóstico do renderizador.
- Interface e efeitos não podem encobrir a ameaça, a recompensa, o jogador nem a próxima decisão.
- O enquadramento de desktop e de celular mostra o caminho jogável, não só a composição.
- Recurso 3D gerado: escala, orientação, legibilidade do material, colisor simplificado e clipe de animação corretos durante o gameplay ativo, não só na pré-visualização parada.

## QA de celular

- O controle por toque emite intenção de jogo real.
- Soltar, cancelar ou perder o foco do ponteiro nunca deixa um controle travado.
- Área segura respeitada.
- Área de toque alcançável e separada da vizinha.
- A rolagem da página não rouba a entrada do gameplay.
- Orientação e redimensionamento preservam canvas e HUD.
- Resolução e desempenho aceitáveis no perfil de celular real, não só emulado.
- A entrada de desktop continua funcionando, a menos que tenha sido removida de propósito.
- Interface legível em tela estreita.

## QA de desempenho

Quando chamadas de desenho, quantidade de recursos, shaders, sombras ou pós-processamento mudaram:

- Registre as chamadas do renderizador, os triângulos, as geometrias e as texturas.
- Registre FPS e tempo de quadro reais (não sem janela; veja a seção do teste por robô no SKILL.md).
- Física: motor, passo, contagem de corpos e colisores, sensores ativos, corpos com CCD, colisor caro conhecido.
- Limite de DPR e configuração de pós-processamento e sombras.
- Meça em gameplay ativo, não só na tela parada.
- Compare antes e depois quando o pedido era de desempenho.
- Relate com honestidade o risco que não foi medido; nunca invente número.

## Verificações de lançamento

Antes de declarar pronto para lançar:

- O build de produção passa.
- A pré-visualização ou o servidor estático de produção foi testado (não só o servidor de desenvolvimento).
- O caminho-base e a URL dos recursos do empacotador batem com a hospedagem de destino.
- Interface gráfica de depuração, sobreposição de diagnóstico, log detalhado e atalho de teste estão atrás de flag ou removidos do build voltado ao jogador.
- Pacote e recursos grandes revisados.
- Nenhuma chave de API em código do lado do cliente, arquivo versionado, recurso compilado ou variável de ambiente visível no navegador.
- Nota de licença ou origem presente para qualquer recurso de terceiros (modelo, textura, efeito sonoro, fonte) que não foi gerado pelo próprio projeto.
- Os recursos públicos carregam sob a premissa real de hospedagem estática.
- Premissa de suporte de navegadores documentada.
- Comando de publicação, ou local do artefato estático, informado.
- Riscos que sobraram listados.

## Formato da evidência

```text
Resultado do QA: passou/falhou
Comandos:
URL:
Controles testados:
Capturas/artefatos:
Erros de console/página/rede:
Checagem de pixels do canvas:
Tamanhos de tela desktop/celular:
Diagnóstico de renderização/desempenho:
Conjunto visual:
Diagnóstico de física:
Evidência de recurso externo:
Evidência de áudio:
Findings (card F-XXX):
Riscos que sobraram:
```

## Falhas de lançamento mais comuns

- Testar em desenvolvimento e publicar produção sem reverificar.
- O caminho-base da hospedagem estática quebra os recursos.
- Interface de depuração visível ao jogador.
- No celular passa na captura de tela, mas o controle não responde.
- Canvas que não é branco, mas é o app errado rodando naquela porta.
- A física parece certa visualmente, mas colisor, sensor e limpeza do recomeço não foram testados.
- A captura é da tela de título ou parada, não de jogo ativo.
- Afirmação de premium sem avaliação visual nem diagnóstico do renderizador.
- Chave de API de geração 3D, de imagem ou de áudio, ou URL temporária, exposta em código do cliente.
