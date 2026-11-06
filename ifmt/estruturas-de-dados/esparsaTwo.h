
#ifndef UNTITLED1_ESPARSATWO_H
#define UNTITLED1_ESPARSATWO_H

#include <stdlib.h>
#include <stdbool.h>

typedef struct NoSparsaTwo {
    float valor;
    int coluna;
    struct NoSparsaTwo *proximo;
} NoSparsaTwo;

typedef struct MatrizSparsaTwo {
    NoSparsaTwo **matriz;
    int linha;
    int coluna;
} MatrizSparsaTwo;

// Inicializa a matriz
static inline bool iniciarMatrizTwo(MatrizSparsaTwo *matriz, int linha, int coluna) {
    if (matriz == NULL || linha <= 0 || coluna <= 0)
        return false;

    matriz->linha = linha;
    matriz->coluna = coluna;

    matriz->matriz = calloc(linha, sizeof(NoSparsaTwo *));

    return matriz->matriz != NULL;
}

// Insere, atualiza ou remove um valor
static inline bool AtribuirValorMatrizTwo(MatrizSparsaTwo *matriz, int linha, int coluna, float valor) {
    if (matriz == NULL || matriz->matriz == NULL ||
        linha < 0 || linha >= matriz->linha ||
        coluna < 0 || coluna >= matriz->coluna) {
        return false;
    }

    NoSparsaTwo *ant = NULL;
    NoSparsaTwo *atual = matriz->matriz[linha];

    // Procura a posição correta
    while (atual != NULL && atual->coluna < coluna) {
        ant = atual;
        atual = atual->proximo;
    }

    // A coluna já existe
    if (atual != NULL && atual->coluna == coluna) {
        if (valor == 0) {
            if (ant == NULL)
                matriz->matriz[linha] = atual->proximo;
            else
                ant->proximo = atual->proximo;

            free(atual);
        } else {
            atual->valor = valor;
        }
    }
    // Coluna não existe: inserir novo nó
    else if (valor != 0) {
        NoSparsaTwo *novo = malloc(sizeof(NoSparsaTwo));

        if (novo == NULL)
            return false;

        novo->valor = valor;
        novo->coluna = coluna;
        novo->proximo = atual;

        if (ant == NULL)
            matriz->matriz[linha] = novo;
        else
            ant->proximo = novo;
    }

    return true;
}

// Consulta o valor de uma posição
static inline float acessarValorMatrizTwo(const MatrizSparsaTwo *matriz, int linha, int coluna) {
    if (matriz == NULL || matriz->matriz == NULL ||
        linha < 0 || linha >= matriz->linha ||
        coluna < 0 || coluna >= matriz->coluna) {
        return 0;
    }

    NoSparsaTwo *atual = matriz->matriz[linha];

    while (atual != NULL && atual->coluna < coluna) {
        atual = atual->proximo;
    }

    if (atual != NULL && atual->coluna == coluna)
        return atual->valor;

    return 0;
}

// Libera toda a memória alocada
static inline void liberarMatrizTwo(MatrizSparsaTwo *matriz) {
    if (matriz == NULL || matriz->matriz == NULL)
        return;

    for (int i = 0; i < matriz->linha; i++) {
        NoSparsaTwo *atual = matriz->matriz[i];

        while (atual != NULL) {
            NoSparsaTwo *proximo = atual->proximo;
            free(atual);
            atual = proximo;
        }
    }

    free(matriz->matriz);
    matriz->matriz = NULL;
    matriz->linha = 0;
    matriz->coluna = 0;
}

#endif // UNTITLED1_ESPARSATWO_H
