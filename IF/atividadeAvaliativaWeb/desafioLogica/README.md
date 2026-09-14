# Desafios de Lógica

## contadorVogais

Conta quantas vogais existem em uma frase.

**Situação:** concluído.

## estatistica

A função deve:

- calcular a soma das notas;
- calcular a média da lista;
- informar a quantidade de aprovados;
- informar a quantidade de reprovados.

A nota maior ou igual a 6 deve ser considerada aprovada.

Para calcular a média, divida a soma pela quantidade de notas:

```js
const media = soma / lista.length
```

Com a lista `[6, 10, 8, 3]`:

- Soma: `27`;
- Média: `6.75`;
- Aprovados: `3`;
- Reprovados: `1`.

**Situação:** precisa trocar `soma / 2` por `soma / lista.length` e contar os aprovados e reprovados.

## fizzBuzz

A função deve exibir:

- `Fizz` para números divisíveis por 3;
- `Buzz` para números divisíveis por 5;
- `FizzBuzz` para números divisíveis por 3 e 5;
- o próprio número nos outros casos.

**Melhorias necessárias:**

- começar pelo número 1, se esse for o intervalo solicitado;
- corrigir `FIzz` para `Fizz`;
- confirmar se o limite final deve ser incluído.

## palindromo

A função deve verificar se uma palavra é igual quando lida de trás para frente.

**Correção necessária:** não retornar dentro do primeiro teste do laço. É preciso comparar todas as posições antes de concluir o resultado.

Exemplos:

- `arara` é um palíndromo;
- `Mateus` não é um palíndromo.

## numerosPrimos

A função deve verificar se um número é divisível somente por 1 e por ele mesmo.

**Correção necessária:** atualmente o código verifica apenas se o número é par ou ímpar. Isso não identifica números primos. Por exemplo, `9` é ímpar, mas não é primo.

Também é necessário tratar números menores que 2, pois eles não são primos.

## fibonacci

A função deve gerar a sequência de Fibonacci, em que cada número é a soma dos dois anteriores.

**Melhorias necessárias:**

- decidir se a sequência deve começar com `0`;
- definir se a função deve apenas imprimir ou também retornar a sequência;
- remover o `console.log` externo que exibe `undefined` quando a função não retorna um valor.
