#include <stdio.h>
#include <stdlib.h>
#include "arranjoSimples.h"
#include "arranjoThreados.h"
#define MAX 500000

int main (void){
    Arranjo *arranjo = malloc(sizeof *arranjo);
    ArranjoThreads *arranjoThreads =
        malloc(sizeof *arranjoThreads);

    if (arranjo == NULL || arranjoThreads == NULL) {
        printf("Erro de alocacao!\n");
        free(arranjo);
        free(arranjoThreads);
        return 1;
    }

    iniciarArranjo(arranjo);
    iniciarArranjoThreads(arranjoThreads);

    long long sumOne = 0;
    long long sumTwo = 0;

    for (int i = 0; i < MAX; i++) {
        sumOne += arranjo->number[i];
        sumTwo += arranjoThreads->number[i];
    }

    printf("Soma sequencial: %lld\n", sumOne);
    printf("Soma paralela: %lld\n", sumTwo);

    free(arranjo);
    free(arranjoThreads);

    return 0;
};