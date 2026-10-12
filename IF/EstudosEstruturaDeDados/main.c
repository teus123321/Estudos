#include <stdio.h>
#include "fila.h"
#include "pilha.h"
#include "lista.h"
#include "esparsa.h"
#include "esparsaTwo.h"

static inline float somaMatriz(MatrizSparsa *matriz, MatrizSparsaTwo *matrizTwo, int linha, int coluna,int linhaTwo, int colunaTwo) {
    if (
        matriz == NULL || matriz->matriz == NULL ||
        linha < 0 || linha >= matriz->linha ||
        coluna < 0 || coluna >= matriz->coluna ||
        matrizTwo == NULL || matrizTwo->matriz == NULL ||
        linhaTwo < 0 || linhaTwo >= matrizTwo->linha ||
        coluna < 0 || colunaTwo >= matrizTwo->coluna
        ) {
            return 0;
        }
    NoSparsa *atual = matriz->matriz[linha];
    NoSparsaTwo *atualTwo = matrizTwo->matriz[linhaTwo];
    while (
        atual != NULL && atualTwo != NULL &&
        atual->coluna < coluna &&
        atualTwo->coluna < colunaTwo
        ) {
        atual = atual->proximo;
        atualTwo = atualTwo->proximo;
        }
    if (atual != NULL && atual->coluna == coluna && atualTwo != NULL && atualTwo->coluna == colunaTwo) {
        float numero = atual->valor;
        float numeroTwo = atualTwo->valor;
        float soma = numero + numeroTwo;
        return soma;
    }
    return 0;
}

int main(void) {

    /*
    //lista
    Lista lista;
    iniciarLista(&lista);
    inserir(&lista, 1);
    inserir(&lista, 2);
    inserir(&lista, 4);
    printf("%d\n", estaNaLista(&lista, 2));
    imprimirLista(&lista);
    trocarIndice(&lista,1,2);
    imprimirLista(&lista);
    inverterFila(&lista);
    imprimirLista(&lista);
    free(&lista);
    printf("Fila :\n");
    Fila fila;
    iniciarFila(&fila);
    inserirNaFila(&fila, 1);
    inserirNaFila(&fila, 2);
    imprimirFila(&fila);
    desenfileirar(&fila);
    imprimirFila(&fila);
    printf("Pilha :\n");
    Pilha pilha;
    iniciarPilha(&pilha);
    inserirNaPilha(&pilha, 1);
    inserirNaPilha(&pilha, 2);
    imprimirPilha(&pilha);
    */

    MatrizSparsa matriz;
    MatrizSparsaTwo matrizTwo;

    iniciarMatriz(&matriz, 2,2);
    iniciarMatrizTwo(&matrizTwo, 2,2);

    // Primeira matriz
    AtribuirValorMatriz(&matriz, 0, 0, 3);
    AtribuirValorMatriz(&matriz, 1, 1, 3);

    // Segunda matriz
    AtribuirValorMatrizTwo(&matrizTwo, 0, 1, 3);
    AtribuirValorMatrizTwo(&matrizTwo, 1, 0, 3);

    printf("%.2f\n", acessarValorMatriz(&matriz,0,0));
    printf("%.2f\n", acessarValorMatrizTwo(&matrizTwo,1,0));
    printf("%.2f\n",somaMatriz(&matriz,&matrizTwo,0,0,1,0));

    liberarMatriz(&matriz);
    liberarMatrizTwo(&matrizTwo);
    return 0;
}
