#ifndef ARRANJO_THREADS_H
#define ARRANJO_THREADS_H
#include <omp.h>

#include <stdio.h>
#include <stddef.h>

#include <stdio.h>
#include <stddef.h>

#define MAX 500000

typedef struct ArranjoThreads {
    int number[MAX];
    int tamanho;
}ArranjoThreads;

static inline void iniciarArranjoThreads(ArranjoThreads *arranjo){
    if (arranjo == NULL) return;
    arranjo->tamanho = MAX;
    double inicio = omp_get_wtime();
    #pragma omp parallel for
    for (int i = 0; i < MAX; i++) {
        arranjo->number[i] = i;
    }
    double fim = omp_get_wtime();
    printf("Paralelo: %.9f segundos\n",
           fim - inicio);
}

static inline void printfArranjoThreads(ArranjoThreads *arranjo){
    if (arranjo == NULL) return;
    printf("[");
    for (int i = 0; i < arranjo->tamanho; i++) {
        printf("%d,", arranjo->number[i]);
    }
    printf("]\n");
    
}

#endif // ARRANJO_THREADS_H