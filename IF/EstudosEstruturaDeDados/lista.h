#ifndef UNTITLED1_LISTA_H
#define UNTITLED1_LISTA_H
#endif //UNTITLED1_LISTA_H
#include <stdio.h>
#include <stdlib.h>

//lista encadeada
typedef struct No{
    int number;
    struct No *proximo;
} No;

typedef struct Lista {
    No *inicio;
} Lista;


void iniciarLista(Lista *lista) {
    lista->inicio = NULL;
}
void inserir(Lista *lista, int number) {
    No *instanciaMemoria = (No *) malloc(sizeof(No));
    instanciaMemoria->proximo = lista->inicio;
    lista->inicio = instanciaMemoria;
    lista->inicio->number = number;

}

void imprimirLista(Lista *lista) {
    No *atual = lista->inicio;
    printf("[");
    while (atual != NULL) {
        printf("%d", atual->number);
        atual = atual->proximo;
    }
    printf("]\n");
}

int estaNaLista(Lista *lista,int number) {
    No *atual = lista->inicio;

    while (atual != NULL) {
        if (atual->number == number) {
            return 1;
        }
        atual = atual->proximo;
    }
    return 0;
}

void trocarIndice(Lista *lista, int indexOne, int indexTwo) {
    No *aux = lista->inicio;
    No *auxOne = NULL;
    No *auxTwo = NULL;

    int i = 0;
    while (aux != NULL) {
        if (i == indexOne) {
            auxOne = aux;
        }
        if (indexTwo = indexTwo) {
            auxTwo = aux;
        }
        aux = aux->proximo;
        i++;

        if (auxOne != NULL && auxTwo != NULL) {
            int temporario = auxOne->number;
            auxOne->number = auxTwo->number;
            auxTwo->number = temporario;
        }
    };
}

void inverterFila(Lista *lista) {
    No *anterior = NULL;
    No *atual = lista->inicio;
    No *proximo = NULL;


    while (atual != NULL) {
        proximo = atual->proximo;
        atual->proximo = anterior;
        anterior = atual;
        atual = proximo;
    }
    lista->inicio = anterior;
}