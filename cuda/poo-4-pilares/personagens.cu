#include <stdio.h>
#include <cuda_runtime.h>

// CLASSE BASE: Personagem define as características de todos os personagens.
// ABSTRAÇÃO: sabemos que todo personagem ataca, mas cada tipo ataca de um jeito.
class Personagem {
private:
    // ENCAPSULAMENTO: o atributo só pode ser acessado pelos métodos da classe.
    int poder;

public:
    // CONSTRUTOR: roda quando um personagem é criado.
    // __device__ indica que esse construtor é executado na GPU.
    // O parâmetro "valor" é recebido e guardado no atributo "poder".
    __device__ Personagem(int valor) {
        poder = valor;
    }

    // GETTER: permite ler o poder sem acessar o atributo privado diretamente.
    // const: o método promete não alterar os atributos do objeto.
    __device__ int getPoder() const {
        return poder;
    }

    // __device__: este método pertence ao código executado na GPU.
    // virtual: permite usar a versão de atacar() da classe filha.
    // const: atacar() não modifica o objeto.
    // = 0: método abstrato; toda classe filha precisa implementá-lo.
    __device__ virtual int atacar() const = 0;

    // ~Personagem(): destrutor, chamado quando o objeto é destruído.
    // virtual garante destruição correta quando usamos a classe base.
    __device__ virtual ~Personagem() {}
};

// HERANÇA: Guerreiro reaproveita a classe Personagem.
// ": public Personagem" significa "Guerreiro é um Personagem".
class Guerreiro : public Personagem {
public:
    // Os dois-pontos aqui chamam o CONSTRUTOR DA CLASSE PAI.
    // Primeiro, Personagem(valor) guarda o poder; depois, Guerreiro fica pronto.
    // Isso NÃO é a mesma coisa que os dois-pontos em "private:" ou "public:".
    __device__ Guerreiro(int valor) : Personagem(valor) {}

    // override: substitui o método virtual atacar() definido em Personagem.
    __device__ int atacar() const override {
        return getPoder() * 2; // Guerreiro causa o dobro do poder.
    }
};

// HERANÇA: Mago também reaproveita Personagem, mas ataca de outro jeito.
class Mago : public Personagem {
public:
    // Chama o construtor da classe pai para guardar o valor do poder.
    __device__ Mago(int valor) : Personagem(valor) {}

    __device__ int atacar() const override {
        return getPoder() + 10; // Mago acrescenta 10 pontos ao poder.
    }
};

// POLIMORFISMO: recebe qualquer classe filha de Personagem.
// O símbolo & indica que recebemos o objeto por referência (sem copiá-lo).
// Se receber Guerreiro, chama Guerreiro::atacar(). Se receber Mago,
// chama Mago::atacar(). O mesmo nome "atacar" tem comportamentos diferentes.
__device__ int realizarAtaque(const Personagem &personagem) {
    return personagem.atacar();
}

// __global__: esta função é chamada pela CPU, mas executada na GPU.
// Cada thread da GPU calcula o dano de UM personagem.
__global__ void calcularDanos(const int *poderes, int *danos, int quantidade) {
    // threadIdx.x: posição da thread dentro do bloco.
    // blockIdx.x: número do bloco; blockDim.x: threads por bloco.
    // Juntos, calculam o índice do personagem que esta thread processa.
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i >= quantidade) {
        return;
    }

    if (i % 2 == 0) { // Índices pares: Guerreiro.
        Guerreiro guerreiro(poderes[i]); // Objeto criado na GPU.
        danos[i] = realizarAtaque(guerreiro);
    } else { // Índices ímpares: Mago.
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

    // <<<1, quantidade>>>: 1 bloco com 6 threads, uma por personagem.
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
