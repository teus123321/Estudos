# Lab 02 — Representação do modelo (regressão linear)

**Curso:** Coursera · Aprendizado de Máquina · Curso 1, Semana 1  
**Laboratório original:** [`C1_W1_Lab02_Model_Representation_Soln.ipynb`](C1_W1_Lab02_Model_Representation_Soln.ipynb)  
**Tema:** representar uma reta e usá-la para prever preços de casas.

Este é um guia em português para acompanhar o notebook do curso. O notebook original foi mantido em inglês, com seus exemplos e células. A seguir, explico **todos os tópicos e os principais comandos** na mesma ordem da aula.

## 1. Objetivo da aula

Entender como implementar um modelo de **regressão linear com uma única variável de entrada**:

$$f_{w,b}(x) = wx + b$$

No exercício, a entrada `x` é o **tamanho de uma casa** e a saída prevista é seu **preço**. O objetivo é encontrar uma reta que passe pelos exemplos conhecidos e depois estimar o preço de uma casa nova.

> **Importante:** aqui escolhemos `w` e `b` manualmente. O notebook **não ensina ainda um algoritmo para treinar ou otimizar automaticamente** esses parâmetros.

## 2. Notação utilizada

| Símbolo | Significado | No código |
| --- | --- | --- |
| $a$ | Escalar: um único número. | — |
| $\mathbf{a}$ | Vetor: uma coleção de números. | — |
| $\mathbf{x}$ | Valores de entrada (*features*): tamanhos das casas. | `x_train` |
| $\mathbf{y}$ | Valores reais desejados (*targets*): preços das casas. | `y_train` |
| $x^{(i)}, y^{(i)}$ | Entrada e preço real do exemplo de índice `i`. | `x_i`, `y_i` |
| $m$ | Quantidade de exemplos no conjunto de treinamento. | `m` |
| $w$ | Peso: determina a inclinação da reta. | `w` |
| $b$ | Viés (*bias*): valor em que a reta cruza o eixo vertical (`x = 0`). | `b` |
| $f_{w,b}(x^{(i)})$ | Preço previsto pelo modelo para o exemplo `i`. | `f_wb` |

O sobrescrito `(i)` indica **qual exemplo**, não uma potência. Por exemplo, $x^{(1)}$ é o segundo exemplo, pois os índices de Python começam em zero.

## 3. Bibliotecas usadas

```python
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('./deeplearning.mplstyle')
```

- `NumPy`: cria e manipula os arrays de dados numéricos.
- `Matplotlib`: desenha pontos e retas no gráfico.
- `as np` e `as plt`: definem apelidos para escrever menos.
- `plt.style.use(...)`: carrega o estilo visual específico fornecido no ambiente do curso.

**Atenção ao executar fora do Coursera:** o arquivo `deeplearning.mplstyle` e as imagens `images/...` mencionadas no notebook não vieram no arquivo `.ipynb` enviado. Se você baixar apenas esse laboratório, **comente** a linha `plt.style.use('./deeplearning.mplstyle')` (coloque `#` no início) ou use `plt.style.use('default')`. Os códigos dos exemplos funcionarão, mas as figuras ilustrativas externas da aula não aparecerão. Os gráficos produzidos com Matplotlib são gerados normalmente.

Para instalar as dependências e abrir o notebook no computador:

```bash
python -m pip install notebook numpy matplotlib
jupyter notebook C1_W1_Lab02_Model_Representation_Soln.ipynb
```

## 4. O problema: prever preços de casas

O laboratório fornece apenas **dois exemplos de treinamento**:

| Casa | Tamanho (`x_train`) | Preço (`y_train`) |
| --- | ---: | ---: |
| 1 | 1,0 mil pés² (1.000 sqft) | 300 mil dólares |
| 2 | 2,0 mil pés² (2.000 sqft) | 500 mil dólares |

O modelo recebe tamanhos **em milhares de pés quadrados** e trabalha com preços **em milhares de dólares**. Assim, `1.2` significa 1.200 sqft e um resultado `340` significa US$ 340.000.

### Criar os arrays

```python
x_train = np.array([1.0, 2.0])
y_train = np.array([300.0, 500.0])

print(f"x_train = {x_train}")
print(f"y_train = {y_train}")
```

- `np.array(...)` transforma uma lista Python em um array NumPy.
- A posição `0` de `x_train` corresponde à posição `0` de `y_train`: casa de 1.000 sqft, preço de US$ 300 mil.
- `print(f"... {variavel} ...")` usa uma **f-string**: o Python substitui as chaves pelo valor da variável na hora de imprimir.

Saída esperada:

