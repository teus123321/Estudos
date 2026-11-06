from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def main():
    pixels, digitos = load_digits(return_X_y=True)
    x_treino, x_teste, y_treino, y_teste = train_test_split(
        pixels, digitos, test_size=0.2, stratify=digitos, random_state=42
    )

    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(x_treino, y_treino)
    previsoes = modelo.predict(x_teste)

    print(f"Acurácia em {len(y_teste)} imagens de teste: {accuracy_score(y_teste, previsoes):.1%}")
    print("Matriz de confusão (linhas = real, colunas = previsto, dígitos de 0 a 9)")
    print(confusion_matrix(y_teste, previsoes, labels=range(10)))


if __name__ == "__main__":
    main()
