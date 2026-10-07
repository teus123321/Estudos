#include <stdio.h>
#include <stdlib.h>



//vetor
#define max 100
typedef struct Vetor {
    int dados[max];
}Vetor;

void iniciaVetor(Vetor *vetor) {
    for (size_t i = 0; i<max; i++) {
        vetor->dados[i] = 0;
    }
}

int inserirDadosVetor(Vetor *vetor, size_t indice, int dados) {
    if (indice >= max) {
        return 0;
    }
    vetor->dados[indice] = dados;
    return 1;
}

int estaNoVetor(Vetor *vetor, int dados) {
    for (int i = 0; i <max; i++) {
        if (vetor ->dados[i] == dados) {
            return 1;
        }
    }
    return 0;
}

int trocarIndiceVetor(Vetor *vetor, size_t indexOne, size_t indexTwo) {
    for (int i = 0; i<max; i++) {
        if (vetor->dados[i] == vetor->dados[indexOne]) {
            vetor->dados[i] = vetor->dados[indexTwo];
            return 1;
        }
        return 0;
    }
}

void imprimirVetor(Vetor *vetor){
    for(int i = 0; i<max; i++){
        printf("%d", vetor->dados[i]);
    }
}



/*
int trocarIndiceVetor(Vetor *vetor, size_t indexOne, size_t indexTwo) {
    int i = 0;
    while(i < max){
        if(vetor->dados[i] == indexOne){
            vetor->dados[i] = indexOne;
            if(vetor->dados[i] == indexTwo){
                vetor
            }
        }
    }
}
*/
/*

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

    // Testar
    int *i = 0;
    while (aux != NULL) {
        if (aux->number[i] == indexOne) {
            aux->number = indexTwo;
            indexTwo = indexOne;
        }
        if (aux->number == indexTwo) {
            aux->number = indexOne;
        }
        aux = aux->proximo;
    }
}
*/

int main(void) {
    /*
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
    */
    Vetor vetor;
    iniciaVetor(&vetor);
    printf("%d\n",inserirDadosVetor(&vetor, 0, 1));
    printf("%d\n",inserirDadosVetor(&vetor, 1, 2));
    printf("%d\n",estaNoVetor(&vetor, 1));
    printf("%d\n",estaNoVetor(&vetor, 2));
    printf("%d\n",trocarIndiceVetor(&vetor, 0, 1));
    imprimirVetor(&vetor);
    return 0;
}
