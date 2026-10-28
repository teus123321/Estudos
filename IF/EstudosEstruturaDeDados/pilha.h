#ifndef UNTITLED1_PILHA_H
#define UNTITLED1_PILHA_H
#include <stdio.h>
#include <stdlib.h>


//lista encadeada
typedef struct NoPilha{
    int number;
    struct NoPilha *proximo;
} NoPilha;

typedef struct Pilha {
    NoPilha *inicio;
    NoPilha *fim;
}Pilha;

void iniciarPilha(Pilha *pilha){
    pilha->inicio = NULL;
    pilha->fim = NULL;
}

void inserirNaPilha(Pilha *pilha, int number){
    NoPilha *instanciaMemoria = (NoPilha *) malloc(sizeof(NoPilha));
    instanciaMemoria->number = number;
    instanciaMemoria->proximo = NULL;
    if(pilha->fim == NULL){
        pilha->inicio = instanciaMemoria;
    } else {
        pilha->fim->proximo = instanciaMemoria;
    }
    pilha->fim = instanciaMemoria;
}

void desempilhar(Pilha *pilha){
    if(pilha == NULL) {
        printf("Pilha vazia");
    };
    NoPilha *aux = pilha->inicio;

    if(aux == pilha->fim){
        free(pilha->fim);
        pilha->inicio = NULL;
        pilha->fim = NULL;
        return;
    }

    while(aux->proximo != pilha->fim){
        aux = aux->proximo;
    }

    free(pilha->fim);
    pilha->fim = aux;
    pilha->fim->proximo = NULL;
}

void imprimirPilha(Pilha *pilha){
    NoPilha *atual = pilha->inicio;
    printf("[");
    while(atual != NULL){
        printf("%d,",atual->number);
        atual = atual->proximo;
    }
    printf("]\n");
}
#endif //UNTITLED1_PILHA_H
