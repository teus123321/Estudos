#include <stdio.h>
#include <stdlib.h>

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
    printf("[\n");
    while (atual != NULL) {
        printf("%d\n", atual->number);
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
}

void trocarIndice(Lista *lista, int indexOne, int indexTwo) {
    No *aux = lista->inicio;

    while (aux != NULL) {
        if (aux->number == indexOne) {
            aux->number = indexTwo;
            indexTwo = indexOne;
        }
        if (aux->number == indexTwo) {
            aux->number = indexOne;
        }
        aux = aux->proximo;
    }
}


int main(void) {
    Lista lista;
    iniciarLista(&lista);
    inserir(&lista, 1);
    inserir(&lista, 2);
    inserir(&lista, 4);
    printf("%d\n", estaNaLista(&lista, 6));
    imprimirLista(&lista);
    trocarIndice(&lista,2,4);
    imprimirLista(&lista);
    free(&lista);
    return 0;
}
