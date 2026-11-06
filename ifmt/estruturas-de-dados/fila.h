#ifndef FILA_H
#define FILA_H

#include <stdio.h>
#include <stdlib.h>


typedef struct NoFila{
    int number;
    struct NoFila *proximo;
} NoFila;

typedef struct Fila {
    NoFila *inicio;
    NoFila *fim;
}Fila;

void iniciarFila(Fila *fila){
    fila->inicio = NULL;
    fila->fim = NULL;
}

void inserirNaFila(Fila *fila, int number){
    NoFila *instanciaMemoria = (NoFila *) malloc(sizeof(NoFila));
    instanciaMemoria->number = number;
    instanciaMemoria->proximo = NULL;

    if (fila->fim == NULL) {
        fila->inicio = instanciaMemoria;
    } else {
        fila->fim->proximo = instanciaMemoria;
    }
    fila->fim = instanciaMemoria;
}

void desenfileirar(Fila *fila){
    NoFila *atual = fila->inicio;
    fila->inicio = atual->proximo;
    free(atual);
}

void imprimirFila(Fila *fila){
    NoFila *atual = fila->inicio;
    printf("[");
    while(atual != NULL){
        printf("%d,",atual->number);
        atual = atual->proximo;
    }
    printf("]\n");
}

#endif //UNTITLED1_FILA_H
