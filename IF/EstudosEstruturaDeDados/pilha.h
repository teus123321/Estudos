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
    NoPilha *atual = pilha->inicio;
    NoPilha *anterior = NULL;
    if(atual == NULL){
        return;
    }
    while(atual->proximo != NULL){
        anterior = atual;
        atual = atual->proximo;
    }
    if(anterior == NULL){
        pilha->inicio = NULL;
    } else {
        anterior->proximo = NULL;
    }
    pilha->fim = anterior;
    free(atual);
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
