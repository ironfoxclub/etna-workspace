---
name: etna-image-assets
description: >
  Gera rápido imagens simples e próprias via etna_imagem_gerar: espaços de imagem de site
  (cards, galeria, fundos), sprites e texturas de jogo, ilustrações de app, fotos de produto.
  É a irmã enxuta da etna-cinema-shot: sem vídeo, sem coreografia de câmera, sem encadeamento
  de cenas. Cuida do bloco de estilo travado (consistência visual entre N imagens geradas em
  paralelo), da regra do assunto literal, da escolha de provedor e do filtro de segurança
  resumido. Use para qualquer imagem NÃO cinematográfica. Para vídeo, hero com rolagem ou
  continuidade entre planos, carregue etna-cinema-shot / etna-site-scrub. Gatilhos: asset,
  sprite, textura, imagem de card, imagem de galeria, ilustração, imagem simples, lote de
  imagens, style-lock.
---

# etna-image-assets: imagens rápidas, baratas e consistentes

Uma ferramenta, um trabalho: `etna_imagem_gerar(prompt, outPath, provider?, imageUrl?, formato?)` → caminho
do png. Não existem outros parâmetros. Proporção e formato entram DENTRO do prompt, em linguagem
de estilo.

## Provedor: decida em uma linha

| Imagem | Provedor |
|---|---|
| Cena, personagem, comida, produto, textura, pintura, sprite estilizado | `antigravity` |
| Layout, diagrama, ícone chapado, qualquer coisa com TEXTO legível | `openai` |

Nunca troque de provedor pra fugir de uma falha: falha é problema de prompt.

## As 5 regras (todas inegociáveis)

1. **Assunto literal.** Gere o que a marca ou o jogo É: a salsicha do cachorro-quente, o espetinho do jogo de churrasco. Teste dos 2 segundos: sem legenda, qualquer pessoa nomeia o assunto.
2. **Estilo travado em lote.** N imagens geradas em paralelo por workers que não se enxergam resultam em estilos que se afastam. ANTES de abrir os workers, o orquestrador escreve UM Bloco de Estilo e cada worker o cola IGUAL no fim do próprio prompt:
   ```
   Style Block: <estética nomeada, ex.: "flat pixel-art 32px, paleta terrosa #C8553D/#F5F0EB,
   contorno grosso, luz única no canto superior esquerdo, fundo transparente">
   ```
   Prompt do worker = [assunto + ação/pose desta imagem] + [Bloco de Estilo igual ao original].
   Sem Bloco de Estilo compartilhado, NÃO abra em paralelo: gere em sequência, usando como
   referência de estilo (imagem para imagem) a `imageUrl` da primeira.
3. **Tratamento de cor da marca.** Paleta e luz da imagem combinam com o fundo do site ou do jogo (use os tokens do design-dna quando existirem). Imagem "colada por cima" deve ser refeita.
4. **Texto nítido fica no código.** Modelo de difusão inventa tipografia: logotipo, título, número e preço NUNCA entram na geração; componha com CSS/canvas por cima.
5. **Material do cliente primeiro.** Foto real de produto fornecida vale mais que qualquer geração.

## Filtro de segurança (resumido: rode ANTES de cada geração)

Qualquer FALHA = não gere; reescreva.

- **F1 nome de pessoa real** (celebridade, figura pública) → troque por um arquétipo: idade, porte, cabelo, roupa.
- **F2 marca, IP ou franquia** (nike, disney, pokémon, iphone...) → descreva geometria, cor e material, nunca o nome.
- **F3 verbo de violência** (kill, stab, blood, fight, punch...) → descreva o resultado, a força ou a direção, não o ato.
- **F4 arma nomeada** (gun, knife, sword, bomb...) → silhueta ou geometria do objeto, não o nome.
- **F5 marca de idade ou menor** (child, kid, boy, girl, teen...) → papel + roupa + ação: "a figure in a wool cloak".
- **F6 mais de 220 palavras** → corte para 30–120 (imagem simples não precisa de mais).

AVISO (endureça e siga): adjetivo de marketing (stunning, breathtaking, epic...) → troque por um detalhe observável.

## Receita de prompt (30–80 palavras, nesta ordem)

```
[Assunto literal + pose/estado] + [contexto mínimo] + [Bloco de Estilo igual ao original] +
[formato: "square 1:1" / "wide 16:9" / "transparent background"]
```

Exemplo (espaço de site, barbearia):
> A vintage barber chair in worn leather, three-quarter view, empty, waiting.
> Style Block: warm amber key light, deep green backdrop #1B2D2A, muted film grade,
> shallow depth. Wide 16:9.

Exemplo (sprite de jogo, lote com estilo travado):
> A skewer of grilled meat, held diagonally, slight char glow.
> Style Block: flat pixel-art 32px, earthy palette #C8553D/#F5F0EB, thick outline,
> single top-left light, transparent background. Square 1:1.

O prompt vai em inglês (os modelos de imagem respondem melhor); o resto da conversa, em português.

## Fluxo do worker

1. Recebe: o assunto da imagem + o Bloco de Estilo (obrigatório em lote) + o outPath.
2. Escreve o prompt pela receita e roda o filtro; deu FALHA? Reescreve.
3. `etna_imagem_gerar(prompt, provider, outPath)`.
4. OLHA o png gerado (Read). Assunto errado, estilo desviado, texto inventado: 1 nova tentativa com o prompt corrigido. Na 2ª falha, relata a lacuna e não insiste (nada de força bruta).
5. Devolve o caminho + uma linha do que gerou.

## Origem

Skill original do Etna. Resume a doutrina de geração da `etna-cinema-shot` (também nossa) para o
caso não cinematográfico e acrescenta o contrato de estilo travado para geração em paralelo.
Nenhum texto ou código de terceiros foi reproduzido.
