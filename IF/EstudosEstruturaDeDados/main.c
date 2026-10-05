#include <stdio.h>

typedef struct No{
    int number;
    struct No *proximo;
} No;

typedef struct Lista {
    No *cabecalho;
} Lista;


void iniciarLista(Lista *lista) {
    lista->cabecalho = NULL;
}
 void inserir(Lista *lista, int number) {
    No *instanciaMemoria = (No *) sizeof(No);
    lista->cabecalho->number = number;
    lista->cabecalho = instanciaMemoria;
    lista->cabecalho->proximo = NULL;
}

int main(void) {
    printf("Olá, mundo\n");
    return 0;
}
