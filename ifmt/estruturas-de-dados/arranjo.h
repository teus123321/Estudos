//
// Created by User on 12/10/2026.
//

#ifndef UNTITLED1_ARRANJO_H
#define UNTITLED1_ARRANJO_H

#include <stdio.h>

#define MAX 1000

typedef struct Arranjo {
    int number[MAX];
    int tamanho;
}Arranjo;

void iniciarArranjo(Arranjo *arranjo) {
    arranjo->tamanho = MAX;
    for (int i = 0; i < MAX; i++) {
        arranjo->number[i] = i;
    }
}

void imprimirArranjo(Arranjo *arranjo) {
    for (int i = 0; i < arranjo->tamanho; i++) {
        printf("%d\n", arranjo->number[i]);
    }
}


void inserirArranjo(Arranjo *arranjo, int number) {
    if (arranjo->tamanho >= MAX) {
        return;
    }
    for (int i = arranjo->tamanho; i > 0; i--) {
        arranjo->number[i] = arranjo->number[i - 1];
    }
    arranjo->number[0] = number;
    arranjo->tamanho++;

}

void removerArranjo(Arranjo *arranjo) {

    for (int i = 0; i < arranjo->tamanho; i++) {
        if (arranjo->number[i] == arranjo->number[0]) {
            for (int j = i; j < arranjo->tamanho - 1 ; j++) {
                arranjo->number[j] = arranjo->number[j + 1];
            }
            arranjo->tamanho--;
            return;
        }
    }
}



#endif //UNTITLED1_ARRANJO_H
