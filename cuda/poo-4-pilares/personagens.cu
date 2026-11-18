#include <stdio.h>
#include <cuda_runtime.h>

// ABSTRAÇÃO: esta classe define o que todo personagem sabe fazer.
class Personagem {
private:
    int poder; // ENCAPSULAMENTO: não pode ser alterado diretamente de fora.

public:
    __device__ Personagem(int valor) : poder(valor) {}

    __device__ int getPoder() const {
        return poder;
    }

    // Método abstrato: cada classe filha precisa definir como atacar.
    __device__ virtual int atacar() const = 0;

    __device__ virtual ~Personagem() {}
};

// HERANÇA: Guerreiro é um tipo de Personagem.
class Guerreiro : public Personagem {
public:
    __device__ Guerreiro(int valor) : Personagem(valor) {}

    __device__ int atacar() const override {
        return getPoder() * 2;
    }
};

// HERANÇA: Mago também é um tipo de Personagem.
class Mago : public Personagem {
public:
    __device__ Mago(int valor) : Personagem(valor) {}

    __device__ int atacar() const override {
        return getPoder() + 10;
    }
};

// POLIMORFISMO: recebe qualquer classe filha de Personagem.
// O método atacar() executado depende do tipo real do objeto.
__device__ int realizarAtaque(const Personagem &personagem) {
    return personagem.atacar();
}

// Cada thread da GPU calcula o dano de um personagem.
__global__ void calcularDanos(const int *poderes, int *danos, int quantidade) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i >= quantidade) {
        return;
    }

    if (i % 2 == 0) {
        Guerreiro guerreiro(poderes[i]); // Objeto criado na GPU.
        danos[i] = realizarAtaque(guerreiro);
    } else {
        Mago mago(poderes[i]); // Outro tipo de objeto na GPU.
        danos[i] = realizarAtaque(mago);
    }
}

int main() {
    const int quantidade = 6;
    const int valores[quantidade] = {5, 10, 15, 20, 25, 30};
    const size_t bytes = quantidade * sizeof(int);

    int *poderes = nullptr;
    int *danos = nullptr;

    // Memória que pode ser acessada pela CPU e pela GPU.
    if (cudaMallocManaged(&poderes, bytes) != cudaSuccess) {
        printf("Erro ao alocar os poderes na GPU.\n");
        return 1;
    }
    if (cudaMallocManaged(&danos, bytes) != cudaSuccess) {
        printf("Erro ao alocar os danos na GPU.\n");
        cudaFree(poderes);
        return 1;
    }

    for (int i = 0; i < quantidade; i++) {
        poderes[i] = valores[i];
    }

    // 1 bloco com 6 threads: uma thread por personagem.
    calcularDanos<<<1, quantidade>>>(poderes, danos, quantidade);

    cudaError_t erro = cudaGetLastError();
    if (erro == cudaSuccess) {
        erro = cudaDeviceSynchronize(); // Aguarda o trabalho da GPU.
    }

    if (erro != cudaSuccess) {
        printf("Erro no CUDA: %s\n", cudaGetErrorString(erro));
        cudaFree(poderes);
        cudaFree(danos);
        return 1;
    }

    for (int i = 0; i < quantidade; i++) {
        const char *tipo = (i % 2 == 0) ? "Guerreiro" : "Mago";
        printf("%s | poder: %d | dano: %d\n", tipo, poderes[i], danos[i]);
    }

    cudaFree(poderes);
    cudaFree(danos);
    return 0;
}
