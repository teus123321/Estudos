#include <stdio.h>

#define valorMaximo 100;

#include<stdio.h>

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

int main(void) {
    /*unsigned char nome[] = "Mateus";
    const long double i = -20.0000;
    printf("Imprimindo a variavel long double : %.2f\n", (float)i, "|");
    printf("Solucao correta :\n");
    printf("Imprimindo a variavel long double : %.10Lf\n", i);
    printf("Imprimindo o nome : %s", nome);
    int a;
    printf("Imprimindo endereco de memoria : %x\n", &a);
    */
    Lista lista;
    lista.segundo = 0;
    /*inserir(&lista, 10);
    printf("Hello, World!\n");
    inserir(&lista, 10);
    imprimir(&lista);
    delete(&lista, 10);
    imprimir(&lista); */
    inserir(&lista, 20);
    inserir(&lista, 40);
    inserir(&lista, 50);
    imprimir(&lista);
    delete(&lista, 40);
    imprimir(&lista);
    return 0;
}
