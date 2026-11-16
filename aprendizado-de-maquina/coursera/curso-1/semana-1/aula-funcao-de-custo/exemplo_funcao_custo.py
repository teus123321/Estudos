"""Exemplo didático da função de custo da regressão linear (Coursera)."""

import numpy as np
import matplotlib.pyplot as plt


# Nosso conjunto de treinamento tem 3 exemplos.
# Para cada entrada x, temos o valor correto y correspondente.
x_train = np.array([1.0, 2.0, 3.0])
y_train = np.array([1.0, 2.0, 3.0])


def prever(x, w):
    """Calcula a previsão f(x) = w * x para cada valor de entrada."""
    return w * x  # NumPy multiplica todos os elementos do array por w.


def calcular_custo(x, y, w):
    """Calcula J(w): a soma dos erros ao quadrado dividida por 2*m."""
    m = len(x)  # Quantidade de exemplos de treinamento (aqui, 3).
    previsoes = prever(x, w)  # O que a reta prevê para cada x.
    erros = previsoes - y  # Diferença entre previsão e valor real.
    erros_ao_quadrado = erros ** 2  # Deixa os erros não negativos.
    soma_dos_erros = np.sum(erros_ao_quadrado)  # Soma os 3 erros.
    return soma_dos_erros / (2 * m)  # Fórmula da função de custo.


# Compara várias inclinações possíveis da reta.
for w in [-0.5, 0, 0.5, 1, 1.5, 2]:
    custo = calcular_custo(x_train, y_train, w)
    print(f"w = {w:4.1f} | J(w) = {custo:.4f}")


# Primeiro gráfico: valores reais contra a reta de previsão com w = 0.5.
figura, (grafico_reta, grafico_custo) = plt.subplots(1, 2, figsize=(12, 5))
w_escolhido = 0.5
grafico_reta.scatter(x_train, y_train, color="red", marker="x", s=80,
                    label="Valores reais")
grafico_reta.plot(x_train, prever(x_train, w_escolhido), color="blue",
                 label="Previsão com w = 0,5")
grafico_reta.set_title("f(x): previsão em função de x")
grafico_reta.set_xlabel("Entrada x")
grafico_reta.set_ylabel("Saída prevista / valor real")
grafico_reta.legend()
grafico_reta.grid(alpha=0.3)


# Segundo gráfico: testamos 150 valores de w e calculamos o custo de cada um.
valores_w = np.linspace(-0.5, 2.5, 150)
valores_custo = [calcular_custo(x_train, y_train, w) for w in valores_w]
grafico_custo.plot(valores_w, valores_custo, color="darkorange")

# Marca os três valores discutidos na aula: 0, 0.5 e 1.
for w in [0, 0.5, 1]:
    grafico_custo.scatter(w, calcular_custo(x_train, y_train, w), color="purple")

grafico_custo.set_title("J(w): custo em função de w")
grafico_custo.set_xlabel("Parâmetro w")
grafico_custo.set_ylabel("Custo J(w)")
grafico_custo.grid(alpha=0.3)

plt.tight_layout()  # Ajusta os espaços entre os gráficos.
plt.show()  # Exibe a janela; em Jupyter, exibe o gráfico na célula.
