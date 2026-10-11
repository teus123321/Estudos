#include <stdio.h>
#include "fila.h"
#include "pilha.h"
#include "lista.h"
int main(void) {

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
    return 0;
}
