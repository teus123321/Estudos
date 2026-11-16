#include <stdio.h>
#include <stdlib.h>

// Mostra todos os elementos do vetor na tela.
void imprimirVetor(const int vetor[], int tamanho) {
    for (int posicao = 0; posicao < tamanho; posicao++) {
        printf("%d ", vetor[posicao]);
    }
    printf("\n");
}

// MERGE: junta duas metades ja ordenadas em uma unica parte ordenada.
// A metade esquerda vai de inicio ate meio.
// A metade direita vai de meio + 1 ate fim.
void merge(int vetor[], int inicio, int meio, int fim) {
    int quantidade = fim - inicio + 1;
    int *temporario = malloc(quantidade * sizeof(int));

    if (temporario == NULL) {
        fprintf(stderr, "Erro ao reservar memoria.\n");
        exit(EXIT_FAILURE);
    }

    int indiceEsquerda = inicio;
    int indiceDireita = meio + 1;
    int indiceTemporario = 0;

    // Compara as duas metades e guarda o menor elemento primeiro.
    while (indiceEsquerda <= meio && indiceDireita <= fim) {
        if (vetor[indiceEsquerda] <= vetor[indiceDireita]) {
            temporario[indiceTemporario] = vetor[indiceEsquerda];
            indiceEsquerda++;
        } else {
            temporario[indiceTemporario] = vetor[indiceDireita];
            indiceDireita++;
        }
        indiceTemporario++;
    }

    // Copia os elementos que sobrarem na metade esquerda.
    while (indiceEsquerda <= meio) {
        temporario[indiceTemporario] = vetor[indiceEsquerda];
        indiceEsquerda++;
        indiceTemporario++;
    }

    // Copia os elementos que sobrarem na metade direita.
    while (indiceDireita <= fim) {
        temporario[indiceTemporario] = vetor[indiceDireita];
        indiceDireita++;
        indiceTemporario++;
    }

    // Coloca os valores ordenados de volta no vetor original.
    for (int posicao = 0; posicao < quantidade; posicao++) {
        vetor[inicio + posicao] = temporario[posicao];
    }

    free(temporario); // Libera a memoria usada pelo vetor temporario.
}

// MERGE SORT: divide o vetor em metades ate restar um elemento por parte.
void mergeSort(int vetor[], int inicio, int fim) {
    if (inicio >= fim) {
        return; // Uma parte com 0 ou 1 elemento ja esta ordenada.
    }

    int meio = inicio + (fim - inicio) / 2;

    mergeSort(vetor, inicio, meio);    // Ordena a metade esquerda.
    mergeSort(vetor, meio + 1, fim);   // Ordena a metade direita.
    merge(vetor, inicio, meio, fim);   // Junta as duas metades ordenadas.
}

int main(void) {
    int numeros[] = {38, 27, 43, 3, 9, 82, 10};
    int tamanho = sizeof(numeros) / sizeof(numeros[0]);

    printf("Antes:  ");
    imprimirVetor(numeros, tamanho);

    mergeSort(numeros, 0, tamanho - 1);

    printf("Depois: ");
    imprimirVetor(numeros, tamanho);

    return 0;
}