```text
x_train = [1. 2.]
y_train = [300. 500.]
```

## 5. Quantidade de exemplos: `m`

```python
print(x_train.shape)   # (2,)
m = x_train.shape[0]   # 2

# Outra forma de obter a mesma quantidade:
m = len(x_train)       # 2
```

- `.shape` informa o formato do array. `(2,)` indica **um array de uma dimensão com dois elementos**.
- `.shape[0]` acessa o tamanho da primeira dimensão, ou seja, `2`.
- `len(x_train)` também retorna `2` porque, neste caso, cada posição representa um exemplo de treinamento.

## 6. Acessar um exemplo específico

```python
i = 0
x_i = x_train[i]
y_i = y_train[i]
print(f"(x^({i}), y^({i})) = ({x_i}, {y_i})")
```

Ao usar `i = 0`, acessamos `(1.0, 300.0)`. Ao trocar por `i = 1`, acessamos `(2.0, 500.0)`. `x_train[i]` busca o tamanho e `y_train[i]` busca o preço real da **mesma casa**.

## 7. Colocar os dados no gráfico

```python
plt.scatter(x_train, y_train, marker='x', c='r')
plt.title('Housing Prices')
plt.ylabel('Price (in 1000s of dollars)')
plt.xlabel('Size (1000 sqft)')
plt.show()
```

| Comando | O que faz |
| --- | --- |
| `plt.scatter(x, y)` | Desenha um ponto para cada par `(tamanho, preço)`. |
| `marker='x'` | Usa o formato de uma cruz (`x`) para cada ponto. |
| `c='r'` | Pinta os pontos de vermelho (*red*). |
| `plt.title(...)` | Coloca um título no gráfico. |
| `plt.xlabel(...)` | Nomeia o eixo horizontal: tamanho. |
| `plt.ylabel(...)` | Nomeia o eixo vertical: preço. |
| `plt.show()` | Exibe o gráfico. |

Nesse momento aparecem somente os **dois preços reais conhecidos**, ainda sem uma reta de previsão.

## 8. Como funciona o modelo `f(x) = wx + b`

Em uma reta, `w` define **quanto o preço previsto aumenta quando o tamanho cresce uma unidade do eixo x**. Como o eixo está em milhares de sqft, `w = 200` significa um acréscimo de **US$ 200 mil por 1.000 sqft**.

O parâmetro `b` desloca a reta para cima ou para baixo. Com `b = 100`, a fórmula retorna `100` quando `x = 0`; isso é apenas o intercepto matemático, **não uma previsão realista para uma casa sem área**.

O notebook começa experimentando:

```python
w = 100
b = 100
print(f"w: {w}")
print(f"b: {b}")
```

Com esses valores, as previsões são:

| Tamanho | Preço real | Previsão `100*x + 100` |
| --- | ---: | ---: |
| 1,0 | 300 | 200 |
| 2,0 | 500 | 300 |

**Essa reta ainda está errada**: não passa pelos dois pontos reais.

## 9. Entendendo a função `compute_model_output`

```python
def compute_model_output(x, w, b):
    """Calcula uma previsão para cada tamanho de casa."""
    m = x.shape[0]
    f_wb = np.zeros(m)

    for i in range(m):
        f_wb[i] = w * x[i] + b

    return f_wb
```

Vamos por partes:

1. `def compute_model_output(x, w, b):` cria uma função que recebe os tamanhos e os dois parâmetros da reta.
2. `m = x.shape[0]` descobre quantos tamanhos foram recebidos.
3. `np.zeros(m)` cria um array com `m` posições, inicialmente todas iguais a zero. **Correção de um pequeno erro no texto da aula:** a função é `np.zeros`, no plural, não `np.zero`.
4. `for i in range(m):` percorre os índices `0, 1, ..., m-1`.
5. `f_wb[i] = w * x[i] + b` calcula a previsão de cada casa e armazena na posição correspondente.
6. `return f_wb` devolve o array de preços previstos.

Por exemplo, com `x = [1.0, 2.0]`, `w = 100` e `b = 100`, a função retorna `[200., 300.]`. O uso de um `for` evita escrever a fórmula uma vez para cada casa.

## 10. Comparar previsões e valores reais

```python
tmp_f_wb = compute_model_output(x_train, w, b)

plt.plot(x_train, tmp_f_wb, c='b', label='Our Prediction')
plt.scatter(x_train, y_train, marker='x', c='r', label='Actual Values')

plt.title('Housing Prices')
plt.ylabel('Price (in 1000s of dollars)')
plt.xlabel('Size (1000 sqft)')
plt.legend()
plt.show()
```

