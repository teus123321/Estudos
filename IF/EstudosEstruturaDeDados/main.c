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

int estaNaLista(Lista *lista,int number) {
    No *atual = lista->inicio;

    while (atual != NULL) {
        if (atual->number == number) {
            return 1;
        }
        atual = atual->proximo;
    }
}

int main(void) {
    Lista lista;
    iniciarLista(&lista);
    inserir(&lista, 1);
    inserir(&lista, 2);
    inserir(&lista, 4);
    printf("%d\n", estaNaLista(&lista, 6));
    free(&lista);
    return 0;
}
