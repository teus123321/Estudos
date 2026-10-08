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

//fila

typedef struct Fila {
    No *inicio;
}Fila;

void iniciarFila(Fila *fila){
    fila->inicio = NULL;
}

void inserirNaFila(Fila *fila, int number){
    No *instanciaMemoria = (No *) malloc(sizeof(No));
    instanciaMemoria->proximo = fila->inicio;
    fila->inicio = instanciaMemoria;
    fila->inicio->number = number;
}

void desenfileirar(Fila *fila){
    No *atual = fila->inicio->proximo;
    fila->inicio->proximo = atual->proximo;
    free(atual);
}

void imprimirFila(Fila *fila){
    struct No *atual = fila->inicio->proximo;
    printf("[");
    while(atual != NULL){
        printf("%d,",atual->number);
        atual = atual->proximo;
    }
    printf("]\n");
}


//pilha
typedef struct Pilha {
    No *inicio;
    No *fim;
}Pilha;

void iniciarPilha(Pilha *pilha){
    pilha->inicio = NULL;
    pilha->fim = NULL;
}

void inserirNaPilha(Pilha *pilha, int number){
    No *instanciaMemoria = (No *) malloc(sizeof(No));
    instanciaMemoria->proximo = pilha->inicio;
    pilha->inicio = instanciaMemoria;
    pilha->inicio->number = number;
}

void desempilhar(Pilha *pilha){

}

void imprimirPilha(Pilha *pilha){
    No *atual = pilha->inicio;
    printf("[");
    while(atual != NULL){
        printf("%d,",atual->number);
        atual = atual->;
    }
    printf("]\n");
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
    */
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
