#include <stdio.h>
#include <stdlib.h>

#define valorMaximo 100;

/*
Troca por ponteiro — Escreva void troca(int *a, int *b) que troca o valor de duas variáveis.

Soma via ponteiro — Função que recebe um array e seu tamanho, e retorna a soma percorrendo o array só com aritmética de ponteiros (sem array[i]).

Maior e menor — Função void min_max(int *v, int n, int *menor, int *maior) que preenche os ponteiros menor e maior com os valores extremos do array.

Inverter array in-place — Função que inverte um array usando dois ponteiros (um no início, outro no fim) que se movem um em direção ao outro.

Strlen manual — Implemente sua própria int minha_strlen(char *s) usando ponteiro (sem usar string.h).

Strcpy manual — Implemente void minha_strcpy(char *dest, char *src).

Contar vogais com ponteiro — Função que recebe char *s e retorna quantas vogais tem, andando o ponteiro com s++.

Alocação dinâmica — Peça um número n ao usuário, aloque um array de n inteiros com malloc, preencha, some e depois dê free.

Ponteiro para ponteiro — Escreva uma função que recebe int **matriz, int linhas, int colunas (matriz alocada dinamicamente) e imprime todos os valores.

Lista ligada simples — Crie uma struct No { int valor; struct No *prox; }, e escreva uma função inserir_fim que adiciona um nó no final de uma lista ligada.

*/



#define MAX 100

typedef struct  {
    int primeiro[MAX];
    int segundo;
} Lista;

void inserir(Lista *lista, int number){
    if(lista->segundo < MAX) {
        lista->primeiro[lista->segundo] = number;
        lista->segundo++;
    };
};

void delete(Lista *lista, int number){
    for (int i = 0; i<lista->segundo; i++) {
        if (number == lista->primeiro[i]){
            for (int j = i; j<lista->segundo - 1; j++) {
                lista->primeiro[j] = lista->primeiro[j + 1];
        }
        lista->segundo--;
        break;
        }
    }
  }


void imprimir(Lista *lista) {
    for (int i = 0; i<lista->segundo; i++) {
        printf("%d\n", lista->primeiro[i]);
    };
};

//Troca por ponteiro — Escreva void troca(int *a, int *b) que troca o valor de duas variáveis.
void trocarPonteiro(int a, int b){
    int *aux = &a;
    int *auxTwo = &b;
    int *temp = aux;
    aux = auxTwo;
    auxTwo = temp;
    printf("%d, %d\n", *aux,*auxTwo);
}

//Soma via ponteiro — Função que recebe um array e seu tamanho, e retorna a soma percorrendo o array só com aritmética de ponteiros (sem array[i]).
void somaArray(int tamanho) {
    int *list = (int *) malloc(tamanho * sizeof(int));
    int *lista = list;
    int soma = 0;
    for (int i = 0; i<tamanho; i++) {
        *lista = i;
        soma += *lista;
        printf("%d", soma);
    }
    free(list);
}

void test() {
    int n = 5;
    int *ptr;
    ptr = (int *) malloc((n * sizeof(int)));

    if (ptr != NULL) {
        printf("Malloc alocado. Alocacaoo de memoria dinanica efetuada\n");

        for (int i = 0; i < n; i++) {
            ptr[i] = i;
        }

        for (int j = 0; j < n; j++){
            printf("%d", ptr[j]);
        }
    }
}


typedef struct No {
    int number;
    struct No *next;
} No ;

void insere(No **lista, int number) {
    No *ptr =(No *) malloc(sizeof(No));

    ptr->number = number;
    ptr->next = *lista;
    *lista = ptr;

}

void inverteLista(No *lista) {
    No *list = lista;

    for (int i = 0; i<list->number; i++) {
        int new = list->number;
        list = lista->next;
        // erro na lógica do for
        printf("%d", list->number);
        printf("%d", new);
    }
}

void imprimindo(No *lista) {

    No *atual = lista;

    while (atual != NULL) {
        printf("%d\n", atual->number);
        atual = atual->next;
    }
}

int main(void) {
        /*unsigned char nome[] = "Mateus";
        const long double i = -20.0000;
        printf("Imprimindo a variavel long double : %.2f\n", (float)i, "|");
        printf("Solucao correta :\n");
        printf("Imprimindo a variavel long double : %.10Lf\n", i);
        printf("Imprimindo o nome : %s", nome);
        int a;
        printf("Imprimindo endereco de memoria : %x\n", &a);
        Lista lista;
        lista.segundo = 0;
        /*inserir(&lista, 10);
        printf("Hello, World!\n");
        inserir(&lista, 10);
        imprimir(&lista);
        delete(&lista, 10);
        imprimir(&lista);
        inserir(&lista, 20);
        inserir(&lista, 40);
        inserir(&lista, 50);
        imprimir(&lista);
        delete(&lista, 40);
        imprimir(&lista);
        */

        //trocarPonteiro( 1,4);
        //somaArray(4);

        No *lista = NULL;
        insere(&lista,4);
        insere(&lista,2);
        insere(&lista,1);
        insere(&lista,3);
        imprimindo(lista);
        inverteLista(lista);


        return 0;
    }