- `tmp_f_wb` guarda os preços previstos pela função.
- `plt.plot(...)` **liga as previsões com uma linha azul** (`c='b'`).
- `plt.scatter(...)` desenha **cruzes vermelhas** nas posições dos preços reais.
- `label=...` dá nomes às duas séries.
- `plt.legend()` mostra a legenda para identificar qual é qual.

Se a reta azul não passar pelas cruzes vermelhas, os parâmetros escolhidos não explicam corretamente esses exemplos.

## 11. Desafio: encontrar `w` e `b`

Para a reta passar exatamente pelos dois exemplos, precisamos que:

$$300 = w \cdot 1 + b$$

$$500 = w \cdot 2 + b$$

Subtraindo a primeira equação da segunda:

$$500 - 300 = (2w + b) - (w + b) \Rightarrow w = 200$$

Substituindo na primeira: $300 = 200 + b$, então **$b = 100$**.

```python
w = 200
b = 100

print(compute_model_output(x_train, w, b))
# [300. 500.]
```

Agora as previsões coincidem com os valores reais. Foi essa combinação que a dica (*hint*) do laboratório sugeriu.

## 12. Prever o preço de uma casa de 1.200 sqft

```python
w = 200
b = 100
x_i = 1.2  # 1.200 sqft, pois a escala de x é de milhares

cost_1200sqft = w * x_i + b
print(f"${cost_1200sqft:.0f} thousand dollars")
```

Calculando passo a passo:

$$f(1{,}2) = 200 \times 1{,}2 + 100 = 240 + 100 = 340$$

O valor `340` está na unidade **milhares de dólares**, então a previsão é **US$ 340.000**. O trecho `:.0f` da f-string formata o número com **zero casas decimais**; por isso a impressão fica `$340 thousand dollars`.

## 13. Código completo, simplificado e com comentários em português

Este exemplo reproduz o cálculo e o gráfico do laboratório **sem depender** do arquivo de estilo e das imagens externas do Coursera:

```python
import numpy as np
import matplotlib.pyplot as plt

# Dois exemplos: tamanho (em 1.000 sqft) e preço (em US$ 1.000)
x_train = np.array([1.0, 2.0])
y_train = np.array([300.0, 500.0])

def compute_model_output(x, w, b):
    previsoes = np.zeros(len(x))  # Um espaço para cada casa
    for i in range(len(x)):
        previsoes[i] = w * x[i] + b  # Fórmula da reta
    return previsoes

# Reta que passa pelos dois exemplos
w = 200
b = 100
previsoes = compute_model_output(x_train, w, b)
print('Previsões para os exemplos:', previsoes)  # [300. 500.]

# Desenha reta prevista e pontos reais
plt.plot(x_train, previsoes, c='b', label='Previsão')
plt.scatter(x_train, y_train, marker='x', c='r', label='Preço real')
plt.xlabel('Tamanho (milhares de sqft)')
plt.ylabel('Preço (milhares de US$)')
plt.title('Regressão linear: preço de casas')
plt.legend()
plt.show()

# Previsão para 1.200 sqft
preco = w * 1.2 + b
print(f'Casa de 1.200 sqft: US$ {preco * 1000:,.0f}')
```

## 14. O que você aprendeu — e o que ainda falta

- **Feature:** dado de entrada do modelo, aqui o tamanho da casa.
- **Target:** valor a ser previsto, aqui o preço.
- **Regressão linear:** modelo que relaciona entrada e saída por uma reta.
- **Parâmetros `w` e `b`:** controlam inclinação e posição da reta.
- **Conjunto de treinamento:** exemplos conhecidos usados para ajustar o modelo.
- **Predição:** aplicar o modelo ajustado a um tamanho novo.

Este é um exemplo didático com **apenas duas casas**: conseguir passar exatamente por dois pontos **não garante que as previsões serão boas para casas reais**. Em problemas de verdade, precisaríamos de mais dados, avaliar o erro e aprender os parâmetros automaticamente (assuntos das próximas aulas).

### Para praticar

1. Mude `w` para `150`, mantendo `b = 100`. O que acontece com a inclinação da linha?
2. Mantenha `w = 200` e mude `b` para `50`. A reta fica acima ou abaixo dos pontos reais?
3. Use o modelo `w = 200`, `b = 100` para prever uma casa de 1.500 sqft (`x = 1.5`). **Resposta para conferir:** US$ 400.000.

---

**Nota sobre os arquivos:** o notebook `.ipynb` é o material original enviado do Coursera; este `README.md` é uma explicação de estudo produzida em português. O laboratório usa dólares e pés quadrados porque essas são as unidades do exemplo da aula.
