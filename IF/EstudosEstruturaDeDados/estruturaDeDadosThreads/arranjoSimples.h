#ifndef ARRANJO_SIMPLES_H
#define ARRANJO_SIMPLES_H
#include <omp.h>

#include <stdio.h>
#include <stddef.h>

#include <stdio.h>
#include <stddef.h>

#define MAX 500000

typedef struct Arranjo {
    int number[MAX];
    int tamanho;
}Arranjo;

static inline void iniciarArranjo(Arranjo *arranjo){
    if (arranjo == NULL) return;
    arranjo->tamanho = MAX;
    double inicio = omp_get_wtime();
    for (int i = 0; i < MAX; i++) {
        arranjo->number[i] = i;
    }
    double fim = omp_get_wtime();
    printf("Sequencial: %.9f segundos\n",
           fim - inicio);
}

static inline void printfArranjo(Arranjo *arranjo){
    if (arranjo == NULL) return;
    printf("[");
    for (int i = 0; i < arranjo->tamanho; i++) {
        printf("%d,", arranjo->number[i]);
    }
    printf("]\n");
}

#endif // ARRANJO_SIMPLES_H