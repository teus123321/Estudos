#include <stdio.h>

#define valorMaximo 100;

int main(void) {
    unsigned char nome[] = "Mateus";
    const long double i = -20.0000;
    printf("Imprimindo a variavel long double : %.2f\n", (float)i, "|");
    printf("Solucao correta :\n");
    printf("Imprimindo a variavel long double : %.10Lf\n", i);
    printf("Imprimindo o nome : %s", nome);
    int a;
    printf("Imprimindo endereco de memoria : %x\n", &a);
    return 0;
}
