#ifndef UNTITLED1_PILHA_H
#define UNTITLED1_PILHA_H
#endif //UNTITLED1_PILHA_H
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
    instanciaMemoria->proximo = pilha->inicio;
    pilha->inicio = instanciaMemoria;
    pilha->inicio->number = number;
}

void desempilhar(Pilha *pilha){

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